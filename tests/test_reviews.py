import re

import pytest
import responses

from aioresponses import aioresponses

from helixswarm import (
    SwarmAsyncClient,
    SwarmClient,
    SwarmCompatibleError,
    SwarmError,
    SwarmNotFoundError,
)


@pytest.fixture
def aiohttp_mock():
    with aioresponses() as mock:
        yield mock


@responses.activate
def test_get():
    data = {
        'lastSeen': 12209,
        'reviews': [
            {
                'id': 12206,
                'author': 'swarm',
                'changes': [12205],
                'comments': 0,
                'commits': [],
                'commitStatus': [],
                'created': 1402507043,
                'deployDetails': [],
                'deployStatus': None,
                'description': 'Review Description\n',
                'participants': {
                    'swarm': []
                },
                'pending': True,
                'projects': [],
                'state': 'needsReview',
                'stateLabel': 'Needs Review',
                'testDetails': [],
                'testStatus': None,
                'type': 'default',
                'updated': 1402518492
            }
        ],
        'totalCount': 1
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews'),
        json=data
    )

    client = SwarmClient('http://server/api/v1', 'login', 'password')

    reviews = client.reviews.get(ids=[12206])
    assert len(reviews['reviews']) == 1


@responses.activate
def test_get_parameters():
    data = {
        'lastSeen': 120,
        'reviews': [
            {
                'id': 123,
                'author': 'bruno',
                'description': 'Adding .jar that should have been included in r110\n',
                'state': 'needsReview'
            },
            {
                'id': 120,
                'author': 'bruno',
                'description': 'Fixing a typo.\n',
                'state': 'needsReview'
            }
        ],
        'totalCount': None
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    reviews = client.reviews.get(
        after=60,
        limit=2,
        fields=['id', 'description', 'author', 'state'],
        changes=[123, 456],
        has_reviewers=True,
        keywords='bruno',
        participants=['bruno'],
        projects=['test'],
        states=['needsReview'],
        passes_tests=True,
        not_updated_since='2017-02-15',
        has_voted=True,
        my_comments=True,
    )

    assert len(reviews['reviews']) == 2


def test_get_exceptions():
    client = SwarmClient('http://server/api/v1.2', 'login', 'password')

    # >= 2 API versions needed
    with pytest.raises(SwarmCompatibleError):
        client.reviews.get(authors=['p.belskiy'])


@responses.activate
def test_get_info():
    data = {
        'review': {
            'id': 12204,
            'author': 'bruno',
            'changes': [10667],
            'commits': [10667],
            'commitStatus': [],
            'created': 1399325913,
            'deployDetails': [],
            'deployStatus': None,
            'description': 'Adding .jar that should have been included in r10145\n',
            'participants': {
                'alex_qc': [],
                'bruno': {
                    'vote': 1,
                    'required': True
                },
                'vera': []
            },
            'reviewerGroups': {
                'group1': [],
                'group2': {
                    'required': True
                },
                'group3': {
                    'required': True,
                    'quorum': '1'
                }
            },
            'pending': False,
            'projects': {
                'swarm': ['main']
            },
            'state': 'archived',
            'stateLabel': 'Archived',
            'testDetails': {
                'url': 'http://jenkins.example.com/job/project_ci/123/'
            },
            'testStatus': None,
            'type': 'default',
            'updated': 1399325913
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12204.*'),
        json=data
    )

    client = SwarmClient('http://server/api/v1', 'login', 'password')

    fields = [
        'id', 'author', 'changes', 'commits', 'commitStatus', 'created',
        'deployDetails', 'deployStatus', 'description', 'participants',
        'reviewerGroups', 'pending', 'projects', 'state', 'stateLabel',
        'testDetails', 'testStatus', 'type', 'updated'
    ]

    reviews = client.reviews.get_info(12204, fields=fields)
    assert reviews['review']['id'] == 12204


@responses.activate
def test_get_info_error():
    data = {
        'error': 'Not Found'
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12345'),
        json=data,
        status=404
    )

    client = SwarmClient('http://server/api/v1', 'login', 'password')
    with pytest.raises(SwarmNotFoundError):
        client.reviews.get_info(12345)


@responses.activate
def test_get_dashboards():
    data = {
        'lastSeen': 120,
        'reviews': [
            {
                'id': 7,
                'author': 'swarm_admin',
                'changes': [6],
                'comments': [0, 0],
                'commits': [6],
                'commitStatus': [],
                'created': 1485793976,
                'deployDetails': [],
                'deployStatus': None,
                'description': 'test\n',
                'groups': ['swarm-project-test'],
                'participants': {'swarm_admin': []},
                'pending': False,
                'projects': {'test': ['test']},
                'roles': ['moderator|reviewer|required_reviewer|author'],
                'state': 'needsReview',
                'stateLabel': 'Needs Review',
                'testDetails': [],
                'testStatus': None,
                'type': 'default',
                'updated': 1485958875,
                'updateDate': '2017-02-01T06:21:15-08:00'
            }
        ],
        'totalCount': None
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/dashboards/action'),
        json=data
    )

    client = SwarmClient('http://server/api/v6', 'login', 'password')

    response = client.reviews.get_for_dashboard()
    assert 'reviews' in response


@responses.activate
def test_get_transitions():
    data = {
        'isValid': 'true',
        'transitions': {
            'needsRevision': 'Needs Revision',
            'approved': 'Approve',
            'approved:commit': 'Approve and Commit',
            'rejected': 'Reject',
            'archived': 'Archive'
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12345/transitions'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')
    response = client.reviews.get_transitions(
        12345,
        up_voters='bruno'
    )
    assert 'transitions' in response

    client = SwarmClient('http://server/api/v8', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.reviews.get_transitions(12345)


@responses.activate
def test_get_latest_revision_and_change():
    client = SwarmClient('http://server/api/v9', 'login', 'password')

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12345'),
        json={'review': {
            'versions': [
                {'change': 1},
                {'change': 2, 'archiveChange': 3}
            ]
        }},
        status=200
    )

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/555'),
        json={'review': {
            'versions': [
                {'change': 7}
            ]
        }},
        status=200
    )

    revision, change = client.reviews.get_latest_revision_and_change(12345)
    assert revision == 2
    assert change == 3

    revision, change = client.reviews.get_latest_revision_and_change(555)
    assert revision == 1
    assert change == 7


@pytest.mark.asyncio
async def test_get_latest_revision_and_change_async(aiohttp_mock):
    client = SwarmAsyncClient('http://server/api/v9', 'login', 'password')

    aiohttp_mock.get(
        re.compile(r'.*/api/v\d+/reviews/12345'),
        payload={
            'review': {
                'versions': [
                    {'change': 1},
                    {'change': 2, 'archiveChange': 3}
                ]
            }
        },
    )

    revision, change = await client.reviews.get_latest_revision_and_change(12345)
    assert revision == 2
    assert change == 3

    await client.close()


@responses.activate
def test_get_latest_revision_and_change_exception():
    client = SwarmClient('http://server/api/v9', 'login', 'password')

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12345'),
        json={'review': {}},
        status=200
    )

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12345'),
        json={'review': {'versions': []}},
        status=200
    )

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12345'),
        json={'review': {
            'versions': [
                {'change': 1},
                {'archiveChange': 3}
            ]
        }},
        status=200
    )

    with pytest.raises(SwarmError):
        client.reviews.get_latest_revision_and_change(12345)

    with pytest.raises(SwarmError):
        client.reviews.get_latest_revision_and_change(12345)

    with pytest.raises(SwarmError):
        client.reviews.get_latest_revision_and_change(12345)


