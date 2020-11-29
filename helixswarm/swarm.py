import json
import re

from abc import ABC, abstractmethod
from collections import namedtuple
from http import HTTPStatus
from typing import Any, Callable, Tuple

from helixswarm.endpoints.activities import Activities
from helixswarm.endpoints.changes import Changes
from helixswarm.endpoints.comments import Comments
from helixswarm.endpoints.groups import Groups
from helixswarm.endpoints.projects import Projects
from helixswarm.endpoints.reviews import Reviews
from helixswarm.endpoints.workflows import Workflows
from helixswarm.exceptions import SwarmError, SwarmNotFoundError

Response = namedtuple('Response', ['status', 'body'])


class Swarm(ABC):

    def __init__(self):
        self.activities = Activities(self)
        self.changes = Changes(self)
        self.comments = Comments(self)
        self.groups = Groups(self)
        self.projects = Projects(self)
        self.reviews = Reviews(self)
        self.workflows = Workflows(self)

    @staticmethod
    def _get_host_and_api_version(url: str) -> Tuple[str, str]:
        match = re.match(r'.+(/api/v(\d+(?:\.\d+)?))', url)
        if not match:
            raise SwarmError('Please specify using API version in host URL')

        host = url[:match.start(1)].strip('/')
        version = match.group(2)
        return host, version

    @staticmethod
    def _callback(response: Response) -> dict:
        try:
            decoded_body = json.loads(response.body)
        except json.decoder.JSONDecodeError as e:
            raise SwarmError from e

        if response.status == HTTPStatus.NOT_FOUND:
            # temporary workaround, need to check Swarm source code
            # coments.add() may return SwarmError (404) with valid json and comment #2
            if 'error' not in decoded_body:
                return decoded_body

            raise SwarmNotFoundError(decoded_body)

        if response.status != HTTPStatus.OK:
            raise SwarmError(response.body)

        return decoded_body

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def request(self,
                callback: Callable[[Response], dict],
                method: str,
                path: str,
                **kwargs: Any
                ) -> dict:
        raise NotImplementedError

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        return self.request(self._callback, method, path, **kwargs)

    def get_version(self) -> dict:
        """
        Show server version information. This can be used to determine the
        currently-installed Swarm version, and also to check that Swarm’s API
        is responding as expected.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self._request('GET', 'version')
