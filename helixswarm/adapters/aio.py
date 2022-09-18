import asyncio

from typing import Any, Awaitable, Callable, Optional, Tuple, Union

from aiohttp import (
    BasicAuth,
    ClientError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
)

from helixswarm.swarm import Response, Swarm, SwarmError


class RetryClientSession:

    def __init__(self, options: dict) -> None:
        self.total = options['total']
        self.factor = options.get('factor', 1)
        self.statuses = options.get('statuses', [])
        self.methods = options.get('methods', [
            'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT', 'TRACE'
        ])

        self.session = ClientSession()

    async def request(self, *args: Any, **kwargs: Any) -> ClientResponse:
        for total in range(self.total):
            try:
                response = await self.session.request(*args, **kwargs)
            except (ClientError, asyncio.TimeoutError) as e:
                if total + 1 == self.total:
                    raise SwarmError from e
            else:
                if response.method.upper() not in self.methods:
                    break
                if response.status not in self.statuses:
                    break

            await asyncio.sleep(self.factor * (2 ** (total - 1)))

        return response

    async def close(self) -> None:
        await self.session.close()


class SwarmAsyncClient(Swarm):

    session = None  # type: Union[ClientSession, RetryClientSession]
    timeout = None
    auth_update_callback = None

    def __init__(self,
                 url: str,
                 user: str,
                 password: str,
                 *,
                 verify: bool = True,
                 timeout: Optional[float] = None,
                 retry: Optional[dict] = None,
                 auth_update_callback: Optional[Callable[[], Awaitable[Tuple[str, str]]]] = None
                 ) -> None:
        """
        Swarm async client class.

        Args:
            url (str):
                URL of Swarm server, must include API version.

            user (str):
                User name.

            password (str):
                Password for user.

            verify (Optional[bool]):
                Verify SSL (default: true).

            timeout (Optional[int])
                HTTP request timeout.

            retry (Optional[dict]):
                Retry options to prevent failures if server restarting or
                temporary network problem. Disabled by default use total > 0 to
                enable.

                - total: ``int`` Total retries count.
                - factor: ``int`` Sleep factor between retries (default 1)
                    {factor} * (2 ** ({number of total retries} - 1))
                - statuses: ``List[int]`` HTTP statues retries on. (default [])
                - methods: ``List[str]`` list of HTTP methods to retry, idempotent
                    methods are used by default.

                Example:

                .. code-block:: python

                    retry = dict(
                        total=10,
                        factor=1,
                        statuses=[500]
                    )

            auth_update_callback (Optional[Callable[[], Tuple[str, str]]):
                Callback function which will be called on SwarmUnauthorizedError
                to update user and password and retry request again.

        Returns:
            SwarmAsyncClient: instance
        """
        super().__init__()

        self.host, self.version = self._get_host_and_api_version(url)

        self.auth = BasicAuth(user, password)
        self.auth_update_callback = auth_update_callback

        if retry:
            self._validate_retry_argument(retry)
            self.session = RetryClientSession(retry)
        else:
            self.session = ClientSession()

        self.verify = verify

        if timeout:
            self.timeout = ClientTimeout(total=timeout)

    async def close(self) -> None:  # type: ignore
        await self.session.close()

    async def request(self,  # type: ignore
                      callback: Callable,
                      method: str,
                      path: str,
                      fcb: Optional[Callable] = None,
                      **kwargs: Any
                      ) -> dict:

        if self.timeout and 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        response = await self.session.request(
            method,
            '{host}/api/v{version}/{path}'.format(
                host=self.host,
                version=self.version,
                path=path,
            ),
            auth=self.auth,
            ssl=self.verify,
            **kwargs
        )

        body = await response.text()
        return callback(Response(response.status, body), fcb)

    async def _update_auth(self) -> Any:
        if self.auth_update_callback is None:
            return

        user, password = await self.auth_update_callback()
        self.auth = BasicAuth(user, password)
