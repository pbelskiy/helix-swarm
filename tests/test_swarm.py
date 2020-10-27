import pytest

from helixswarm import SwarmClient, SwarmError


def test_get_host_and_api_version():
    host, version = SwarmClient._get_host_and_api_version('http://swarm-server.com/api/v9')
    assert host == 'http://swarm-server.com'
    assert version == '9'

    with pytest.raises(SwarmError):
        SwarmClient._get_host_and_api_version('http://swarm-server.com/')

    with pytest.raises(SwarmError):
        SwarmClient._get_host_and_api_version('http://swarm-server.com')

    with pytest.raises(SwarmError):
        SwarmClient._get_host_and_api_version('swarm-server.com')

    host, version = SwarmClient._get_host_and_api_version('swarm-server.com/api/v1.2')
    assert host == 'swarm-server.com'
    assert version == '1.2'
