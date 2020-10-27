import pytest

from aioresponses import aioresponses

from helixswarm import SwarmAsyncClient


@pytest.mark.asyncio
async def test_async_client():
    data = {
        'apiVersions': [1, 1.1, 1.2, 2, 3, 4, 5, 6, 7, 8, 9],
        'version': 'SWARM/2018.2/1705499 (2018/09/25)',
        'year': '2018'
    }

    try:
        client = SwarmAsyncClient('http://server/api/v9', 'login', 'password')
        with aioresponses() as mock:
            mock.get('http://server/api/v9/version', status=200, payload=data)
            version = await client.get_version()

        assert version['year'] == '2018'
    finally:
        await client.close()
