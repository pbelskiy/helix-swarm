import re

from typing import Tuple, Any

import requests

from .reviews import Reviews


class Swarm:

    def __init__(self, url: str, user: str, password: str):
        """
        Core library class

        If API version isn`t specified in host URL then it will be detected
        automatically (latest available on server).
        """
        self._host, self._api_version = self._get_host_and_api_version(url)

        self._session = requests.Session()
        self._session.auth = (user, password)

        if self._api_version is None:
            self._set_latest_api_version()

        self.reviews = Reviews(self)

    @staticmethod
    def _get_host_and_api_version(url: str) -> Tuple[str, str]:
        match = re.match(r'.+(/api/v(\d+(?:\.\d+)?))', url)
        if match:
            host = url[:match.start(1)]
            version = match.group(2)
        else:
            host = url
            version = None

        return host.strip('/'), version

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        return self._session.request(
            method,
            '{host}/api/{version}/{path}'.format(
                host=self._host,
                version=self._api_version,
                path=path,
            ),
            **kwargs
        ).json()

    def _set_latest_api_version(self) -> str:
        known_versions = (1, 1.1, 1.2, 2, 3, 4, 5, 6, 7, 8, 9, 10)

        for version in reversed(known_versions):
            self._api_version = str(version)
            if 'error' not in self.get_version():
                break

    def get_version(self) -> dict:
        return self._request('GET', 'version')
