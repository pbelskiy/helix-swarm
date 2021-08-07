import re

import aiohttp
import pytest
from requests.packages.urllib3.util import retry
import responses

from aioresponses import aioresponses

from helixswarm import SwarmAsyncClient, SwarmClient, SwarmError

GET_VERSION_DATA = {
    'apiVersions': [1, 1.1, 1.2, 2, 3, 4, 5, 6, 7, 8, 9],
    'version': 'SWARM/2018.2/1705499 (2018/09/25)',
    'year': '2018'
}


@pytest.fixture
def aiohttp_mock():
    with aioresponses() as mock:
        yield mock


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


def test_retry_argument_validation():
    with pytest.raises(SwarmError):
        SwarmClient(
            'http://server/api/v9',
            'login',
            'password',
            retry=dict(total=1, strange_argument=1)
        )

    with pytest.raises(SwarmError):
        SwarmAsyncClient(
            'http://server/api/v9',
            'login',
            'password',
            retry=dict(total=0)
        )


@responses.activate
def test_response_invalid_json():
    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/version'),
        body='invalid json',
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    with pytest.raises(SwarmError):
        client.get_version()


@responses.activate
def test_response_non_ok():
    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/version'),
        json={'error': 'server error'},
        status=500
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    with pytest.raises(SwarmError):
        client.get_version()


@responses.activate
def test_sync_client():
    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/version'),
        json=GET_VERSION_DATA,
        status=200
    )

    try:
        client = SwarmClient(
            'http://server/api/v9',
            'login',
            'password',
            timeout=10,
        )

        version = client.get_version()
        assert version['year'] == '2018'
    finally:
        client.close()


@responses.activate
def test_sync_client_retry():
    # responses library does`t support Retry mock
    # https://github.com/getsentry/responses/issues/135
    # so, just cover code of retry constructor
    client = SwarmClient(
        'http://server/api/v9',
        'login',
        'password',
        retry=dict(
            total=10,
            factor=1,
            statuses=[400, 500],
        )
    )

    assert client.session.adapters['http://'].max_retries.status_forcelist == [400, 500]


@pytest.mark.asyncio
async def test_async_client(aiohttp_mock):
    try:
        client = SwarmAsyncClient(
            'http://server/api/v9',
            'login',
            'password',
            timeout=10,
        )

        aiohttp_mock.get(
            'http://server/api/v9/version',
            payload=GET_VERSION_DATA,
            status=200,
        )

        version = await client.get_version()
        assert version['year'] == '2018'
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_async_client_retry(aiohttp_mock):
    client = SwarmAsyncClient(
        'http://server/api/v9',
        'login',
        'password',
        retry=dict(
            total=10,
            statuses=[500],
        )
    )

    aiohttp_mock.get(
        'http://server/api/v9/version',
        payload={'error': 'Server error'},
        status=500,
    )

    aiohttp_mock.get(
        'http://server/api/v9/version',
        payload=GET_VERSION_DATA,
        status=200,
    )

    version = await client.get_version()
    assert version['year'] == '2018'
    await client.close()


@pytest.mark.asyncio
async def test_async_client_retry_exception(aiohttp_mock):
    client = SwarmAsyncClient(
        'http://server/api/v9',
        'login',
        'password',
        retry=dict(
            total=2,
            statuses=[500],
        )
    )

    aiohttp_mock.get('http://server/api/v9/version', exception=aiohttp.ClientError())
    aiohttp_mock.get('http://server/api/v9/version', exception=aiohttp.ClientError())

    with pytest.raises(SwarmError):
        await client.get_version()

    await client.close()


@responses.activate
def test_check_auth():
    data = {
        'results': {
            'trigger': 'GAuth says yes!',
            'successMsg': 'Second factor authentication approved.'
        },
        'code': 200
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/checkauth'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.check_auth()
    assert 'results' in response


@responses.activate
def test_check_auth_token():
    data = {
        'results': {
            'trigger': 'GAuth says yes!',
            'successMsg': 'Second factor authentication approved.'
        },
        'code': 200
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/checkauth'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.check_auth('TOKEN')
    assert 'results' in response


@responses.activate
def test_get_auth_methods():
    data = {
        'results': {
            'methods': {
                '1': {
                    'methodName': 'Method Name will be here',
                    'methodDesc': 'Method Description will be here'
                },
                '2': {
                    'methodName': 'Method Name will be here',
                    'methodDesc': 'Method Description will be here'
                },
                '3': {
                    'methodName': 'Method Name will be here',
                    'methodDesc': 'Method Description will be here'
                },
                '4': {
                    'methodName': 'Method Name will be here',
                    'methodDesc': 'Method Description will be here'
                }
            }
        },
        'option': {
            'persist': 'option',
            'nextState': 'init-auth'
        },
        'code': 200
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/listmethods'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.get_auth_methods()
    assert 'results' in response


@responses.activate
def test_init_auth():
    data = {
        'results': {
            'trigger': 'TriggerName',
            'successMsg': 'Message from Authentication method'
        },
        'option': {
            'prompt': True,
            'nextState': 'check-auth'
        },
        'code': 200
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/initauth'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.init_auth('METHOD')
    assert 'results' in response


@responses.activate
def test_check_session():
    data = {
        'isValid': True,
        'messages': [],
        'user': {
            'User': 'reviewer',
            'FullName': 'Code Reviewer',
            'Email': 'reviewer@swarm.local',
            'Type': 'standard',
            'Password': 'enabled'
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/session'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.check_session()
    assert 'user' in response


@responses.activate
def test_init_session():
    data = {
        'isValid': True,
        'messages': [],
        'user': {
            'User': 'reviewer',
            'FullName': 'Code Reviewer',
            'Email': 'reviewer@swarm.local',
            'Type': 'standard',
            'Password': 'enabled'
        }
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/session'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.init_session()
    assert 'user' in response


@responses.activate
def test_destroy_session():
    data = {
        'isValid': True,
        'messages': []
    }

    responses.add(
        responses.DELETE,
        re.compile(r'.*/api/v\d+/session'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.destroy_session()
    assert 'messages' in response


@responses.activate
def test_login():
    data = {
        'isValid': True,
        'messages': [],
        'user': {
            'User': 'swarm.user',
            'FullName': 'Swarm User',
            'Email': 'swarm.user@mydomain.com',
            'Type': 'standard',
            'Password': 'enabled',
            'isAdmin': False,
            'isSuper': False
        }
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/login'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.login()
    assert 'user' in response


@responses.activate
def test_login_saml():
    data = {
        'isValid': 'true',
        'url': '&lt;url to redirect to&gt;'
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/login/saml'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.login(saml=True)
    assert 'isValid' in response


@responses.activate
def test_logout():
    data = {
        'isValid': True,
        'messages': []
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/logout'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.logout()
    assert 'messages' in response
