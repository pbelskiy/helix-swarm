from helixswarm.helpers import minimal_version


class Servers:

    def __init__(self, swarm):
        self.swarm = swarm

    @minimal_version(9)
    def get(self) -> dict:
        """
        Gets a list of servers.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self.swarm._request('GET', 'servers')
