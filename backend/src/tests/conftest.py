import logging
import pytest
from application import app


@pytest.fixture(autouse=True, scope="function")
def setUp():
    yield


@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    app.logger.setLevel(logging.ERROR)
    yield client
