from pytest import fixture
from app import app
from app.config import TestConfig


@fixture()
def test_app():
    app.config.from_object(TestConfig)

    yield app

@fixture()
def client(test_app):
    return test_app.test_client()
