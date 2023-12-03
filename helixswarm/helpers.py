import re

from functools import wraps
from typing import Callable

from helixswarm.exceptions import SwarmCompatibleError, SwarmError


def minimal_version(version: int):
    def wrapper(f: Callable) -> Callable:
        @wraps(f)
        def _check_version(self, *args, **kwargs):
            if hasattr(self, 'swarm'):
                current_version = self.swarm.version
            else:
                current_version = self.version

            if float(current_version) >= float(version):
                return f(self, *args, **kwargs)

            raise SwarmCompatibleError(
                f'Unsupported with API v{current_version} (needed v{version}+)'
            )

        return _check_version
    return wrapper


def get_review_id(review_url: str) -> int:
    ret = re.compile(r'/(\d+)').findall(review_url)
    if not ret:
        raise SwarmError(f'Invalid review: {review_url}')

    return int(ret[0])
