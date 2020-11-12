import re

import aiohttp
import pytest
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
