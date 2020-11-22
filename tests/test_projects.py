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


@responses.activate
def test_get_info():
    data = {
        'project': {
            'id': 'testproject2',
            'defaults': [],
            'description': 'Test test test',
            'members': ['alice'],
            'name': 'TestProject 2'
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/projects'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.projects.get_info(
        'testproject2',
        fields=['id', 'description', 'members', 'name']
    )

    assert 'project' in response


@responses.activate
def test_create():
    data = {
        'project': {
            'id': 'testproject3',
            'defaults': [],
            'branches': [{'name': 'Branch One', 'paths': '//depot/main/TestProject/...'}],
            'deleted': False,
            'deploy': {'url': '', 'enabled': False},
            'description': 'The third iteration of our test project.',
            'followers': [],
            'jobview': 'subsystem=testproject',
            'members': ['alice', 'bob'],
            'name': 'TestProject 3',
            'owners': ['root', 'admin'],
            'private': False,
            'minimumUpVotes': '2',
            'retainDefaultReviewers': False,
            'subgroups': ['subgroup'],
            'tests': {'url': '', 'enabled': False}
        }
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/projects'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.projects.create(
        'testproject3',
        ['alice', 'bob'],
        subgroups=['subgroup'],
        owners=['root', 'admin'],
        description='The third iteration of our test project.',
        is_private=False,
        deploy_config={'url': '', 'enabled': False},
        tests_config={'url': '', 'enabled': False},
        branches=[{'name': 'Branch One', 'paths': '//depot/main/TestProject/...'}],
        job_view='subsystem=testproject',
        notify_commits=True,
        notify_reviews=True,
        defaults=[{'reviewers': {'user2': {'required': True}}}],
        retain_default_reviewers=False,
        minimum_up_votes='2'
    )

    assert 'project' in response


@responses.activate
def test_edit():
    data = {
        'project': {
            'id': 'testproject3',
            'defaults': [],
            'branches': [{'name': 'Branch One', 'paths': '//depot/main/TestProject/...'}],
            'deleted': False,
            'deploy': {'url': '', 'enabled': False},
            'description': 'The third iteration of our test project.',
            'followers': [],
            'jobview': 'subsystem=testproject',
            'members': ['alice', 'bob'],
            'name': 'TestProject 3',
            'owners': ['root', 'admin'],
            'private': False,
            'minimumUpVotes': '2',
            'retainDefaultReviewers': False,
            'subgroups': ['subgroup'],
            'tests': {'url': '', 'enabled': False}
        }
    }

    responses.add(
        responses.PATCH,
        re.compile(r'.*/api/v\d+/projects/testproject3'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.projects.edit(
        'testproject3',
        name='testproject3',
        members=['alice', 'bob'],
        subgroups=['subgroup'],
        owners=['root', 'admin'],
        description='The third iteration of our test project.',
        is_private=False,
        deploy_config={'url': '', 'enabled': False},
        tests_config={'url': '', 'enabled': False},
        branches=[{'name': 'Branch One', 'paths': '//depot/main/TestProject/...'}],
        job_view='subsystem=testproject',
        notify_commits=True,
        notify_reviews=True,
        defaults=[{'reviewers': {'user2': {'required': True}}}],
        retain_default_reviewers=False,
        minimum_up_votes='2'
    )

    assert 'project' in response


@responses.activate
def test_delete():
    data = {
        'id': 'testproject4'
    }

    responses.add(
        responses.DELETE,
        re.compile(r'.*/api/v\d+/projects/testproject4'),
        json=data
    )

    client = SwarmClient('http://server/api/v2', 'login', 'password')

    response = client.projects.delete('testproject4')
    assert 'id' in response
