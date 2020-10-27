import json
import re

from collections import namedtuple
from http import HTTPStatus
from typing import Any, Tuple

from .endpoints.comments import Comments
from .endpoints.reviews import Reviews
from .exceptions import SwarmError, SwarmNotFoundError

Response = namedtuple('Response', ['status', 'body'])


class Swarm:
    """
    Core library class

    If API version isn`t specified in host URL then it will be detected
    automatically (latest available on server).
    """
    def __init__(self, url: str, user: str, password: str):
        host, self._api_version = self._get_host_and_api_version(url)

        self.connector = self.connect(host, user, password, self._api_version)

        self.reviews = Reviews(self)
        self.comments = Comments(self)

    def connect(self, host: str, user: str, password: str, version: str) -> Any:
        raise NotImplementedError

    def close(self) -> None:
        return self.connector.close()

    @staticmethod
    def _get_host_and_api_version(url: str) -> Tuple[str, str]:
        match = re.match(r'.+(/api/v(\d+(?:\.\d+)?))', url)
        if not match:
            raise SwarmError('Please specify using API version in host URL')

        host = url[:match.start(1)].strip('/')
        version = match.group(2)
        return host, version

    @property
    def api_version(self) -> float:
        return float(self._api_version)

    @staticmethod
    def _callback(response: Response) -> dict:
        if response.status == HTTPStatus.NOT_FOUND:
            raise SwarmNotFoundError(json.loads(response.body))

        if response.status != HTTPStatus.OK:
            raise SwarmError(response.body)

        return json.loads(response.body)

    def _request(self, method, path, data=None):
        return self.connector.request(self._callback, method, path, data=data)

    def get_version(self) -> dict:
        return self._request('GET', 'version')
