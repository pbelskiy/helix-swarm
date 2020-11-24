from typing import Dict, List, Optional, Union

from helixswarm.helpers import minimal_version


class Workflows:

    def __init__(self, swarm):
        self.swarm = swarm

    @minimal_version(9)
    def get(self,
            *,
            fields: Optional[List[str]] = None,
            no_cache: Optional[bool] = None
            ) -> dict:
        """
        Gets workflows.

        * fields: ``List[str]`` (optional)
          An optional list of fields to show for each workflow. Omitting this
          parameter or passing an empty value shows all fields.

        * noCache: ``bool`` (optional)
          If provided and has a value of 'true' a query will always be performed
          and the cache of workflows is ignored. Otherwise the cache will be used
          if it exists.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, Union[str, bool]]

        if fields:
            params['fields'] = ','.join(fields)

        if no_cache:
            params['noCache'] = no_cache

        return self.swarm._request('GET', 'workflows', params=params)

    @minimal_version(9)
    def get_info(self,
                 identifier: int,
                 *,
                 fields: Optional[List[str]] = None
                 ) -> dict:
        """
        Gets a workflow by identifier.

        * identifier: ``int``
          Workflow id.

        * fields: ``List[str]`` (optional)
          An optional list of fields to show for each workflow. Omitting this
          parameter or passing an empty value shows all fields.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, str]

        if fields:
            params['fields'] = ','.join(fields)

        response = self.swarm._request(
            'GET',
            'workflows/{}'.format(identifier),
            params=params
        )

        return response
