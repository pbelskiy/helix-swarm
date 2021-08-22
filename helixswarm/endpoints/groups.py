from typing import Dict, List, Optional, Union

from helixswarm.exceptions import SwarmError
from helixswarm.helpers import minimal_version


class Groups:

    def __init__(self, swarm):
        self.swarm = swarm

    @minimal_version(2)
    def get(self,
            *,
            after: Optional[str] = None,
            limit: Optional[int] = None,
            fields: Optional[List[str]] = None,
            keywords: Optional[str] = None
            ) -> dict:
        """
        Returns the complete list of groups in Swarm.

        * after: ``str`` (optional)
          A group ID to seek to. Groups prior to and including the specified ID
          are excluded from the results and do not count towards ``limit``.
          Useful for pagination. Commonly set to the ``lastSeen`` property from
          a previous query.

        * limit: ``int`` (optional)
          Maximum number of groups to return. This does not guarantee that
          ``limit`` groups are returned. It does guarantee that the number of
          groups returned won’t exceed ``limit``. Default: 100.

        * fields:  ``List[str]`` (optional)
          List of fields to show for each group.
          Omitting this parameter or passing an empty value shows all fields.

        * keywords: ``str`` (optional)
          Keywords to limit groups on. Only groups where the group ID, group name
          (if set), or description contain the specified keywords are returned.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, Union[str, int]]

        if after:
            params['after'] = after

        if limit:
            params['max'] = limit

        if fields:
            params['fields'] = ','.join(fields)

        if keywords:
            params['keywords'] = keywords

        return self.swarm._request('GET', 'groups', params=params)

    @minimal_version(2)
    def get_info(self,
                 identifier: str,
                 *,
                 fields: Optional[List[str]]
                 ) -> dict:
        """
        Retrieve information about a group.

        * identifier: ``str``
          Group identifier.

        * fields:  ``List[str]`` (optional)
          List of fields to show for each group.
          Omitting this parameter or passing an empty value shows all fields.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, str]

        if fields:
            params['fields'] = ','.join(fields)

        response = self.swarm._request(
            'GET',
            'groups/{}'.format(identifier),
            params=params
        )

        return response

    @minimal_version(2)
    def create(self,
               identifier: str,
               *,
               users: Optional[List[str]] = None,
               owners: Optional[List[str]] = None,
               subgroups: Optional[List[str]] = None,
               name: Optional[str] = None,
               description: Optional[str] = None,
               email_address: Optional[str] = None,
               notify_reviews: Optional[bool] = None,
               notify_commits: Optional[bool] = None,
               use_mailing_list: Optional[bool] = None
               ) -> dict:
        """
        Create a new group.

        * identifier: ``str``
          Group identifier.

        * users: ``List[str]`` (optional)
          An optional array of group users.
          **At least one of Users, Owners, or Subgroups is required.**

        * owners: ``List[str]`` (optional)
          An optional array of group owners.
          **At least one of Users, Owners, or Subgroups is required.**

        * subgroups: ``List[str]`` (optional)
          An optional array of group subgroups.
          **At least one of Users, Owners, or Subgroups is required.**

        * name: ``str`` (optional)
          An optional full name for the group.

        * description: ``str`` (optional)
          An optional group description.

        * email_address: ``str`` (optional)
          The email address for this group.

        * notify_reviews: ``bool`` (optional)
          Email members when a new review is requested.

        * notify_commits: ``bool`` (optional)
          Email members when a change is committed.

        * use_mailing_list: ``bool`` (optional)
          Whether to use the configured email address or expand individual
          members addresses.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        data = dict()  # type: Dict[str, Union[str, bool, List[str]]]

        data['Group'] = identifier

        if not (users and owners and subgroups):
            raise SwarmError('At least one of users, owners, or subgroups is required')

        if users:
            data['Users'] = users
        if owners:
            data['Owners'] = owners
        if subgroups:
            data['Subgroups'] = subgroups

        if name:
            data['config[name]'] = name
        if description:
            data['config[description]'] = description
        if email_address:
            data['config[emailAddress]'] = email_address
        if notify_reviews:
            data['config[emailFlags][reviews]'] = notify_reviews
        if notify_commits:
            data['config[emailFlags][commits]'] = notify_commits
        if use_mailing_list:
            data['config[useMailingList]'] = use_mailing_list

        return self.swarm._request('POST', 'groups', json=data)

    @minimal_version(2)
    def edit(self,
             identifier: str,
             *,
             users: Optional[List[str]] = None,
             owners: Optional[List[str]] = None,
             subgroups: Optional[List[str]] = None,
             name: Optional[str] = None,
             description: Optional[str] = None,
             email_address: Optional[str] = None,
             notify_reviews: Optional[bool] = None,
             notify_commits: Optional[bool] = None,
             use_mailing_list: Optional[bool] = None
             ) -> dict:
        """
        Change the settings of a group, only super users and group owners can
        perform this action.

        * identifier: ``str``
          Group identifier.

        * users: ``List[str]`` (optional)
          An optional array of group users.
          **At least one of Users, Owners, or Subgroups is required.**

        * owners: ``List[str]`` (optional)
          An optional array of group owners.
          **At least one of Users, Owners, or Subgroups is required.**

        * subgroups: ``List[str]`` (optional)
          An optional array of group subgroups.
          **At least one of Users, Owners, or Subgroups is required.**

        * name: ``str`` (optional)
          An optional full name for the group.

        * description: ``str`` (optional)
          An optional group description.

        * email_address: ``str`` (optional)
          The email address for this group.

        * notify_reviews: ``bool`` (optional)
          Email members when a new review is requested.

        * notify_commits: ``bool`` (optional)
          Email members when a change is committed.

        * use_mailing_list: ``bool`` (optional)
          Whether to use the configured email address or expand individual
          members addresses.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        data = dict()  # type: Dict[str, Union[str, bool, List[str]]]

        if users:
            data['Users'] = users
        if owners:
            data['Owners'] = owners
        if subgroups:
            data['Subgroups'] = subgroups
        if name:
            data['config[name]'] = name
        if description:
            data['config[description]'] = description
        if email_address:
            data['config[emailAddress]'] = email_address
        if notify_reviews:
            data['config[emailFlags][reviews]'] = notify_reviews
        if notify_commits:
            data['config[emailFlags][commits]'] = notify_commits
        if use_mailing_list:
            data['config[useMailingList]'] = use_mailing_list

        response = self.swarm._request(
            'PATCH',
            'groups/{}'.format(identifier),
            json=data
        )

        return response

    @minimal_version(2)
    def delete(self, identifier: str) -> dict:
        """
        Delete a group, only super users and group owners can perform this action.

        * identifier: ``str``
          Group identifier.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self.swarm._request('DELETE', 'groups/{}'.format(identifier))
