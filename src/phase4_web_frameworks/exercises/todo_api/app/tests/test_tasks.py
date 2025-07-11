import pytest
from fastapi.testclient import TestClient


def test_create_task(client: TestClient, auth_headers):
    """タスク作成テスト"""
    response = client.post(
        "/tasks/",
        json={
            "title": "テストタスク",
            "description": "テスト用のタスクです",
            "priority": "high"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テストタスク"
    assert data["completed"] == False
    assert data["priority"] == "high"


def test_get_tasks(client: TestClient, auth_headers):
    """タスク一覧取得テスト"""
    # タスクを作成
    client.post(
        "/tasks/",
        json={"title": "タスク1", "priority": "low"},
        headers=auth_headers
    )
    client.post(
        "/tasks/",
        json={"title": "タスク2", "priority": "medium"},
        headers=auth_headers
    )

    # 一覧取得
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_task(client: TestClient, auth_headers):
    """タスク更新テスト"""
    # タスク作成
    create_response = client.post(
        "/tasks/",
        json={"title": "更新前タスク", "priority": "low"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    # タスク更新
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "更新後タスク", "completed": True},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "更新後タスク"
    assert data["completed"] == True


def test_delete_task(client: TestClient, auth_headers):
    """タスク削除テスト"""
    # タスク作成
    create_response = client.post(
        "/tasks/",
        json={"title": "削除対象タスク", "priority": "medium"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    # タスク削除
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    # 削除確認
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404
