import logging
import sys

import pytest


logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def some_fixture_of_session_scope():
    logger.info("Starting session scoped fixture")
    yield
    logger.info("Ending session scoped fixture")


@pytest.fixture(scope="function", autouse=True)
def some_fixture_of_function_scope():
    logger.info("Starting function scoped fixture")
    yield
    logger.info("Ending function scoped fixture")
