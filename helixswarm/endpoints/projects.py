from typing import Dict, List, Optional, Union


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

    def create(self,
               name: str,
               members: List[str],
               *,
               subgroups: Optional[List[str]] = None,
               owners: Optional[List[str]] = None,
               description: Optional[str] = None,
               is_private: Optional[bool] = None,
               deploy_config: Optional[dict] = None,
               tests_config: Optional[dict] = None,
               branches: Optional[List[dict]] = None,
               job_view: Optional[str] = None,
               notify_commits: Optional[bool] = None,
               notify_reviews: Optional[bool] = None,
               defaults: Optional[List[dict]] = None,
               retain_default_reviewers: Optional[bool] = None,
               minimum_up_votes: Optional[str] = None
               ) -> dict:
        """
        Creates a new project.

        * name: ``str``
          Project name (is also used to generate the Project ID).

        * members: ``List[str]``
          Array of project members.

        * subgroups: ``List[str]`` (optional)
          Array of project subgroups.

        * owners: ``List[str]`` (optional)
          Array of project owners.

        * description: ``str`` (optional)
          Project description.

        * private: ``bool`` (optional)
          Private projects are visible only to: members, moderators, owners,
          and administrators. Default: false

        * deploy: ``dict`` (optional)
          Configuration for automated deployment.

          Example: {'enabled': True, 'url': 'http://localhost/?change={change}'}

        * tests:  ``dict`` (optional)
          Configuration for testing, continuous integration.

          Example: {'url': '', 'enabled': False}

        * branches: ``List[dict]`` (optional)
          Branch definitions for this project.

          Example:

        .. code-block:: python

          [
            {
              'name': 'Branch One',
              'paths': '//depot/main/TestProject/...'
            }
          ]

        * jobview: ``str`` (optional)
          Jobview for associating certain jobs with this project.

          Example: 'subsystem=testproject'

        * notify_commits: ``bool`` (optional)
          Email members, moderators and followers when a change is committed.

        * notify_reviews: ``bool`` (optional)
          Email members and moderators when a new review is requested.

        * defaults: ``List[dict]`` (optional)
          Array of defaults at a project level (for example default reviewers).

          Example: [{'reviewers': {'user2': {'required': True}}]

        * retain_default_reviewers: ``bool`` (optional)
          Retain the default reviewers.

        * minimum_up_votes: ``str`` (optional)
          Minimum number of up votes required.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        data = dict(
            name=name,
            members=members,
        )  # type: Dict[str, Union[str, bool, dict, List[str], List[dict]]]

        if subgroups:
            data['subgroups'] = subgroups

        if owners:
            data['owners'] = owners

        if description:
            data['description'] = description

        if is_private is not None:
            data['private'] = is_private

        if deploy_config:
            data['deploy'] = deploy_config

        if tests_config:
            data['tests'] = tests_config

        if branches:
            data['branches'] = branches

        if job_view:
            data['jobview'] = job_view

        if notify_commits is not None:
            data['emailFlags[change_email_project_users]'] = notify_commits

        if notify_reviews is not None:
            data['emailFlags[review_email_project_members]'] = notify_reviews

        if defaults:
            data['defaults'] = defaults

        if retain_default_reviewers is not None:
            data['retainDefaultReviewers'] = retain_default_reviewers

        if minimum_up_votes:
            data['minimumUpVotes'] = minimum_up_votes

        return self.swarm._request('POST', 'projects', json=data)

    def edit(self,
             identifier: str,
             *,
             name: str,
             members: List[str],
             subgroups: Optional[List[str]] = None,
             owners: Optional[List[str]] = None,
             description: Optional[str] = None,
             is_private: Optional[bool] = None,
             deploy_config: Optional[dict] = None,
             tests_config: Optional[dict] = None,
             branches: Optional[List[dict]] = None,
             job_view: Optional[str] = None,
             notify_commits: Optional[bool] = None,
             notify_reviews: Optional[bool] = None,
             defaults: Optional[List[dict]] = None,
             retain_default_reviewers: Optional[bool] = None,
             minimum_up_votes: Optional[str] = None
             ) -> dict:
        """
        Edit a project.

        * identifier: ``str``
          Project ID

        * name: ``str`` (optional)
          Project name, changing the project name does not change the project ID.

        * members: ``List[str]`` (optional)
          Array of project members.

        * subgroups: ``List[str]`` (optional)
          Array of project subgroups.

        * owners: ``List[str]`` (optional)
          Array of project owners.

        * description: ``str`` (optional)
          Project description.

        * private: ``bool`` (optional)
          Private projects are visible only to: members, moderators, owners,
          and administrators. Default: false

        * deploy: ``dict`` (optional)
          Configuration for automated deployment.

          Example: {'enabled': True, 'url': 'http://localhost/?change={change}'}

        * tests:  ``dict`` (optional)
          Configuration for testing, continuous integration.

          Example: {'url': '', 'enabled': False}

        * branches: ``List[dict]`` (optional)
          Branch definitions for this project.

          Example:

          .. code-block:: python

            [
              {
                'name': 'Branch One',
                'paths': '//depot/main/TestProject/...'
              }
            ]

        * jobview: ``str`` (optional)
          Jobview for associating certain jobs with this project.

          Example: 'subsystem=testproject'

        * notify_commits: ``bool`` (optional)
          Email members, moderators and followers when a change is committed.

        * notify_reviews: ``bool`` (optional)
          Email members and moderators when a new review is requested.

        * defaults: ``List[dict]`` (optional)
          Array of defaults at a project level (for example default reviewers).

          Example: [{'reviewers': {'user2': {'required': True}}]

        * retain_default_reviewers: ``bool`` (optional)
          Retain the default reviewers.

        * minimum_up_votes: ``str`` (optional)
          Minimum number of up votes required.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        data = dict()  # type: Dict[str, Union[str, bool, dict, List[str], List[dict]]]

        if name:
            data['name'] = name

        if members:
            data['members'] = members

        if subgroups:
            data['subgroups'] = subgroups

        if owners:
            data['owners'] = owners

        if description:
            data['description'] = description

        if is_private is not None:
            data['private'] = is_private

        if deploy_config:
            data['deploy'] = deploy_config

        if tests_config:
            data['tests'] = tests_config

        if branches:
            data['branches'] = branches

        if job_view:
            data['jobview'] = job_view

        if notify_commits is not None:
            data['emailFlags[change_email_project_users]'] = notify_commits

        if notify_reviews is not None:
            data['emailFlags[review_email_project_members]'] = notify_reviews

        if defaults:
            data['defaults'] = defaults

        if retain_default_reviewers is not None:
            data['retainDefaultReviewers'] = retain_default_reviewers

        if minimum_up_votes:
            data['minimumUpVotes'] = minimum_up_votes

        response = self.swarm._request(
            'PATCH',
            'projects/{}'.format(identifier),
            json=data
        )

        return response

    def delete(self, identifier: str) -> dict:
        """
        Delete a project, mark a Swarm project as deleted. The project ID and
        name cannot be reused. If a project has owners set, only the owners can
        perform this action.

        * identifier: ``str``
          Project ID

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        response = self.swarm._request(
            'DELETE',
            'projects/{}'.format(identifier)
        )

        return response
