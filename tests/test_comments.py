import re

import pytest
import responses

from helixswarm import Swarm, SwarmCompatibleError


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

    client = Swarm('http://server/api/v9', 'login', 'password')
    response = client.comments.add('reviews/123', 'Best. Comment. EVER!')
    assert response['comment']['body'] == 'Best. Comment. EVER!'


def test_comments_add_old_api():
    client = Swarm('http://server/api/v2', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.comments.add('reviews/123', 'Best. Comment. EVER!')
