from typing import Any, Callable, Optional

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from helixswarm.swarm import Response, Swarm


class SwarmClient(Swarm):

    def __init__(self,
                 url: str,
                 user: str,
                 password: str,
                 *,
                 verify: bool = True,
                 timeout: Optional[float] = None,
                 retry: Optional[dict] = None
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

        * retry: ``dict`` (optional)
          Retry options to prevent failures if server restarting or temporary
          network problem.

          - total: ``int`` Total retries count. (default 0)
          - factor: ``int`` Sleep between retries (default 0)
            {factor} * (2 ** ({number of total retries} - 1))
          - statuses: ``List[int]`` HTTP statues retries on. (default [])

          Example:

          .. code-block:: python

            retry = dict(
                attempts=10,
                factor=1,
                statuses=[500]
            )

        :returns: ``SwarmClient instance``
        :raises: ``SwarmError``
        """
        super().__init__()

        self.host, self.version = self._get_host_and_api_version(url)

        self.session = Session()
        self.session.auth = (user, password)
        self.timeout = timeout
        self.verify = verify

        if not retry:
            return

        adapter = HTTPAdapter(max_retries=Retry(
            total=retry.get('total', 0),
            backoff_factor=retry.get('factor', 0),
            status_forcelist=retry.get('statuses', []),
            method_whitelist=['GET', 'POST', 'PATCH'],
        ))

        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

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
