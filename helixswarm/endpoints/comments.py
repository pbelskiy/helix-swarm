from typing import Dict, List, Optional, Union

from helixswarm.exceptions import SwarmCompatibleError


class Comments:

    def __init__(self, swarm):
        self.swarm = swarm

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
        if self.swarm.api_version < 3:
            raise SwarmCompatibleError('Comments supported from API version >= 3')

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
        if self.swarm.api_version < 3:
            raise SwarmCompatibleError('Comments supported from API version >= 3')

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
