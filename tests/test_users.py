import re

import responses

from helixswarm import SwarmClient


@responses.activate
def test_get():
    data_1 = [
        {
            'User': 'bruno',
            'FullName': 'Bruno First'
        },
        {
            'User': 'super',
            'FullName': 'Super Second'
        }
    ]

    data_2 = {
        'isValid': False,
        'messages': 'No such group'
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/users'),
        json=data_1
    )

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/users'),
        json=data_2
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.users.get(
        fields=['User', 'FullName'],
        users=['super', 'bruno'],
    )

    assert len(response) > 0

    response = client.users.get(
        group='none'
    )

    assert response['isValid'] is False


@responses.activate
def test_unfollow_all():
    data = {
        'isValid': True,
        'messages': 'User p.belskiy is no longer following any Projects or Users.'
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/users/p.belskiy/unfollowall'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.users.unfollow_all('p.belskiy')

    assert 'messages' in response
