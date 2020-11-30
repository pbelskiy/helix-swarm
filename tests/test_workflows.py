import re

import responses

from helixswarm import SwarmClient


@responses.activate
def test_get():
    data = {
        'workflows': [
            {
                'id': '1',
                'name': 'myWorkflow',
                'description': 'A description',
                'on_submit': {
                    'with_review': {
                        'rule': 'no_checking'
                    },
                    'without_review': {
                        'rule': 'no_checking'
                    }
                },
                'auto_approve': {
                    'rule': 'never'
                },
                'counted_votes': {
                    'rule': 'anyone'
                },
                'shared': 'true',
                'owners': [
                    'user1',
                    'user2'
                ]
            },
            {
                'id': '2',
                'name': 'myWorkflow 2',
                'description': 'A description',
                'on_submit': {
                    'with_review': {
                        'rule': 'no_checking'
                    },
                    'without_review': {
                        'rule': 'no_checking'
                    }
                },
                'auto_approve': {
                    'rule': 'votes'
                },
                'counted_votes': {
                    'rule': 'members'
                },
                'shared': 'true',
                'owners': [
                    'user3',
                    'user4'
                ]
            }
        ]
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/workflows'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.workflows.get(
        fields=[
            'id', 'name', 'description', 'on_submit', 'auto_approve',
            'counted_votes', 'shared', 'owners'
        ],
        no_cache=True
    )

    assert 'workflows' in response


@responses.activate
def test_get_info():
    data = {
        'workflow': {
            'id': '1',
            'name': 'myWorkflow',
            'description': 'A description',
            'on_submit': {
                'with_review': {
                    'rule': 'no_checking'
                },
                'without_review': {
                    'rule': 'no_checking'
                }
            },
            'auto_approve': {
                'rule': 'never'
            },
            'counted_votes': {
                'rule': 'anyone'
            },
            'shared': 'true',
            'owners': [
                'user1',
                'user2'
            ]
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/workflows/1'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.workflows.get_info(
        1,
        fields=[
            'id', 'name', 'description', 'on_submit', 'auto_approve',
            'counted_votes', 'shared', 'owners'
        ]
    )

    assert 'workflow' in response


@responses.activate
def test_create():
    data = {
        'workflow': {
            'id': '1',
            'name': 'myWorkflow',
            'description': 'A description',
            'on_submit': {
                'with_review': {
                    'rule': 'no_checking'
                },
                'without_review': {
                    'rule': 'no_checking'
                }
            },
            'auto_approve': {
                'rule': 'never'
            },
            'counted_votes': {
                'rule': 'members'
            },
            'shared': 'true',
            'owners': [
                'user1',
                'user2'
            ]
        }
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/workflows'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.workflows.create(
        'myWorkflow',
        owners=['user1', 'user2'],
        description='A description',
        shared=True,
        end_rules=['no_revision'],
        on_submit={
           'with_review': {'rule': 'no_checking'},
           'without_review': {'rule': 'no_checking'}
        },
        auto_approve='never',
        counted_votes='members',
    )

    assert 'workflow' in response


@responses.activate
def test_edit():
    data = {
        'workflow': {
            'id': '1',
            'name': 'myWorkflow',
            'description': 'A description',
            'on_submit': {
                'with_review': {
                    'rule': 'no_checking'
                },
                'without_review': {
                    'rule': 'no_checking'
                }
            },
            'auto_approve': {
                'rule': 'never'
            },
            'counted_votes': {
                'rule': 'anyone'
            },
            'shared': 'true',
            'owners': [
                'user1',
                'user2'
            ]
        }
    }

    responses.add(
        responses.PATCH,
        re.compile(r'.*/api/v\d+/workflows/1'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.workflows.edit(
        1,
        name='myWorkflow',
        owners=['user1', 'user2'],
        description='A description',
        shared=True,
        end_rules=['no_revision'],
        on_submit={
           'with_review': {'rule': 'no_checking'},
           'without_review': {'rule': 'no_checking'}
        },
        auto_approve='never',
        counted_votes='members',
    )

    assert 'workflow' in response
