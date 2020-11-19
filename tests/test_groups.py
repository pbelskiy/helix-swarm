import re

import pytest
import responses

from helixswarm import SwarmClient, SwarmError


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
        after='some-group',
        keywords='test-group',
        fields=['Group', 'Owners', 'Users', 'config'],
        limit=2
    )

    assert 'groups' in response


@responses.activate
def test_groups_get_info():
    data = {
        'group': {
            'Group': 'test-group',
            'Owners': [],
            'Users': ['bruno'],
            'config': {
                'description': 'Our testing group',
                'emailFlags': [],
                'name': 'Test Group'
            }
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/groups/my-group'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.groups.get_info(
        'my-group',
        fields=['Group', 'Owners', 'Users', 'config']
    )

    assert 'group' in response


@responses.activate
def test_group_create():
    data = {
        'group': {
            'Group': 'my-group',
            'MaxLockTime': None,
            'MaxResults': None,
            'MaxScanRows': None,
            'Owners': ['username'],
            'PasswordTimeout': None,
            'Subgroups': [],
            'Timeout': None,
            'Users': [],
            'config': {
                'description': 'This group is special to me.',
                'emailFlags': {
                    'reviews': '1',
                    'commits': '0'
                },
                'name': 'My Group',
                'useMailingList': True
            }
        }
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/groups'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    with pytest.raises(SwarmError):
        client.groups.create('my-group')

    response = client.groups.create(
        'my-group',
        owners=['alice', 'bob'],
        users=['bruno', 'user2'],
        subgroups=['subgroup_1'],
        name='My Group',
        description='This group is special to me.',
        notify_reviews=True,
        notify_commits=True,
        email_address='my-group@host.domain',
        use_mailing_list=True,
    )

    assert 'group' in response


@responses.activate
def test_edit():
    data = {
        'group': {
            'Group': 'my-group',
            'Users': ['root'],
            'Owners': ['Pedro', 'Pablo'],
            'Subgroups': ['subgroup_2'],
            'config': {
                'description': 'This group is special to me.',
                'emailAddress': 'test-group@host.domain',
                'emailFlags': {
                    'reviews': '1',
                    'commits': '1'
                },
                'name': 'My Group',
                'useMailingList': True
            }
        }
    }

    responses.add(
        responses.PATCH,
        re.compile(r'.*/api/v\d+/groups/my-group'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.groups.edit(
        'my-group',
        owners=['root'],
        users=['Pedro', 'Pablo'],
        subgroups=['subgroup_2'],
        name='My Group',
        description='This group is special to me.',
        notify_reviews=True,
        notify_commits=True,
        email_address='test-group@host.domain',
        use_mailing_list=True,
    )

    assert 'group' in response


@responses.activate
def test_delete():
    data = {
        'id': 'my-group'
    }

    responses.add(
        responses.DELETE,
        re.compile(r'.*/api/v\d+/groups/my-group'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.groups.delete('my-group')
    assert 'id' in response
