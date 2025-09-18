import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from app.main import app
from app.database import Base, get_db
from app import models


TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    pool_pre_ping=True,
)


Base.metadata.create_all(bind=engine)

connection = engine.connect()


@pytest.fixture(autouse=True)
def _outer_transaction_per_test():
    outer = connection.begin()
    try:
        yield
    finally:
        outer.rollback()

TestingSession = sessionmaker(
    bind=connection,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture(scope="function")
def client():
    def _override_get_db():
        db = TestingSession()
        db.begin_nested()
        @event.listens_for(db, "after_transaction_end")
        def _restart_savepoint(sess, trans):
            if trans.nested and not sess.in_nested_transaction():
                sess.begin_nested()

        try:
            yield db
        finally:
            event.remove(db, "after_transaction_end", _restart_savepoint)
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_header(client):
    def _make(email: str = "u@test.com", password: str = "Passw0rd!"):
        client.post("/auth/register", json={"email": email, "password": password})
        res = client.post("/auth/login", json={"email": email, "password": password})
        assert res.status_code == 200, res.text
        token = res.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return _make
