import json
import re

from abc import ABC, abstractmethod
from collections import namedtuple
from http import HTTPStatus
from typing import Any, Callable, Optional, Tuple

from helixswarm.endpoints.activities import Activities
from helixswarm.endpoints.changes import Changes
from helixswarm.endpoints.comments import Comments
from helixswarm.endpoints.groups import Groups
from helixswarm.endpoints.projects import Projects
from helixswarm.endpoints.reviews import Reviews
from helixswarm.endpoints.servers import Servers
from helixswarm.endpoints.users import Users
from helixswarm.endpoints.workflows import Workflows
from helixswarm.exceptions import SwarmError, SwarmNotFoundError
from helixswarm.helpers import minimal_version

Response = namedtuple('Response', ['status', 'body'])


class Swarm(ABC):

    def __init__(self):
        self.activities = Activities(self)
        self.changes = Changes(self)
        self.comments = Comments(self)
        self.groups = Groups(self)
        self.projects = Projects(self)
        self.reviews = Reviews(self)
        self.servers = Servers(self)
        self.users = Users(self)
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
    def _validate_retry_argument(retry: dict) -> None:
        for key in retry:
            if key not in ('total', 'factor', 'statuses'):
                raise SwarmError('Unknown key in retry argument: ' + key)

        if retry.get('total', 0) <= 0:
            raise SwarmError('Invalid `total` in retry argument must be > 0')

    @staticmethod
    def _callback(response: Response, fcb: Callable) -> dict:
        # function callback used to support both sync and async syntax
        fcb = fcb or (lambda response: response)

        try:
            decoded_body = json.loads(response.body)
        except json.decoder.JSONDecodeError as e:
            raise SwarmError from e

        if response.status == HTTPStatus.NOT_FOUND:
            # temporary workaround, need to check Swarm source code
            # coments.add() may return SwarmError (404) with valid json and comment #2
            if 'error' not in decoded_body:
                return fcb(decoded_body)

            raise SwarmNotFoundError(decoded_body)

        if response.status != HTTPStatus.OK:
            raise SwarmError(response.body)

        return fcb(decoded_body)

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def request(self,
                callback: Callable,
                method: str,
                path: str,
                fcb: Optional[Callable] = None,
                **kwargs: Any
                ) -> dict:
        raise NotImplementedError

    def _request(self,
                 method: str,
                 path: str,
                 fcb: Optional[Callable] = None,
                 **kwargs: Any
                 ) -> dict:
        return self.request(self._callback, method, path, fcb, **kwargs)

    def get_version(self) -> dict:
        """
        Show server version information. This can be used to determine the
        currently-installed Swarm version, and also to check that Swarm’s API
        is responding as expected.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self._request('GET', 'version')

    @minimal_version(9)
    def check_auth(self, token: Optional[str] = None) -> dict:
        """
        Checking the 2FA authentication.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        if token:
            return self._request('POST', 'checkauth', data=dict(token=token))

        return self._request('GET', 'checkauth')

    @minimal_version(9)
    def get_auth_methods(self) -> dict:
        """
        Returns the complete list of methods of 2FA.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self._request('GET', 'listmethods')

    @minimal_version(9)
    def init_auth(self, method: str) -> dict:
        """
        Initiating the 2FA authentication.

        * method
          The Method in which you want to use.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self._request('POST', 'initauth', data=dict(method=method))

    @minimal_version(9)
    def check_session(self) -> dict:
        """
        Get the current effective user details.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self._request('GET', 'session')

    @minimal_version(9)
    def init_session(self) -> dict:
        """
        Create a new Swarm session using the given credentials.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self._request('POST', 'session')

    @minimal_version(9)
    def destroy_session(self) -> dict:
        """
        Destroy the current session, for instance logout.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self._request('DELETE', 'session')

    @minimal_version(9)
    def login(self, saml: Optional[bool] = None) -> dict:
        """
        Login to Swarm.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        if saml is not None:
            return self._request('POST', 'login/saml')

        return self._request('POST', 'login')

    @minimal_version(9)
    def logout(self, saml: Optional[bool] = None) -> dict:
        """
        Logout of Swarm.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self._request('POST', 'logout')
