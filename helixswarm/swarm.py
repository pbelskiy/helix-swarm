import re

from http import HTTPStatus
from typing import Any, Optional, Tuple

import requests

from .endpoints.reviews import Reviews
from .exceptions import SwarmError, SwarmNotFoundError


class Swarm:
    """
    Core library class

    If API version isn`t specified in host URL then it will be detected
    automatically (latest available on server).
    """
    def __init__(self, url: str, user: str, password: str):
        self._host, self._api_version = self._get_host_and_api_version(url)

        self._session = requests.Session()
        self._session.auth = (user, password)

        if self._api_version is None:
            self._set_latest_api_version()

        self.reviews = Reviews(self)

    @staticmethod
    def _get_host_and_api_version(url: str) -> Tuple[str, Optional[str]]:
        match = re.match(r'.+(/api/v(\d+(?:\.\d+)?))', url)
        if match:
            host = url[:match.start(1)].strip('/')
            version = match.group(2)
            return host, version

        return url.strip('/'), None

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        response = self._session.request(
            method,
            '{host}/api/{version}/{path}'.format(
                host=self._host,
                version=self._api_version,
                path=path,
            ),
            **kwargs
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise SwarmNotFoundError(response.json())

        if response.status_code != HTTPStatus.OK:
            raise SwarmError(response)

        return response.json()

    def _set_latest_api_version(self) -> None:
        known_versions = (1, 1.1, 1.2, 2, 3, 4, 5, 6, 7, 8, 9, 10)

        for version in reversed(known_versions):
            self._api_version = str(version)
            if 'error' not in self.get_version():
                break

    def get_version(self) -> dict:
        return self._request('GET', 'version')
