from typing import Any, Callable

import requests

from helixswarm.swarm import Response, Swarm


class Connector:

    def __init__(self, host: str, user: str, password: str, version: str):
        self.session = requests.session()
        self.session.auth = (user, password)

        self.host = host
        self.version = version

    def close(self) -> None:
        self.session.close()

    def request(self,
                callback: Callable[[Response], dict],
                method: str,
                path: str,
                **kwargs: Any
                ) -> dict:
        response = self.session.request(
            method,
            '{host}/api/v{version}/{path}'.format(
                host=self.host,
                version=self.version,
                path=path,
            ),
            **kwargs
        )

        return callback(Response(response.status_code, response.text))


class SwarmClient(Swarm):

    def connect(self, host: str, user: str, password: str, version: str) -> Connector:
        return Connector(host, user, password, version)
