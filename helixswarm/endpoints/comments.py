from typing import Dict, List, Optional, Union

from helixswarm.exceptions import SwarmCompatibleError
from helixswarm.helpers import minimal_version


class Comments:

    def __init__(self, swarm):
        self.swarm = swarm

    @minimal_version(3)
    def get(self,
            *,
            after: Optional[int] = None,
            limit: Optional[int] = None,
            topic: Optional[str] = None,
            context_version: Optional[int] = None,
            ignore_archived: Optional[bool] = None,
            tasks_only: Optional[bool] = None,
            task_states: Optional[List[str]] = None,
            fields: Optional[List[str]] = None
            ) -> dict:
        """
        Get list of comments.

        * after: ``int`` (optional)
          A comment ID to seek to. Comments up to and including the specified ID
          are excluded from the results and do not count towards ``limit``.
          Useful for pagination. Commonly set to the ``lastSeen`` property from
          a previous query.

        * limit: ``int`` (optional)
          Maximum number of comments to return. This does not guarantee that
          ``limit`` comments are returned. It does guarantee that the number of
          comments returned won’t exceed ``limit``. Default: 100.

        * topic: ``str`` (optional)
          Only comments for given topic are returned.
          Examples: ``reviews/1234``, ``changes/1234``, ``jobs/job001234``.

        * context_version: ``int`` (optional)
          If a ``reviews/1234`` topic is provided, limit returned comments to a
          specific version of the provided review.

        * ignore_archived: ``bool`` (optional)
          Prevents archived comments from being returned. (**v5+**)

        * task_only: ``bool`` (optional)
          Returns only comments that have been flagged as tasks. (**v5+**)

        * task_states: ``List[str]`` (optional)
          Limit the returned comments to ones that match the provided task state
          Examples: ``open``, ``closed``, ``verified``, or ``comment``. (**v5+**)

        * fields: ``List[str]`` (optional)
          List of fields to show for each comment. Omitting this parameter or
          passing an empty value shows all fields.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        params = dict()  # type: Dict[str, Union[str, int, bool, List[str]]]

        if after:
            params['after'] = after
        if limit:
            params['max'] = limit
        if topic:
            params['topic'] = topic
        if context_version:
            params['context[version]'] = context_version

        if ignore_archived:
            params['ignoreArchived'] = ignore_archived
            if float(self.swarm.version) < 5:
                raise SwarmCompatibleError(
                    'ignore_archived field is supported from API version >= 5'
                )

        if tasks_only:
            params['tasksOnly'] = tasks_only
            if float(self.swarm.version) < 5:
                raise SwarmCompatibleError(
                    'tasks_only field is supported from API version >= 5'
                )

        if task_states:
            params['taskStates'] = task_states
            if float(self.swarm.version) < 5:
                raise SwarmCompatibleError(
                    'task_states field is supported from API version >= 5'
                )

        if fields:
            params['fields'] = ','.join(fields)

        return self.swarm._request('GET', 'comments', params=params)

    @minimal_version(3)
    def add(self,
            topic: str,
            body: str,
            *,
            silence_notification: Optional[bool] = None,
            delay_notification: Optional[bool] = None,
            task_state: Optional[str] = None,
            flags: Optional[List[str]] = None,
            context_file: Optional[str] = None,
            context_left_line: Optional[int] = None,
            context_right_line: Optional[int] = None,
            context_content: Optional[List[str]] = None,
            context_version: Optional[int] = None
            ) -> dict:
        """
        Add a comment to a topic.

        * topic ``str``:
          Examples: ``reviews/1234``, ``changes/1234`` or ``jobs/job001234``.

        * body ``str``:
          Content of the comment, markdown is supported.
          https://www.perforce.com/manuals/swarm/Content/Swarm/basics.markdown.html

          Please note that sometimes message can be rendered incorrectly when
          markdown used then need to strip trailing spaces of message.

        * silence_notification: ``bool`` (optional)
          If true no notifications will ever be sent for this created comment.

        * delay_notification: ``bool`` (optional)
          If true notifications will be delayed.

        * task_state: ``str`` (optional)
          Task state of the comment, valid values when adding a comment are
          ``comment`` and ``open``. This creates a plain comment or opens a task,
          respectively.

        * flags: ``List[str]`` (optional)
          Typically set to ``closed`` to archive a comment.

        * context_file: ``str`` (optional)
          File to comment on. Valid only for changes and reviews topics.
          Example: ``//depot/main/README.txt``

        * context_left_line: ``int`` (optional)
          Left-side diff line to attach the inline comment to. Valid only for
          changes and reviews topics. If this is specified, ``context[file]`` must
          also be specified.

        * context_right_line: ``int`` (optional)
          Right-side diff line to attach the inline comment to. Valid only for
          changes and reviews topics. If this is specified, ``context[file]`` must
          also be specified.

        * context_content: ``List[str]`` (optional)
          Optionally provide content of the specified line and its four preceding
          lines. This is used to specify a short excerpt of context in case the
          lines being commented on change during the review. When not provided,
          Swarm makes an effort to build the content on its own - as this involves
          file operations, it could become slow.

        * context_version: ``int`` (optional)
          With a ``reviews`` topic, this field specifies which version to attach
          the comment to.

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        data = dict(
            topic=topic,
            body=body,
        )  # type: Dict[str, Union[str, int, bool, List[str]]]

        if silence_notification:
            data['silenceNotification'] = 'true'

        if delay_notification:
            data['delayNotification'] = 'true'

        if task_state:
            data['taskState'] = task_state

        if flags:
            data['flags[]'] = flags

        if context_file:
            data['context[file]'] = context_file

        if context_left_line:
            data['context[leftLine]'] = context_left_line

        if context_right_line:
            data['context[rightLine]'] = context_right_line

        if context_content:
            data['context[content]'] = context_content

        if context_version:
            data['context[version]'] = context_version

        return self.swarm._request('POST', 'comments', data=data)

    @minimal_version(3)
    def edit(self,
             comment_id: int,
             body: str,
             *,
             topic: Optional[str] = None,
             task_state: Optional[str] = None,
             flags: Optional[List[str]] = None,
             silence_notification: Optional[bool] = None,
             delay_notification: Optional[bool] = None) -> dict:
        """
        Edit a comment.

        * comment_id:
          ID of the comment to be edited.

        * body:
          Content of the comment.

        * topic: (optional)
          Topic to comment on.
          Examples: ``reviews/1234``, ``changes/1234``, ``jobs/job001234``

        * task_state: ``str`` (optional)
          Task state of the comment. Note that certain transitions (such as
          moving from `open` to ``verified``) are not possible without an intermediate
          step (``addressed``, in this case).
          Examples: ``comment`` (not a task), ``open``, ``addressed``, ``verified``.

        * flags: ``List[str]`` (optional)
          Flags on the comment. Typically set to ``closed`` to archive a comment.

        * silence_notification: ``bool`` (optional)
          If set to '`true'` no notifications will ever be sent for this edited comment.

        * delay_notification: ``bool`` (optional)
          If set to '`true'` notifications will be delayed

        :raises: ``SwarmError``
        :returns: ``dict``
        """
        data = dict(
            body=body,
        )  # type: Dict[str, Union[str, bool, List[str]]]

        if topic:
            data['topic'] = topic

        if task_state:
            data['taskState'] = task_state

        if flags:
            data['flags[]'] = flags

        if silence_notification:
            data['silenceNotification'] = 'true'

        if delay_notification:
            data['delayNotification'] = 'true'

        response = self.swarm._request(
            'PATCH',
            'comments/{}'.format(comment_id),
            data=data,
        )

        return response

    @minimal_version(3)
    def notify(self, topic: str) -> dict:
        """
        Sends notification for comments.

        * topic ``str``:
          This is going to send a single notification for any comments that were
          not notified immediately for the user authenticated for a given topic
          they are posting for. Examples: ``reviews/1234``

        :returns: ``dict``
        :raises: ``SwarmError``
        """
        return self.swarm._request('POST', 'comments', params=dict(topic=topic))
