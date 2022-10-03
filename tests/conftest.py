import pytest

from aioresponses import aioresponses


@pytest.fixture
def aiohttp_mock():
    with aioresponses() as mock:
        yield mock
