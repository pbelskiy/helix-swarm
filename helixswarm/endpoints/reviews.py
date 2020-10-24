class Reviews:

    def __init__(self, swarm):
        self.swarm = swarm

    def get_all(self) -> dict:
        """
        Get List of Reviews
        """
        return self.swarm._request('GET', 'reviews')

    def get(self, review_id: int) -> dict:
        """
        Retrieve information about a review.
        """
        return self.swarm._request('GET', 'reviews/{}'.format(review_id))

    def create(self) -> None:
        return self.swarm._request('POST', 'reviews')
