"""
FastAPI Async処理の基本
========================

このファイルでは、FastAPIでの非同期処理の基本概念を学習します。
async/awaitキーワードを使用した非同期プログラミングの基本を理解しましょう。
"""

import asyncio
import time
from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI(title="FastAPI Async Basic", version="1.0.0")

# ===== 基本的な非同期関数の例 =====


async def async_task(task_name: str, duration: int) -> str:
    """
    非同期タスクの例

    Args:
        task_name: タスク名
        duration: 実行時間（秒）

    Returns:
        完了メッセージ
    """
    print(f"開始: {task_name}")
    await asyncio.sleep(duration)  # 非同期的に待機
    print(f"完了: {task_name}")
    return f"{task_name} が {duration} 秒で完了しました"


def sync_task(task_name: str, duration: int) -> str:
    """
    同期タスクの例（比較用）

    Args:
        task_name: タスク名
        duration: 実行時間（秒）

    Returns:
        完了メッセージ
    """
    print(f"開始: {task_name}")
    time.sleep(duration)  # 同期的に待機（ブロッキング）
    print(f"完了: {task_name}")
    return f"{task_name} が {duration} 秒で完了しました"

# ===== FastAPI エンドポイントの例 =====


@app.get("/")
async def root() -> Dict[str, str]:
    """ルートエンドポイント"""
    return {"message": "FastAPI Async処理の基本サンプル"}


@app.get("/sync-endpoint")
def sync_endpoint() -> Dict[str, Any]:
    """
    同期エンドポイントの例
    複数のタスクを順番に実行（ブロッキング）
    """
    start_time = time.time()

    result1 = sync_task("タスク1", 2)
    result2 = sync_task("タスク2", 2)
    result3 = sync_task("タスク3", 2)

    end_time = time.time()
    total_time = end_time - start_time

    return {
        "type": "同期処理",
        "results": [result1, result2, result3],
        "total_time": f"{total_time:.2f}秒",
        "note": "タスクが順番に実行されるため、合計6秒程度かかります"
    }


@app.get("/async-sequential")
async def async_sequential_endpoint() -> Dict[str, Any]:
    """
    非同期エンドポイント（順次実行）
    awaitを使用して順番に実行
    """
    start_time = time.time()

    result1 = await async_task("非同期タスク1", 2)
    result2 = await async_task("非同期タスク2", 2)
    result3 = await async_task("非同期タスク3", 2)

    end_time = time.time()
    total_time = end_time - start_time

    return {
        "type": "非同期処理（順次実行）",
        "results": [result1, result2, result3],
        "total_time": f"{total_time:.2f}秒",
        "note": "awaitで順番に待機するため、同期処理と同様の時間がかかります"
    }


@app.get("/async-concurrent")
async def async_concurrent_endpoint() -> Dict[str, Any]:
    """
    非同期エンドポイント（並列実行）
    asyncio.gather()を使用して並列実行
    """
    start_time = time.time()

    # 複数のタスクを並列実行
    results = await asyncio.gather(
        async_task("並列タスク1", 2),
        async_task("並列タスク2", 2),
        async_task("並列タスク3", 2)
    )

    end_time = time.time()
    total_time = end_time - start_time

    return {
        "type": "非同期処理（並列実行）",
        "results": results,
        "total_time": f"{total_time:.2f}秒",
        "note": "並列実行により、約2秒で完了します"
    }


@app.get("/async-timeout")
async def async_timeout_endpoint() -> Dict[str, Any]:
    """
    非同期処理でのタイムアウト処理の例
    """
    try:
        # 3秒でタイムアウト
        result = await asyncio.wait_for(
            async_task("タイムアウトテスト", 5),  # 5秒のタスク
            timeout=3.0
        )
        return {"status": "成功", "result": result}
    except asyncio.TimeoutError:
        return {
            "status": "タイムアウト",
            "message": "3秒でタイムアウトしました",
            "note": "長時間の処理に対してタイムアウトを設定できます"
        }


@app.get("/async-exception")
async def async_exception_endpoint() -> Dict[str, Any]:
    """
    非同期処理での例外処理の例
    """
    async def failing_task():
        await asyncio.sleep(1)
        raise ValueError("意図的なエラーです")

    try:
        await failing_task()
        return {"status": "成功"}
    except ValueError as e:
        return {
            "status": "エラー",
            "error": str(e),
            "note": "非同期処理でも通常の例外処理が使用できます"
        }

# ===== 実行例 =====

if __name__ == "__main__":
    import uvicorn

    print("FastAPI Async処理の基本サンプル")
    print("=" * 40)
    print("サーバーを起動します...")
    print("ブラウザで以下のURLにアクセスして動作を確認してください:")
    print("- http://localhost:8000/ (ルート)")
    print("- http://localhost:8000/docs (API文書)")
    print("- http://localhost:8000/sync-endpoint (同期処理)")
    print("- http://localhost:8000/async-sequential (非同期順次)")
    print("- http://localhost:8000/async-concurrent (非同期並列)")
    print("- http://localhost:8000/async-timeout (タイムアウト)")
    print("- http://localhost:8000/async-exception (例外処理)")
    print("\nCtrl+C で停止")
    print("=" * 40)

    uvicorn.run(app, host="0.0.0.0", port=8000)
