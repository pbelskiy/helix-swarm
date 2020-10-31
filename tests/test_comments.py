import re

import pytest
import responses

from helixswarm import SwarmClient, SwarmCompatibleError


@responses.activate
def test_comments_get():
    data = {
        'topic': 'reviews/911',
        'comments': {
            '35': {
                'id': 35,
                'body': 'Excitation thunder cats intelligent man braid organic bitters.',
                'time': 1461164347,
                'user': 'bruno'
            },
            '39': {
                'id': 39,
                'body': 'Chamber tote bag butcher, shirk truffle mode shabby chic single-origin coffee.',
                'time': 1461164347,
                'user': 'swarm_user'
            }
        },
        'lastSeen': 39
    }

    responses.add(responses.GET, re.compile(r'.*/comments'), json=data)

    client = SwarmClient('http://server/api/v9', 'login', 'password')
    response = client.comments.get(
        topic='reviews/911',
        limit=2,
        fields=['id', 'body', 'time', 'user']
    )

    assert response['topic'] == 'reviews/911'


def test_comments_get_exception():
    client = SwarmClient('http://server/api/v4', 'login', 'password')

    with pytest.raises(SwarmCompatibleError):
        client.comments.get(ignore_archived=True)

    with pytest.raises(SwarmCompatibleError):
        client.comments.get(tasks_only=True)

    with pytest.raises(SwarmCompatibleError):
        client.comments.get(task_states=['open'])


@responses.activate
def test_comments_add():
    data = {
        'comment': {
            'id': 42,
            'attachments': [],
            'body': 'Best. Comment. EVER!',
            'context': [],
            'edited': None,
            'flags': [],
            'likes': [],
            'taskState': 'comment',
            'time': 123456789,
            'topic': 'reviews/2',
            'updated': 123456790,
            'user': 'bruno'
        }
    }

    responses.add(responses.POST, re.compile(r'.*\/comments'), json=data)

    client = SwarmClient('http://server/api/v9', 'login', 'password')
    response = client.comments.add('reviews/123', 'Best. Comment. EVER!')
    assert response['comment']['body'] == 'Best. Comment. EVER!'


def test_comments_add_old_api():
    client = SwarmClient('http://server/api/v2', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.comments.add('reviews/123', 'Best. Comment. EVER!')


@responses.activate
def test_comments_edit():
    data = {
        'comment': {
            'id': 1,
            'attachments': [],
            'body': 'Edited comment',
            'context': [],
            'edited': 123466790,
            'flags': ['closed'],
            'likes': [],
            'taskState': 'comment',
            'time': 123456789,
            'topic': 'reviews/42',
            'updated': 123456790,
            'user': 'bruno'
        }
    }

    responses.add(responses.PATCH, re.compile(r'.*\/comments/123'), json=data)

    client = SwarmClient('http://server/api/v8', 'login', 'password')
    response = client.comments.edit(123, 'Edited comment', flags=['closed'])
    assert response['comment']['body'] == 'Edited comment'
    assert 'closed' in response['comment']['flags']


def test_comments_edit_old_api():
    client = SwarmClient('http://server/api/v1', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.comments.edit(123, 'Edited comment')


@responses.activate
def test_comments_notify():
    data = {
        'isValid': True,
        'message': 'No comment notifications to send',
        'code': 200
    }

    responses.add(responses.POST, re.compile(r'.*\/comments'), json=data)

    client = SwarmClient('http://server/api/v9', 'login', 'password')
    response = client.comments.notify('reviews/911')
    assert response['isValid'] is True
