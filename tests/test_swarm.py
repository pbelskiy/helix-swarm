from unittest.mock import Mock

from helixswarm import Swarm


def test_get_host_and_api_version():
    host, version = Swarm._get_host_and_api_version('http://swarm-server.com/api/v9')
    assert host == 'http://swarm-server.com'
    assert version == '9'

    host, version = Swarm._get_host_and_api_version('http://swarm-server.com/')
    assert host == 'http://swarm-server.com'
    assert version is None

    host, version = Swarm._get_host_and_api_version('http://swarm-server.com')
    assert host == 'http://swarm-server.com'
    assert version is None

    host, version = Swarm._get_host_and_api_version('swarm-server.com')
    assert host == 'swarm-server.com'
    assert version is None

    host, version = Swarm._get_host_and_api_version('swarm-server.com/api/v1.2')
    assert host == 'swarm-server.com'
    assert version == '1.2'


def test_version_detect(monkeypatch):
    data = [
        # v10
        {
            'error': 'Not Found'
        },
        # v9
        {
            'apiVersions': [1, 1.1, 1.2, 2, 3, 4, 5, 6, 7, 8, 9],
            'version': 'SWARM/2018.2/1705499 (2018/09/25)',
            'year': '2018'
        }
    ]

    monkeypatch.setattr('helixswarm.Swarm._request', Mock(side_effect=data))

    client = Swarm('host', 'login', 'password')
    assert client._api_version == '9'
