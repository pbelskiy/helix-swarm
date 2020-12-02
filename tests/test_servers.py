import re

import responses

from helixswarm import SwarmClient


@responses.activate
def test_get():
    data = {
        'servers': {
            'Master': {
                'port': 'ssl:10.33.44.55:1666'
            },
            'Artifacts': {
                'port': '10.55.66.77:1666'
            }
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/servers'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.servers.get()
    assert 'servers' in response
