import asyncio

from typing import Any, Callable, Optional

import aiohttp

from helixswarm.swarm import Response, Swarm


class Connector:

    def __init__(self, host: str, user: str, password: str, version: Optional[str]):
        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()

        self.host = host
        self.version = version
        self.auth = aiohttp.BasicAuth(user, password)

    async def close(self) -> None:
        await self. session.close()

    async def request(self,
                      callback: Callable[[Response], dict],
                      method: str,
                      path: str,
                      **kwargs: Any
                      ) -> dict:
        response = await self.session.request(
            method,
            '{host}/api/v{version}/{path}'.format(
                host=self.host,
                version=self.version,
                path=path,
            ),
            auth=self.auth,
            **kwargs
        )

        body = await response.text()
        return callback(Response(response.status, body))


class SwarmAsyncClient(Swarm):

    def connect(self, host: str, user: str, password: str, version: Optional[str]) -> Connector:
        return Connector(host, user, password, version)
