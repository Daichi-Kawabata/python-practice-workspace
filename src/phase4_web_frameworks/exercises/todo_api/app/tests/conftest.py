import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .test_config import setup_test_environment  # テスト環境の設定
from app.main import app
from app.database import get_db_session, Base
from app.models.user import User
from app.models.task import Task


# テスト用SQLiteデータベース（インメモリ）
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """テスト用データベースセッション"""
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """テスト用FastAPIクライアント"""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """テスト用ユーザー"""
    from app.crud.user import create_user
    from app.schemas.user import UserCreate

    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    return create_user(db=db_session, user=user_data)


@pytest.fixture
def auth_headers(client, test_user):
    """認証ヘッダー"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
