from typing import Dict, List, Optional, Union


class Activities:

    def __init__(self, swarm):
        self.swarm = swarm

    def get(self,
            *,
            change: Optional[int] = None,
            stream: Optional[str] = None,
            category: Optional[str] = None,
            after: Optional[int] = None,
            limit: Optional[int] = None,
            fields: Optional[List[str]] = None
            ) -> dict:
        """
        Retrieve the activity list.

        * change: ``int`` (optional)
          Filter activity entries by associated changelist id. This only includes
          records for which there is an activity entry in Swarm.

        * stream: ``str`` (optional)
          Filter activity stream to query for entries. This can include
          user-initiated actions (``user-alice``), activity relating to a user’s
          followed projects/users (``personal-alice``), review streams
          (``review-1234``), and project streams (``project-exampleproject``).

        * category: ``str`` (optional)
          Type of activity, examples: ``change``, ``comment``, ``job``, ``review``.

        * after: ``int`` (optional)
          An activity ID to seek to. Activity entries up to and including the
          specified ID are excluded from the results and do not count towards ``limit``.
          Useful for pagination. Commonly set to the ``lastSeen`` property from a
          previous query.

        * limit: ``int`` (optional)
          Maximum number of activity entries to return. This does not guarantee
          that ``limit`` entries are returned. It does guarantee that the number
          of entries returned won’t exceed ``limit``. Server-side filtering may
          exclude some activity entries for permissions reasons. Default: 100

        * fields: ``List[str]`` (optional)
          List of fields to show. Omitting this parameter or passing an empty
          value shows all fields.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, Union[int, str]]

        if change:
            params['change'] = change
        if stream:
            params['stream'] = stream
        if category:
            params['type'] = category
        if after:
            params['after'] = after
        if limit:
            params['max'] = limit
        if fields:
            params['fields'] = ','.join(fields)

        return self.swarm._request('GET', 'activity', params=params)

    def create(self,
               *,
               category: str,
               user: str,
               action: str,
               target: str,
               topic: Optional[str] = None,
               description: Optional[str] = None,
               change: Optional[int] = None,
               streams: Optional[List[str]] = None,
               link: Optional[str] = None
               ) -> dict:
        """
        Retrieve the activity list.

        * category: ``str``
          Type of activity, used for filtering activity streams.
          Values can include ``change``, ``comment``, ``job``, ``review``).

        * user: ``str``
          User who performed the action.

        * action: ``str``
          Action that was performed - past-tense, for example, ``created``,
          ``commented on``.

        * target: ``str``
          Target that the action was performed on, for example, ``issue 1234``.

        * topic: ``str``
          Topic for the activity entry. Topics are essentially comment thread IDs.
          Examples: ``reviews/1234`` or ``jobs/job001234``.

        * description: ``str``
          Optional description of object or activity to provide context.

        * change: ``int``
          Optional changelist ID this activity is related to.
          Used to filter activity related to restricted changes.

        * streams: ``List[str]``
          Optional array of streams to display on. This can include user-initiated
          actions (``user-alice``), activity relating to a user’s followed
          projects/users (``personal-alice``), review streams (``review-1234``)
          and project streams (``project-exampleproject``).

        * link: ``str``
          Optional URL for ``target``.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        data = dict()  # type: Dict[str, Union[int, str, List[str]]]

        if category:
            data['type'] = category
        if user:
            data['user'] = user
        if action:
            data['action'] = action
        if target:
            data['target'] = target
        if topic:
            data['topic'] = topic
        if description:
            data['description'] = description
        if change:
            data['change'] = change
        if streams:
            data['streams'] = streams
        if link:
            data['link'] = link

        return self.swarm._request('POST', 'activity', data=data)
