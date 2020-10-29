from typing import Dict, List, Optional


class Reviews:

    def __init__(self, swarm):
        self.swarm = swarm

    def get_all(self) -> dict:
        """
        Get List of Reviews
        """
        return self.swarm._request('GET', 'reviews')

    def get(self, review_id: int, *, fields: Optional[List[str]] = None) -> dict:
        """
        Retrieve information about a review.

        * fields: ``List[str]`` (optional)
          List of fields to show. Omitting this parameter or passing an empty
          value shows all fields.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, str]

        if fields:
            params['fields'] = ','.join(fields)

        response = self.swarm._request(
            'GET',
            'reviews/{}'.format(review_id),
            params=params
        )

        return response

    def create(self) -> None:
        return self.swarm._request('POST', 'reviews')
