from typing import Dict, List, Optional


class Projects:

    def __init__(self, swarm):
        self.swarm = swarm

    def get(self,
            *,
            fields: Optional[List[str]] = None,
            workflow: Optional[str] = None
            ) -> dict:
        """
        Returns a list of projects in Swarm that are visible to the current user.
        Administrators will see all projects, including private ones.

        * fields:  ``List[str]`` (optional)
          List of fields to show for each group.
          Omitting this parameter or passing an empty value shows all fields.

        * workflow: ``str`` (optional)
          List only projects using a workflow.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, str]

        if fields:
            params['fields'] = ','.join(fields)

        if workflow:
            params['workflow'] = workflow

        return self.swarm._request('GET', 'projects', params=params)

    def get_info(self,
                 identifier: str,
                 *,
                 fields: Optional[List[str]] = None
                 ) -> dict:
        """
        Retrieve information about a project.

        * identifier: ``str``
          Project identifier.

        * fields:  ``List[str]`` (optional)
          List of fields to show for each project.
          Omitting this parameter or passing an empty value shows all fields.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, str]

        if fields:
            params['fields'] = ','.join(fields)

        response = self.swarm._request(
            'GET',
            'projects/{}'.format(identifier),
            params=params
        )

        return response
