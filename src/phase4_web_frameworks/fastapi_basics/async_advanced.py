"""
FastAPI 実践的なAsync処理
========================

このファイルでは、実際のWebアプリケーションでよく使用される
非同期処理のパターンを学習します。

- HTTP リクエスト
- データベース操作
- ファイル操作
- 複数の非同期処理の組み合わせ
"""

import asyncio
import aiohttp
import aiofiles
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

app = FastAPI(title="FastAPI Async実践", version="1.0.0")

# ===== Pydantic モデル =====


class ApiResponse(BaseModel):
    url: str
    status_code: int
    content_length: int
    response_time: float


class FileInfo(BaseModel):
    filename: str
    size: int
    content_preview: str


class TaskResult(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None

# ===== 非同期HTTP リクエスト =====


async def fetch_url(session: aiohttp.ClientSession, url: str) -> ApiResponse:
    """
    非同期でURLからデータを取得

    Args:
        session: aiohttp セッション
        url: 取得するURL

    Returns:
        APIレスポンス情報
    """
    start_time = time.time()

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            content = await response.text()
            response_time = time.time() - start_time

            return ApiResponse(
                url=url,
                status_code=response.status,
                content_length=len(content),
                response_time=response_time
            )
    except Exception as e:
        response_time = time.time() - start_time
        raise HTTPException(
            status_code=500,
            detail=f"URL取得エラー: {str(e)} (時間: {response_time:.2f}秒)"
        )


@app.post("/fetch-multiple-urls")
async def fetch_multiple_urls(urls: List[str]) -> Dict[str, Any]:
    """
    複数のURLを並列で取得

    Args:
        urls: 取得するURLのリスト

    Returns:
        取得結果の一覧
    """
    if len(urls) > 10:
        raise HTTPException(status_code=400, detail="URL数は10個以下にしてください")

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        try:
            # 全URLを並列で取得
            results = await asyncio.gather(
                *[fetch_url(session, url) for url in urls],
                return_exceptions=True  # 例外もresultに含める
            )

            # 成功とエラーを分別
            successful = []
            errors = []

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    errors.append({
                        "url": urls[i],
                        "error": str(result)
                    })
                else:
                    successful.append(result)

            total_time = time.time() - start_time

            return {
                "total_urls": len(urls),
                "successful": len(successful),
                "errors": len(errors),
                "total_time": f"{total_time:.2f}秒",
                "results": {
                    "successful": successful,
                    "errors": errors
                }
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"処理エラー: {str(e)}")

# ===== 非同期ファイル操作 =====


async def read_file_async(filepath: Path) -> FileInfo:
    """
    非同期でファイルを読み取り

    Args:
        filepath: ファイルパス

    Returns:
        ファイル情報
    """
    try:
        async with aiofiles.open(filepath, mode='r', encoding='utf-8') as file:
            content = await file.read()

        file_stats = filepath.stat()

        return FileInfo(
            filename=filepath.name,
            size=file_stats.st_size,
            content_preview=content[:200] +
            "..." if len(content) > 200 else content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイル読み取りエラー: {str(e)}")


async def write_file_async(filepath: Path, content: str) -> Dict[str, Any]:
    """
    非同期でファイルに書き込み

    Args:
        filepath: ファイルパス
        content: 書き込む内容

    Returns:
        書き込み結果
    """
    try:
        # ディレクトリが存在しない場合は作成
        filepath.parent.mkdir(parents=True, exist_ok=True)

        start_time = time.time()
        async with aiofiles.open(filepath, mode='w', encoding='utf-8') as file:
            await file.write(content)

        write_time = time.time() - start_time

        return {
            "filename": filepath.name,
            "content_length": len(content),
            "write_time": f"{write_time:.4f}秒",
            "path": str(filepath)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイル書き込みエラー: {str(e)}")


@app.post("/process-files")
async def process_files(file_contents: Dict[str, str]) -> Dict[str, Any]:
    """
    複数のファイルを並列で処理

    Args:
        file_contents: ファイル名と内容のマッピング

    Returns:
        処理結果
    """
    if len(file_contents) > 5:
        raise HTTPException(status_code=400, detail="ファイル数は5個以下にしてください")

    # 一時ディレクトリ
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    start_time = time.time()

    try:
        # 並列でファイル書き込み
        write_tasks = [
            write_file_async(temp_dir / filename, content)
            for filename, content in file_contents.items()
        ]
        write_results = await asyncio.gather(*write_tasks)

        # 並列でファイル読み取り（確認用）
        read_tasks = [
            read_file_async(temp_dir / filename)
            for filename in file_contents.keys()
        ]
        read_results = await asyncio.gather(*read_tasks)

        total_time = time.time() - start_time

        return {
            "processed_files": len(file_contents),
            "total_time": f"{total_time:.2f}秒",
            "write_results": write_results,
            "read_results": read_results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイル処理エラー: {str(e)}")

# ===== バックグラウンドタスク =====

# タスクの状態管理（実際のアプリケーションではRedisやDBを使用）
task_status: Dict[str, TaskResult] = {}


async def long_running_task(task_id: str, duration: int):
    """
    長時間実行されるバックグラウンドタスク

    Args:
        task_id: タスクID
        duration: 実行時間（秒）
    """
    try:
        task_status[task_id] = TaskResult(task_id=task_id, status="実行中")

        # 重い処理をシミュレート
        for i in range(duration):
            await asyncio.sleep(1)
            # 進行状況の更新
            task_status[task_id].result = f"進行状況: {i+1}/{duration}"

        # 完了
        task_status[task_id].status = "完了"
        task_status[task_id].result = f"{duration}秒の処理が完了しました"

    except Exception as e:
        task_status[task_id].status = "エラー"
        task_status[task_id].error = str(e)


@app.post("/start-background-task/{duration}")
async def start_background_task(duration: int, background_tasks: BackgroundTasks) -> Dict[str, str]:
    """
    バックグラウンドタスクを開始

    Args:
        duration: 実行時間（秒）
        background_tasks: FastAPIのBackgroundTasks

    Returns:
        タスクID
    """
    if duration > 60:
        raise HTTPException(status_code=400, detail="実行時間は60秒以下にしてください")

    import uuid
    task_id = str(uuid.uuid4())

    # バックグラウンドタスクを追加
    background_tasks.add_task(long_running_task, task_id, duration)

    return {
        "task_id": task_id,
        "message": f"{duration}秒のバックグラウンドタスクを開始しました",
        "status_check_url": f"/task-status/{task_id}"
    }


@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str) -> TaskResult:
    """
    タスクの状態を確認

    Args:
        task_id: タスクID

    Returns:
        タスクの状態
    """
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="タスクが見つかりません")

    return task_status[task_id]

# ===== 複合的な非同期処理の例 =====


@app.post("/complex-async-operation")
async def complex_async_operation() -> Dict[str, Any]:
    """
    複数種類の非同期処理を組み合わせた例
    HTTP取得、ファイル操作、計算処理を並列実行
    """
    start_time = time.time()

    # 並列で実行するタスクを定義
    async def fetch_api_data():
        async with aiohttp.ClientSession() as session:
            return await fetch_url(session, "https://httpbin.org/uuid")

    async def heavy_computation():
        # 重い計算をシミュレート
        await asyncio.sleep(2)
        return {"result": "計算完了", "value": 42}

    async def file_operation():
        content = f"処理開始時刻: {time.ctime()}\n処理データ: 非同期テスト"
        temp_path = Path("temp") / "async_test.txt"
        return await write_file_async(temp_path, content)

    try:
        # 全てのタスクを並列実行
        api_result, computation_result, file_result = await asyncio.gather(
            fetch_api_data(),
            heavy_computation(),
            file_operation(),
            return_exceptions=True
        )

        total_time = time.time() - start_time

        # 結果をまとめて返す
        return {
            "total_time": f"{total_time:.2f}秒",
            "api_result": api_result if not isinstance(api_result, Exception) else f"エラー: {api_result}",
            "computation_result": computation_result if not isinstance(computation_result, Exception) else f"エラー: {computation_result}",
            "file_result": file_result if not isinstance(file_result, Exception) else f"エラー: {file_result}",
            "note": "3つの処理を並列実行しました"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"複合処理エラー: {str(e)}")

# ===== ルートとヘルスチェック =====


@app.get("/")
async def root() -> Dict[str, Any]:
    """ルートエンドポイント"""
    return {
        "message": "FastAPI 実践的なAsync処理のサンプル",
        "endpoints": [
            "/docs - API文書",
            "/fetch-multiple-urls - 複数URL並列取得",
            "/process-files - ファイル並列処理",
            "/start-background-task/{duration} - バックグラウンドタスク開始",
            "/task-status/{task_id} - タスク状態確認",
            "/complex-async-operation - 複合非同期処理"
        ]
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """ヘルスチェック"""
    return {"status": "healthy", "timestamp": time.ctime()}

# ===== 実行例 =====

if __name__ == "__main__":
    import uvicorn

    print("FastAPI 実践的なAsync処理サンプル")
    print("=" * 40)
    print("必要なパッケージ:")
    print("- pip install aiohttp aiofiles")
    print("\nサーバーを起動します...")
    print("ブラウザで http://localhost:8001/docs にアクセスして")
    print("各エンドポイントをテストしてください。")
    print("\nCtrl+C で停止")
    print("=" * 40)

    uvicorn.run(app, host="0.0.0.0", port=8001)
