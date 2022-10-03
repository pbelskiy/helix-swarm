from typing import Any, Callable, Optional, Tuple

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import \
    Retry  # pylint: disable=import-error

from helixswarm.swarm import Response, Swarm


class SwarmClient(Swarm):

    auth_update_callback = None

    def __init__(self,
                 url: str,
                 user: str,
                 password: str,
                 *,
                 verify: bool = True,
                 timeout: Optional[float] = None,
                 retry: Optional[dict] = None,
                 auth_update_callback: Optional[Callable[[], Tuple[str, str]]] = None
                 ) -> None:
        """
        Swarm client class.

        Args:
            url (str):
                URL of Swarm server, must include API version.

            user (str):
                User name.

            password (str):
                Password for user.

            verify (Optional[bool])
                Verify SSL (default: true).

            timeout (Optional[float]):
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

                With factor = 1

                ============  =============
                Retry number  Sleep
                ============  =============
                1              0.5 seconds
                2              1.0 seconds
                3              2.0 seconds
                4              4.0 seconds
                5              8.0 seconds
                6             16.0 seconds
                7             32.0 seconds
                8              1.1 minutes
                9              2.1 minutes
                10             4.3 minutes
                11             8.5 minutes
                12            17.1 minutes
                13            34.1 minutes
                14             1.1 hours
                15             2.3 hours
                16             4.6 hours
                17             9.1 hours
                18            18.2 hours
                19            36.4 hours
                20            72.8 hours
                ============  =============

            auth_update_callback (Optional[Callable[[], Tuple[str, str]]])
                Callback function which will be called on SwarmUnauthorizedError
                to update user and password and retry request again.

        Returns:
            SwarmClient: class instance.
        """
        super().__init__()

        self.host, self.version = self._get_host_and_api_version(url)

        self.session = Session()
        self.session.auth = (user, password)
        self.timeout = timeout
        self.verify = verify

        self.auth_update_callback = auth_update_callback

        if not retry:
            return

        self._validate_retry_argument(retry)

        adapter = HTTPAdapter(max_retries=Retry(
            total=retry['total'],
            backoff_factor=retry.get('factor', 1),
            status_forcelist=retry.get('statuses', []),
            method_whitelist=['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT', 'TRACE'],
        ))

        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def close(self) -> None:
        self.session.close()

    def request(self,
                callback: Callable,
                method: str,
                path: str,
                fcb: Optional[Callable] = None,
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

        return callback(Response(response.status_code, response.text), fcb)

    def _update_auth(self) -> None:
        if self.auth_update_callback is None:
            return

        user, password = self.auth_update_callback()
        self.session.auth = (user, password)
