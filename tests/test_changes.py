import re

import responses

from helixswarm import SwarmClient


@responses.activate
def test_get_affects_projects():
    data = {
        'change': {
            'id': '1050',
            'projects': {
                'jam': [
                    'live',
                    'main'
                ]
            }
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/changes/\d+/affectsprojects'),
        json=data
    )

    client = SwarmClient('http://server/api/v8', 'login', 'password')

    response = client.changes.get_affects_projects(1050)
    assert 'projects' in response['change']


@responses.activate
def test_get_default_reviewers():
    data = {
        'change': {
            'id': '1050',
            'defaultReviewers': {
                'groups': {
                    'group1': {'required': '1'},
                    'group2': {}
                },
                'users': {
                    'user1': {},
                    'user2': {'required': 'true'}
                }
            }
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/changes/\d+/defaultreviewers'),
        json=data
    )

    client = SwarmClient('http://server/api/v8', 'login', 'password')

    response = client.changes.get_default_reviewers(1050)
    assert 'defaultReviewers' in response['change']


@responses.activate
def test_get_check_status():
    data = {
        'status':   'OK',
        'isValid':  'true',
        'messages': []
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/changes/\d+/check'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.changes.get_check_status(1050, 'enforced')
    assert 'status' in response
