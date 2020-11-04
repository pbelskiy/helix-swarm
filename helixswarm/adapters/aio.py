import asyncio

from typing import Any, Callable, Optional

from aiohttp import BasicAuth, ClientSession, ClientTimeout

from helixswarm.swarm import Response, Swarm


class SwarmAsyncClient(Swarm):

    def __init__(self,
                 url: str,
                 user: str,
                 password: str,
                 *,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 verify: bool = True,
                 timeout: Optional[int] = None
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

        :returns: ``SwarmClient instance``
        :raises: ``SwarmError``
        """
        super().__init__()

        self.loop = loop or asyncio.get_event_loop()
        self.host, self.version = self._get_host_and_api_version(url)

        self.auth = BasicAuth(user, password)
        self.session = ClientSession(loop=self.loop)

        self.verify = verify
        self.timeout = None  # Optional[ClientTimeout]
        if timeout:
            self.timeout = ClientTimeout(total=timeout)

    async def close(self) -> None:  # type: ignore
        await self.session.close()

    async def request(self,  # type: ignore
                      callback: Callable[[Response], dict],
                      method: str,
                      path: str,
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
        return callback(Response(response.status, body))
