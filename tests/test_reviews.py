import re

import pytest
import responses

from helixswarm import SwarmClient, SwarmCompatibleError, SwarmNotFoundError


@responses.activate
def test_reviews_all():
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

    reviews = client.reviews.get_all()
    assert len(reviews['reviews']) == 1


@responses.activate
def test_reviews_all_parameters():
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

    reviews = client.reviews.get_all(
        limit=2,
        fields=['id', 'description', 'author', 'state']
    )

    assert len(reviews['reviews']) == 2


def test_reviews_all_exceptions():
    client = SwarmClient('http://server/api/v1.2', 'login', 'password')

    # >= 2 API versions needed
    with pytest.raises(SwarmCompatibleError):
        client.reviews.get_all(authors=['p.belskiy'])


@responses.activate
def test_get_review_info():
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

    reviews = client.reviews.get(12204, fields=fields)
    assert reviews['review']['id'] == 12204


@responses.activate
def test_get_review_info_error():
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
        client.reviews.get(12345)
