from typing import Dict, List, Optional, Union

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
