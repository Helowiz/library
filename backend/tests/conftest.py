import pytest
from core.main import create_app
from core.extensions import db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def session(app):
    return db.session

@pytest.fixture
def client(app):
    return app.test_client()