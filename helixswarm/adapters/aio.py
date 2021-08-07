import asyncio

from typing import Any, Callable, Optional, Union

from aiohttp import (
    BasicAuth,
    ClientError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
)

from helixswarm.swarm import Response, Swarm, SwarmError


class RetryClientSession:

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop], options: dict):
        self.total = options['total']
        self.factor = options.get('factor', 1)
        self.statuses = options.get('statuses', [])

        self.session = ClientSession(loop=loop)

    async def request(self, *args: Any, **kwargs: Any) -> ClientResponse:
        for total in range(self.total):
            try:
                response = await self.session.request(*args, **kwargs)
            except (ClientError, asyncio.TimeoutError) as e:
                if total + 1 == self.total:
                    raise SwarmError from e
            else:
                if response.status not in self.statuses:
                    break

            await asyncio.sleep(self.factor * (2 ** (total - 1)))

        return response

    async def close(self) -> None:
        await self.session.close()


class SwarmAsyncClient(Swarm):

    session = None  # type: Union[ClientSession, RetryClientSession]
    timeout = None

    def __init__(self,
                 url: str,
                 user: str,
                 password: str,
                 *,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 verify: bool = True,
                 timeout: Optional[float] = None,
                 retry: Optional[dict] = None
                 ):
        """
        Swarm async client class.

        * url: ``str``
          Url of Swarm server, must include API version.

        * user: ``str``
          User name, login.

        * password: ``str``
          Password for user.

        * loop: ``AbstractEventLoop`` (optional)
          Asyncio current event loop.

        * verify: ``bool`` (optional)
          Verify SSL (default: true).

        * timeout: ``int``, (optional)
          HTTP request timeout.

        * retry: ``dict`` (optional)
          Retry options to prevent failures if server restarting or temporary
          network problem. Disabled by default use total > 0 to enable.

          - total: ``int`` Total retries count.
          - factor: ``int`` Sleep factor between retries (default 1)
            {factor} * (2 ** ({number of total retries} - 1))
          - statuses: ``List[int]`` HTTP statues retries on. (default [])

          Example:

          .. code-block:: python

            retry = dict(
                total=10,
                factor=1,
                statuses=[500]
            )

        :returns: ``SwarmClient instance``
        :raises: ``SwarmError``
        """
        super().__init__()

        self.loop = loop or asyncio.get_event_loop()
        self.host, self.version = self._get_host_and_api_version(url)

        self.auth = BasicAuth(user, password)

        if retry:
            self._validate_retry_argument(retry)
            self.session = RetryClientSession(loop, retry)
        else:
            self.session = ClientSession(loop=self.loop)

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
