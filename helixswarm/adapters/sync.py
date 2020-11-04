from typing import Any, Callable, Optional

from requests import Session

from helixswarm.swarm import Response, Swarm


class SwarmClient(Swarm):

    def __init__(self,
                 url: str,
                 user: str,
                 password: str,
                 *,
                 verify: bool = True,
                 timeout: Optional[float] = None
                 ):
        """
        Swarm client class.

        * url: ``str``
          Url of Swarm server, must include API version.

        * user: ``str``
          User name, login.

        * password: ``str``
          Password for user.

        * verify: ``bool`` (optional)
          Verify SSL (default: true).

        * timeout: ``float`` (optional)
          HTTP request timeout.

        :returns: ``SwarmClient instance``
        :raises: ``SwarmError``
        """
        super().__init__()

        self.host, self.version = self._get_host_and_api_version(url)

        auth = (user, password)

        session = Session()
        session.auth = auth

        self.session = session
        self.timeout = timeout
        self.verify = verify

    def close(self) -> None:
        self.session.close()

    def request(self,
                callback: Callable[[Response], dict],
                method: str,
                path: str,
                **kwargs: Any
                ) -> dict:

        if self.timeout and 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        response = self.session.request(
            method,
            '{host}/api/v{version}/{path}'.format(
                host=self.host,
                version=self.version,
                path=path,
            ),
            verify=self.verify,
            **kwargs
        )

        return callback(Response(response.status_code, response.text))
