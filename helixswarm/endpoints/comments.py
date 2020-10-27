from typing import Any, Dict, List, Optional

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

        Method will raise :class:`SwarmException` on failure.

        :param topic:
            Examples: reviews/1234, changes/1234 or jobs/job001234.
        :param body:
            Content of the comment, markdown is supported.
            https://www.perforce.com/manuals/swarm/Content/Swarm/basics.markdown.html

            Please note that sometimes message can be rendered incorrectly when
            markdown used then need to strip trailing spaces of message.
        :param silence_notification: (optional)
            If true no notifications will ever be sent for this created comment.
        :param delay_notification: (optional)
            If true notifications will be delayed.
        :param task_state: (optional)
            Task state of the comment, valid values when adding a comment are
            `comment` and `open`. This creates a plain comment or opens a task,
            respectively.
        :param flags: (optional)
            Typically set to `closed` to archive a comment.
        :param context_file: (optional)
            File to comment on. Valid only for changes and reviews topics.
            Example: //depot/main/README.txt.
        :param context_left_line: (optional)
            Left-side diff line to attach the inline comment to. Valid only for
            changes and reviews topics. If this is specified, context[file] must
            also be specified.
        :param context_right_line: (optional)
            Right-side diff line to attach the inline comment to. Valid only for
            changes and reviews topics. If this is specified, context[file] must
            also be specified.
        :param context_content: (optional)
            Optionally provide content of the specified line and its four preceding
            lines. This is used to specify a short excerpt of context in case the
            lines being commented on change during the review. When not provided,
            Swarm makes an effort to build the content on its own - as this involves
            file operations, it could become slow.
        :param context_version: (optional)
            With a `reviews` topic, this field specifies which version to attach
            the comment to.

        :returns: ``dict``
        """
        if self.swarm.api_version < 3:
            raise SwarmCompatibleError('Comments supported from API version >= 3')

        data = dict(
            topic=topic,
            body=body,
        )  # type: Dict[str, Any]

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

        Method will raise :class:`SwarmException` on failure.

        :param comment_id:
            ID of the comment to be edited.
        :param body:
            Content of the comment.
        :param topic: (optional)
            Topic to comment on. Examples: reviews/1234, changes/1234 or jobs/job001234
        :param task_state: (optional)
            Task state of the comment. Note that certain transitions (such as
            moving from `open` to `verified`) are not possible without an intermediate
            step (`addressed`, in this case).
            Examples: `comment` (not a task), `open`, `addressed`, `verified`.
        :param flags: (optional)
            Flags on the comment. Typically set to `closed` to archive a comment.
        :param silence_notification: (optional)
            If set to 'true' no notifications will ever be sent for this edited comment.
        :param delay_notification: (optional)
            If set to 'true' notifications will be delayed

        :returns: ``dict``
        """
        if self.swarm.api_version < 3:
            raise SwarmCompatibleError('Comments supported from API version >= 3')

        data = dict(
            body=body,
        )  # type: Dict[str, Any]

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
