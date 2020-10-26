class SwarmError(Exception):
    """
    Core library exception
    """
    ...


class SwarmNotFoundError(SwarmError):
    """
    Raises when request return HTTP code 404 (not found)
    """
    ...


class SwarmCompatibleError(SwarmError):
    """
    Raises when trying to use new API endpoints on old API version
    """
    ...
