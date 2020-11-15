import re

import responses

from helixswarm import SwarmClient


@responses.activate
def test_groups_get():
    data = {
        'groups': [
            {
                'Group': 'test-group',
                'Owners': [],
                'Users': ['bruno'],
                'config': {
                    'description': 'Our testing group',
                    'emailAddress': 'test-group@host.domain',
                    'emailFlags': {
                        'reviews': '1',
                        'commits': '0'
                    },
                    'name': 'Test Group',
                    'useMailingList': True
                },
            },
            {
                'Group': 'test-group2',
                'Owners': [],
                'Users': ['bruno'],
                'config': {
                    'description': 'Our second testing group',
                    'emailAddress': 'test-group2@host.domain',
                    'emailFlags': [],
                    'name': 'Test Group 2',
                    'useMailingList': True
                }
            }
        ],
        'lastSeen': 'test-group2'
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/groups'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.groups.get(
        keywords='test-group',
        fields=['Group', 'Owners', 'Users', 'config'],
        limit=2
    )

    assert 'groups' in response
