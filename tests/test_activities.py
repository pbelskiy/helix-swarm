import re

import responses

from helixswarm import SwarmClient


@responses.activate
def test_activity_get():
    data = {
        'activity': [
            {
                'id': 619,
                'action': 'updated files in',
                'behalfOf': None,
                'behalfOfExists': False,
                'behalfOfFullName': '',
                'change': 290,
                'date': '2019-01-23T02:46:59-08:00',
                'depotFile': None,
                'description': 'Start of Project Blue Book.',
                'target': 'review 290 (revision 2)',
                'time': 1548240419,
                'topic': 'reviews/290',
                'type': 'review',
                'url': '/main/reviews/290/v2/',
                'user': 'allison.clayborne',
                'userExists': True,
                'userFullName': 'Allison Clayborne'
            }
        ],
        'lastSeen': 618
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/activity?.*'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.activities.get(
        change=290,
        stream='review-290',
        category='review',
        after=600,
        limit=1,
        fields=[
            'id', 'action', 'behalfOf', 'behalfOfExists', 'behalfOfFullName',
            'change', 'date', 'depotFile', 'description', 'target', 'time',
            'topic', 'type', 'url', 'user', 'userExists', 'userFullName'
        ]
    )

    assert 'activity' in response
