import re

import responses

from helixswarm import SwarmClient


@responses.activate
def test_get():
    data = {
        'projects': [
            {
                'id': 'testproject1',
                'description': 'Test test test',
                'members': ['alice'],
                'name': 'TestProject'
            },
            {
                'id': 'testproject2',
                'description': 'Test test test',
                'members': ['alice'],
                'name': 'TestProject'
            }
        ]
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/projects'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.projects.get(
        fields=['id', 'description', 'members', 'name'],
        workflow='some-workflow'
    )

    assert 'projects' in response
