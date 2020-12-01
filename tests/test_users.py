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