@responses.activate
def test_create():
    data = {
        'review': {
            'id': 12205,
            'author': 'bruno',
            'changes': [10667],
            'commits': [10667],
            'commitStatus': [],
            'created': 1399325913,
            'deployDetails': [],
            'deployStatus': None,
            'description': 'My awesome description',
            'participants': {
                'bruno': []
            },
            'reviewerGroups': {
                'group1': [],
                'group2': {
                    'required': True
                },
                'group3': {
                    'required': True,
                    'quorum': '1'
                }
            },
            'pending': False,
            'projects': [],
            'state': 'archived',
            'stateLabel': 'Archived',
            'testDetails': [],
            'testStatus': None,
            'type': 'default',
            'updated': 1399325913
        }
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.create(
        10667,
        description='My awesome description',
        reviewers=['p.belskiy']
    )

    assert 'review' in response


def test_create_exception():
    client_v1 = SwarmClient('http://server/api/v1', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client_v1.reviews.create(111, required_reviewers=['p.belskiy'])

    client_v6 = SwarmClient('http://server/api/v6', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client_v6.reviews.create(222, reviewer_groups=['master'])


@responses.activate
def test_add_change():
    data = {
        'review': {
            'id': 123,
            'author': 'bruno',
            'changes': [122, 124],
            'commits': [],
            'commitStatus': [],
            'created': 1399325913,
            'deployDetails': [],
            'deployStatus': None,
            'description': 'Adding .jar that should have been included in r110\n',
            'groups': [],
            'participants': {
                'bruno': []
            },
            'pending': True,
            'projects': [],
            'state': 'needsReview',
            'stateLabel': 'Needs Review',
            'testDetails': [],
            'testStatus': None,
            'type': 'default',
            'updated': 1399325913,
            'versions': [
                {
                    'difference': 1,
                    'stream': None,
                    'change': 124,
                    'user': 'bruno',
                    'time': 1399330003,
                    'pending': True,
                    'archiveChange': 124
                }
            ]
        }
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews/12345/changes'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.add_change(
        12345,
        change=124,
        mode='append'
    )

    assert 'review' in response


@responses.activate
def test_update():
    data = {
        'review': {
            'id': 12306,
            'author': 'swarm',
            'changes': [12205],
            'comments': 0,
            'commits': [],
            'commitStatus': [],
            'created': 1402507043,
            'deployDetails': [],
            'deployStatus': None,
            'description': 'Updated Review Description\n',
            'participants': {
                'swarm': []
            },
            'pending': True,
            'projects': [],
            'state': 'needsReview',
            'stateLabel': 'Needs Review',
            'testDetails': [],
            'testStatus': None,
            'type': 'default',
            'updated': 1402518492
        },
        'transitions': {
            'needsRevision': 'Needs Revision',
            'approved': 'Approve',
            'rejected': 'Reject',
            'archived': 'Archive'
        },
        'canEditAuthor': True
    }

    responses.add(
        responses.PATCH,
        re.compile(r'.*/api/v\d+/reviews/12306'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.update(
        12306,
        author='new_author',
        description='new_description'
    )

    assert 'review' in response

    with pytest.raises(SwarmError):
        client.reviews.update(12306)


@responses.activate
def test_vote():
    data = {
        'isValid': 'true',
        'messages': ['User username set vote to up on review 1']
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews/12345/vote'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.vote(
        12345,
        vote='up',
        version='1'
    )

    assert 'messages' in response


@responses.activate
def test_archive():
    data = {
        'archivedReviews': [
            {
                'id': 911,
                'author': 'swarm',
                'changes': [601],
                'commits': [],
                'commitStatus': [],
                'created': 1461164344,
                'deployDetails': [],
                'deployStatus': None,
                'description': 'Touch up references on html pages.\n',
                'groups': [],
                'participants': {
                    'swarm': []
                },
                'pending': False,
                'projects': [],
                'state': 'archived',
                'stateLabel': 'Archived',
                'testDetails': [],
                'testStatus': None,
                'type': 'default',
                'updated': 1478191605
            },
            {
                'id': 908,
                'author': 'earl',
                'changes': [605],
                'commits': [],
                'commitStatus': [],
                'created': 1461947794,
                'deployDetails': [],
                'deployStatus': None,
                'description': 'Remove (attempted) installation of now deleted man pages.\n',
                'groups': [],
                'participants': {
                    'swarm': []
                },
                'pending': False,
                'projects': [],
                'state': 'archived',
                'stateLabel': 'Archived',
                'testDetails': [],
                'testStatus': None,
                'type': 'default',
                'updated': 1478191605
            }
        ],
        'failedReviews': [
            {}
        ]
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews/archive'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.archive(
        not_updated_since='2016-06-30',
        description='My awesome description'
    )

    assert 'archivedReviews' in response

    client = SwarmClient('http://server/api/v5', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.reviews.archive(
            not_updated_since='2016-06-30',
            description='My awesome description'
        )


@responses.activate
def test_cleanup():
    data = {
        'complete': [
            {
                '1': ['2']
            }
        ],
        'incomplete': []
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews/12345/cleanup'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.cleanup(12345, reopen=True)
    assert 'complete' in response

    client = SwarmClient('http://server/api/v5', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.reviews.cleanup(12345)


@responses.activate
def test_obliterate():
    data = {
        'isValid': True,
        'message': 'review 1 has been Obliterated',
        'code': 200
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews/12345/obliterate'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.obliterate(12345)
    assert 'message' in response

    client = SwarmClient('http://server/api/v8', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.reviews.obliterate(12345)
