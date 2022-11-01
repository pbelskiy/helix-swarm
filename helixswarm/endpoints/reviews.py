from typing import Callable, Dict, List, Optional, Tuple, Union

from helixswarm.exceptions import SwarmCompatibleError, SwarmError
from helixswarm.helpers import minimal_version


class Reviews:

    def __init__(self, swarm) -> None:
        self.swarm = swarm

    def get(self,
            *,
            after: Optional[int] = None,
            limit: Optional[int] = None,
            fields: Optional[List[str]] = None,
            authors: Optional[List[str]] = None,
            changes: Optional[List[int]] = None,
            has_reviewers: Optional[bool] = None,
            ids: Optional[List[int]] = None,
            keywords: Optional[str] = None,
            participants: Optional[List[str]] = None,
            projects: Optional[List[str]] = None,
            states: Optional[List[str]] = None,
            passes_tests: Optional[bool] = None,
            not_updated_since: Optional[str] = None,
            has_voted: Optional[str] = None,
            my_comments: Optional[bool] = None
            ) -> dict:
        """
        Get list of available reviews.

        Args:
            after (Optional[int]):
                A review ID to seek to. Reviews up to and including the specified
                `id` are excluded from the results and do not count towards `limit`.
                Useful for pagination. Commonly set to the `lastSeen` property
                from a previous query.

            limit (Optional[int]):
                Maximum number of reviews to return. This does not guarantee that
                `limit` reviews are returned. It does guarantee that the number
                of reviews returned won't exceed `limit`. Server-side filtering
                may exclude some reviews for permissions reasons.

                Default: `1000`

            fields (Optional[List[str]):
                Fields to show, Omitting this parameter or passing an empty value
                shows all fields.

            author (Optional[List[str]):
                One or more authors to limit reviews by. Reviews with any of the
                specified authors are returned. (**API v1.2+**)

            changes (Optional[List[str]):
                One or more change IDs to limit reviews by. Reviews associated
                with any of the specified changes are returned.

            has_reviewers (Optional[bool):
                Limit reviews list to those with or without reviewers.

            ids (Optional[List[int]):
                One or more review IDs to fetch. Only the specified reviews are
                returned. This filter cannot be combined with the `limit`
                parameter.

            keywords (Optional[str]):
                Keywords to limit reviews by. Only reviews where the description,
                participants list or project list contain the specified keywords
                are returned.

            participants (Optional[List[str]):
                One or more participants to limit reviews by. Reviews with any
                of the specified participants are returned.

            projects (Optional[List[str]):
                One or more projects to limit reviews by. Reviews affecting any
                of the specified projects are returned.

            states (Optional[List[str]):
                One or more states to limit reviews by. Reviews in any of the
                specified states are returned.

            passes_tests (Optional[bool]):
                Option to limit reviews by tests passing or failing.

            not_updated_since (Optional[str]):
                Option to fetch unchanged reviews. Requires the date to be in
                the format `YYYY-mm-dd`, for example 2017-01-01. Reviews to be
                returned are determined by looking at the last updated date of
                the review.

            has_voted (Optional[str]):
                Should have the value ``up`` or ``down`` to filter reviews that
                have been voted up or down by the current authenticated user.

            my_comments (Optional[bool]):
                Filtering reviews that include comments by the current authenticated user.

        Returns:
            dict: json response.
        """
        params = dict()  # type: Dict[str, Union[int, str, bool, List[str], List[int]]]

        if after:
            params['after'] = after

        if limit:
            params['max'] = limit

        if fields:
            params['fields'] = ','.join(fields)

        if authors:
            params['author'] = authors
            if float(self.swarm.version) < 2:
                raise SwarmCompatibleError(
                    'author field is supported from API version >= 2'
                )

        if changes:
            params['change'] = changes

        if has_reviewers is not None:
            params['hasReviewers'] = has_reviewers

        if ids:
            params['ids'] = ids

        if keywords:
            params['keywords'] = keywords

        if participants:
            params['participants'] = participants

        if projects:
            params['project'] = projects

        if states:
            params['state'] = states

        if passes_tests is not None:
            params['passesTests'] = passes_tests

        if not_updated_since:
            params['notUpdatedSince'] = not_updated_since

        if has_voted:
            params['hasVoted'] = has_voted

        if my_comments is not None:
            params['myComments'] = my_comments

        return self.swarm._request('GET', 'reviews', params=params)

    @minimal_version(6)
    def get_for_dashboard(self) -> dict:
        """
        Gets reviews for the action dashboard for the authenticated user

        Returns:
            dict: json response.
        """
        return self.swarm._request('GET', 'dashboards/action')

    def _get_info(self,
                  review_id: int,
                  fields: Optional[List[str]] = None,
                  callback: Optional[Callable] = None
                  ) -> dict:
        """
        Retrieve information about a review.

        Args:
            review_id (int):
                Review id getting information from.

            fields (Optional[List[str]]):
                List of fields to show. Omitting this parameter or passing an
                empty value shows all fields.

            callback (Optional[Callable]):
                Function callback for support both sync and async syntax.

        Returns:
            dict: json response.
        """
        params = dict()  # type: Dict[str, str]

        if fields:
            params['fields'] = ','.join(fields)

        response = self.swarm._request(
            'GET',
            'reviews/{}'.format(review_id),
            fcb=callback,
            params=params
        )

        return response

    def get_info(self,
                 review_id: int,
                 *,
                 fields: Optional[List[str]] = None
                 ) -> dict:
        """
        Retrieve information about a review.

        Args:
            review_id (int):
                Review id getting information from.

            fields (Optional[List[str]]):
                List of fields to show. Omitting this parameter or passing an
                empty value shows all fields.

        Returns:
            dict: json response.
        """
        return self._get_info(review_id, fields)

    @minimal_version(9)
    def get_transitions(self,
                        review_id: int,
                        *,
                        up_voters: Optional[str] = None
                        ) -> dict:
        """
        Get transitions for a review (**v9+**)

        Args:
            review_id: ``int``
                Review id getting information from.

            up_voters  (Optional[str]):
                A list of users whose vote up will be assumed when determining
                the transitions. For example if a user has not yet voted but
                would be the last required vote and asked for possible transitions
                we would want to include 'approve'

        Returns:
            dict: json response.
        """
        params = dict()

        if up_voters:
            params['upVoters'] = up_voters

        response = self.swarm._request(
            'GET',
            'reviews/{}/transitions'.format(review_id),
            params=params
        )

        return response

    def get_latest_revision_and_change(self, review_id: int) -> Tuple[int, int]:
        """
        Get latest revision and change (changelist) for a review.

        Args:
            review_id (int):
                Review id getting information from.

        Returns:
            Tuple[int, int]: revision and change respectively.
        """
        def callback(response: dict) -> Tuple[int, int]:
            review = response.get('review')

            if review is None or 'versions' not in review:
                raise SwarmError('can`t find `versions` field in review data')

            latest_revision = len(review['versions'])
            if latest_revision == 0:
                raise SwarmError('can`t get review revision, `versions` is empty')

            latest_version = review['versions'][-1]
            if 'change' not in latest_version:
                raise SwarmError('no `change` field in latest versions block')

            latest_change = int(latest_version['change'])
            return latest_revision, latest_change

        response = self._get_info(
            review_id,
            fields=['versions'],
            callback=callback
        )

        return response  # type: ignore

    def create(self,
               change: int,
               *,
               description: Optional[str] = None,
               reviewers: Optional[List[str]] = None,
               required_reviewers: Optional[List[str]] = None,
               reviewer_groups: Optional[List[str]] = None
               ) -> dict:
        """
        Create a review.

        Args:
            fields (int):
                Change ID to create a review from.

            description (Optional[str]):
                Description for the new review (defaults to change description).

            reviewers (Optional[List[str]]):
                A list of reviewers for the new review.

            required_reviewers (Optional[List[str]]):
                A list of required reviewers for the new review (**v1.1+**)

            reviewer_groups (Optional[List[str]]):
                A list of required reviewers for the new review (**v7+**)

        Returns:
            dict: json response.
        """
        data = dict(change=change)  # type: Dict[str, Union[int, str, List[str]]]

        if description:
            data['description'] = description

        if reviewers:
            data['reviewers'] = reviewers

        if required_reviewers:
            data['requiredReviewers'] = required_reviewers
            if float(self.swarm.version) == 1:
                raise SwarmCompatibleError(
                    'required_reviewers field is supported from API version > 1'
                )

        if reviewer_groups:
            data['reviewerGroups'] = reviewer_groups
            if float(self.swarm.version) < 7:
                raise SwarmCompatibleError(
                    'reviewer_groups field is supported from API version > 6'
                )

        return self.swarm._request('POST', 'reviews', json=data)

    @minimal_version(9)
    def vote(self,
             review_id: int,
             vote: str,
             *,
             version: Optional[str] = None
             ) -> dict:
        """
        Set the vote for the authenticated user to be up, down or cleared.

        Args:
            review_id (int):
                Review ID.

            vote (str):
                Valid votes are `up`, `down` and `clear`.

            version (Optional[str]):
                Expected to be a valid review revision to vote on if supplied,
                ignored if the revision does not exist and the vote will apply
                to the latest revision.

        Returns:
            dict: json response.
        """
        data = dict()  # type: Dict[str, str]

        if vote:
            data['vote[value]'] = vote

        if version:
            data['vote[version]'] = version

        response = self.swarm._request(
            'POST',
            'reviews/{}/vote'.format(review_id),
            data=data
        )

        return response

    def add_change(self,
                   review_id: int,
                   change: int,
                   *,
                   mode: Optional[str] = None
                   ) -> dict:
        """
        Add change to a review, links the given change to the review and
        schedules an update.

        Args:
            review_id (int):
                Review ID.

            change (int):
                Change ID.

            mode (str):
                The mode of operation, currently ]replace` or `append`.

        Returns:
            dict: json response.
        """
        data = dict(
            change=change,
        )  # type: Dict[str, Union[str, int]]

        if mode:
            data['mode'] = mode

        response = self.swarm._request(
            'POST',
            'reviews/{}/changes/'.format(review_id),
            data=data
        )

        return response

    @minimal_version(6)
    def archive(self,
                *,
                not_updated_since: str,
                description: str
                ) -> dict:
        """
        Archiving the inactive reviews (**v6+**).

        Args:
            not_updated_since (str):
                Updated since date. Requires the date to be in the format
                `YYYY-mm-dd`

                Example: `2017-01-01`

            description (str):
                A description that is posted as a comment for archiving.

        Returns:
            dict: json response.
        """
        data = dict(
            notUpdatedSince=not_updated_since,
            description=description
        )

        return self.swarm._request('POST', 'reviews/archive', data=data)

    def update(self,
               review_id: int,
               *,
               author: Optional[str] = None,
               description: Optional[str] = None
               ) -> dict:
        """
        Archiving the inactive reviews (**v6+**).

        Args:
            review_id (int):
                Review ID.

            author (Optional[str]):
                The new author for the specified review.

            description (Optional[str]):
                The new description for the specified review.

        Returns:
            dict: json response.
        """
        if author is description is None:
            raise SwarmError('At least one of description or author are required')

        data = dict()  # type: Dict[str, str]

        if author:
            data['author'] = author
        if description:
            data['description'] = description

        response = self.swarm._request(
            'PATCH',
            'reviews/{}'.format(review_id),
            data=data
        )

        return response

    @minimal_version(6)
    def cleanup(self,
                review_id: int,
                *,
                reopen: Optional[bool] = None
                ) -> dict:
        """
        Clean up a review for the given id (**v6+**).

        Args:
            review_id (int):
                Review id getting information from.

            reopen (Optional[bool]):
                Expected to be a boolean (defaulting to false). If true then an
                attempt will be made to reopen files into a default changelist

        Returns:
            dict: json response.
        """
        data = dict()

        if reopen:
            data['reopen'] = reopen

        response = self.swarm._request(
            'POST',
            'reviews/{}/cleanup'.format(review_id),
            data=data
        )

        return response

    @minimal_version(9)
    def obliterate(self, review_id: int) -> dict:
        """
        Obliterate a review for the given id (**v9+**).

        Args:
            review_id (int):
                Review id getting information from.

        Returns:
            dict: json response.
        """
        response = self.swarm._request(
            'POST',
            'reviews/{}/obliterate'.format(review_id)
        )

        return response
