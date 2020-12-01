from typing import Dict, List, Optional, Union

from helixswarm.helpers import minimal_version


class Users:

    def __init__(self, swarm):
        self.swarm = swarm

    @minimal_version(9)
    def get(self,
            *,
            fields: Optional[List[str]] = None,
            users: Optional[List[str]] = None,
            group: Optional[str] = None
            ) -> dict:
        """
        Get list of users.

        * fields: ``List[str]`` (optional)
          List of fields to show for each user. Omitting this parameter or passing
          an empty value shows all fields. Be aware the fields are case sensitive
          for users. You can use one of the below: User, Type, Email, Update,
          Access, FullName, JobView, Password, AuthMethod, Reviews.

        * users: ``List[str]`` (optional)
          List of users to display. Omitting this parameter or passing an empty
          value shows all users.

        * group: ``str`` (optional)
          An optional to get users from a group. Cannot be used with users parameter.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, Union[str, List[str]]]

        if fields:
            params['fields'] = ','.join(fields)

        if users:
            params['users'] = ','.join(users)

        if group:
            params['group'] = group

        return self.swarm._request('GET', 'users', params=params)

    @minimal_version(9)
    def unfollow_all(self, name: str) -> dict:
        """
        Unfollow all users and projects, admin and super users are permitted to
        execute unfollow all against any target user. Other users are only
        permitted to execute the call if they themselves are the target user

        * name: ``str``
          User name.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self.swarm._request('GET', 'users/{}/unfollowall'.format(name))
