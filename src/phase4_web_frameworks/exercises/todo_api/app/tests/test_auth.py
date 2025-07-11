import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    """ユーザー登録テスト"""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data

def test_register_duplicate_user(client: TestClient, test_user):
    """重複ユーザー登録テスト"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password"
        }
    )
    assert response.status_code == 400

def test_login_user(client: TestClient, test_user):
    """ログインテスト"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient, test_user):
    """無効な認証情報でのログインテスト"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_get_current_user(client: TestClient, auth_headers):
    """現在のユーザー取得テスト"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"