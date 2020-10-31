from functools import wraps

from .exceptions import SwarmCompatibleError


def minimal_version(version):
    def wrapper(f):
        @wraps(f)
        def _check_version(self, *args, **kwargs):
            if self.swarm.api_version >= version:
                return f(self, *args, **kwargs)

            raise SwarmCompatibleError(
                'Unsupported with API v{} (needed v{}+)'.format(
                    self.swarm.api_version,
                    version
                )
            )

        return _check_version
    return wrapper
