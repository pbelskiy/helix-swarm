from helixswarm.helpers import minimal_version


class Changes:

    def __init__(self, swarm):
        self.swarm = swarm

    @minimal_version(8)
    def get_affects_projects(self, change: int) -> dict:
        """
        Get projects, and branches, affected by a given change id (**v8+**).

        * change: ``int``
          Change id.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self.swarm._request(
            'GET',
            'changes/{}/affectsprojects'.format(change)
        )

    @minimal_version(8)
    def get_default_reviewers(self, change: int) -> dict:
        """
        Get default reviewers for a given change id (**v8+**).

        * change: ``int``
          Change id.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self.swarm._request(
            'GET',
            'changes/{}/defaultreviewers'.format(change)
        )

    @minimal_version(9)
    def get_check_status(self, change: int, category: str) -> dict:
        """
        Performs checks on the change if workflow configuration requires it (**v9+**).

        * change: ``int``
          Change id to check.

        * category: ``str``
          The type of check. Must have a value of ``enforced``, ``strict`` or ``shelve``.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self.swarm._request(
            'GET',
            'changes/{}/check'.format(change),
            params=dict(type=category)
        )
