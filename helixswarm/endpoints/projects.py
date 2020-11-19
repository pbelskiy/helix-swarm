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
        Returns the complete list of groups in Swarm.

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
