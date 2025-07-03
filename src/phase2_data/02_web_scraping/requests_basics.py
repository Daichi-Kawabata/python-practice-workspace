"""
requestsライブラリの基本操作

HTTP通信の基礎とrequestsライブラリの使い方を学習します。
フェーズ1で学んだ例外処理も活用します。
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HttpResponse:
    """HTTP レスポンスを表すデータクラス"""
    status_code: int
    headers: Dict[str, str]
    content: str
    url: str
    success: bool
    
    @classmethod
    def from_response(cls, response: requests.Response) -> 'HttpResponse':
        """requests.ResponseからHttpResponseを作成"""
        return cls(
            status_code=response.status_code,
            headers=dict(response.headers),
            content=response.text,
            url=response.url,
            success=response.ok
        )


def basic_get_requests():
    """基本的なGETリクエスト"""
    print("=== 基本的なGETリクエスト ===")
    
    # 1. シンプルなGETリクエスト
    print("1. シンプルなGETリクエスト:")
    try:
        # JSONPlaceholder（テスト用のAPI）を使用
        url = "https://jsonplaceholder.typicode.com/posts/1"
        response = requests.get(url)
        
        print(f"ステータスコード: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"レスポンスサイズ: {len(response.text)} 文字")
        
        # JSONデータの取得
        if response.ok:
            data = response.json()
            print(f"タイトル: {data.get('title')}")
            print(f"本文: {data.get('body')[:50]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析エラー: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. パラメータ付きGETリクエスト
    print("2. パラメータ付きGETリクエスト:")
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        params = {
            'userId': 1,
            '_limit': 3  # 結果を3件に制限
        }
        
        response = requests.get(url, params=params)
        print(f"実際のURL: {response.url}")
        
        if response.ok:
            posts = response.json()
            print(f"取得した投稿数: {len(posts)}")
            for post in posts:
                print(f"  - {post['title']}")
    
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")


def advanced_request_options():
    """高度なリクエストオプション"""
    print("=== 高度なリクエストオプション ===")
    
    # 1. ヘッダーの設定
    print("1. カスタムヘッダーの設定:")
    try:
        url = "https://httpbin.org/headers"  # ヘッダー情報を返すテストAPI
        headers = {
            'User-Agent': 'Python-Learning-Program/1.0',  # ASCII文字のみ使用
            'Accept': 'application/json',
            'X-Custom-Header': 'Learning-Python',
            'X-Language': 'ja'  # 言語情報はコードで表現
        }
        
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            sent_headers = data.get('headers', {})
            print(f"送信したUser-Agent: {sent_headers.get('User-Agent')}")
            print(f"カスタムヘッダー: {sent_headers.get('X-Custom-Header')}")
    
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
    
    print("\n" + "-"*30 + "\n")
    
    # 2. タイムアウトの設定
    print("2. タイムアウトの設定:")
    try:
        url = "https://jsonplaceholder.typicode.com/posts/1"
        
        # タイムアウトを3秒に設定
        response = requests.get(url, timeout=3)
        print(f"レスポンス時間: {response.elapsed.total_seconds():.2f}秒")
        
    except requests.exceptions.Timeout:
        print("タイムアウトエラー: リクエストが3秒以内に完了しませんでした")
    except requests.exceptions.RequestException as e:
        print(f"その他のエラー: {e}")
    except UnicodeEncodeError as e:
        print(f"文字エンコーディングエラー: HTTPヘッダーにASCII以外の文字が含まれています - {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")
    
    print("\n" + "-"*30 + "\n")
    
    # 3. リトライ機能
    print("3. リトライ機能の実装:")
    
    def request_with_retry(url: str, max_retries: int = 3, delay: float = 1.0) -> Optional[requests.Response]:
        """リトライ機能付きリクエスト"""
        for attempt in range(max_retries):
            try:
                print(f"  試行 {attempt + 1}/{max_retries}")
                response = requests.get(url, timeout=5)
                if response.ok:
                    return response
                else:
                    print(f"  HTTPエラー: {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"  リクエストエラー: {e}")
            
            if attempt < max_retries - 1:
                print(f"  {delay}秒待機してリトライ...")
                time.sleep(delay)
        
        print("  最大試行回数に達しました")
        return None
    
    # テスト用（正常なURL）
    response = request_with_retry("https://jsonplaceholder.typicode.com/posts/1")
    if response:
        print("  ✅ リクエスト成功")
    else:
        print("  ❌ リクエスト失敗")


def post_requests():
    """POSTリクエストの処理"""
    print("=== POSTリクエストの処理 ===")
    
    # 1. JSONデータのPOST
    print("1. JSONデータのPOST:")
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        post_data = {
            'title': 'Python学習記録',
            'body': 'requests ライブラリの学習中です。',
            'userId': 1
        }
        
        response = requests.post(url, json=post_data)
        print(f"ステータスコード: {response.status_code}")
        
        if response.ok:
            created_post = response.json()
            print(f"作成されたポストID: {created_post.get('id')}")
            print(f"タイトル: {created_post.get('title')}")
    
    except requests.exceptions.RequestException as e:
        print(f"POSTリクエストエラー: {e}")
    
    print("\n" + "-"*30 + "\n")
    
    # 2. フォームデータのPOST
    print("2. フォームデータのPOST:")
    try:
        url = "https://httpbin.org/post"  # POSTテスト用API
        form_data = {
            'username': 'test_user',
            'message': 'Hello from Python!'
        }
        
        response = requests.post(url, data=form_data)
        if response.ok:
            result = response.json()
            sent_form = result.get('form', {})
            print(f"送信したユーザー名: {sent_form.get('username')}")
            print(f"送信したメッセージ: {sent_form.get('message')}")
    
    except requests.exceptions.RequestException as e:
        print(f"フォームPOSTエラー: {e}")


def session_management():
    """セッション管理"""
    print("=== セッション管理 ===")
    
    # セッションオブジェクトの作成
    session = requests.Session()
    
    # セッション共通のヘッダーを設定
    session.headers.update({
        'User-Agent': 'Python-Learning-Session/1.0',  # ASCII文字のみ使用
        'Accept': 'application/json'
    })
    
    print("1. セッションを使った連続リクエスト:")
    try:
        # 複数のリクエストでセッションを再利用
        urls = [
            "https://jsonplaceholder.typicode.com/posts/1",
            "https://jsonplaceholder.typicode.com/posts/2",
            "https://jsonplaceholder.typicode.com/posts/3"
        ]
        
        for i, url in enumerate(urls, 1):
            response = session.get(url)
            if response.ok:
                data = response.json()
                print(f"  投稿{i}: {data['title'][:30]}...")
            else:
                print(f"  投稿{i}: エラー {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"セッションエラー: {e}")
    
    finally:
        # セッションを適切にクローズ
        session.close()


def error_handling_examples():
    """エラーハンドリングの例"""
    print("=== エラーハンドリングの例 ===")
    
    def safe_request(url: str) -> Optional[HttpResponse]:
        """安全なHTTPリクエスト"""
        try:
            response = requests.get(url, timeout=5)
            return HttpResponse.from_response(response)
        
        except requests.exceptions.Timeout:
            print(f"タイムアウト: {url}")
            return None
        
        except requests.exceptions.ConnectionError:
            print(f"接続エラー: {url}")
            return None
        
        except requests.exceptions.HTTPError as e:
            print(f"HTTPエラー: {e}")
            return None
        
        except requests.exceptions.RequestException as e:
            print(f"リクエストエラー: {e}")
            return None
    
    # テスト用URL（正常・異常）
    test_urls = [
        "https://jsonplaceholder.typicode.com/posts/1",  # 正常
        "https://nonexistent-domain-xyz123.com",         # 接続エラー
        "https://httpbin.org/status/404"                 # HTTPエラー
    ]
    
    print("各URLへのリクエスト結果:")
    for url in test_urls:
        print(f"\n  URL: {url}")
        result = safe_request(url)
        if result:
            print(f"    ✅ 成功: {result.status_code}")
        else:
            print(f"    ❌ 失敗")


def download_file_example():
    """ファイルダウンロードの例"""
    print("=== ファイルダウンロードの例 ===")
    
    try:
        # 小さなJSONファイルをダウンロード
        url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(url)
        
        if response.ok:
            # ファイルに保存
            output_file = Path("downloaded_users.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
            
            print(f"ファイルをダウンロードしました: {output_file}")
            print(f"ファイルサイズ: {output_file.stat().st_size} バイト")
            
            # ダウンロードしたファイルの内容確認
            with open(output_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
                print(f"ユーザー数: {len(users)}人")
                print(f"最初のユーザー: {users[0]['name']}")
            
            # クリーンアップ
            output_file.unlink()
            print(f"ファイルを削除しました: {output_file}")
    
    except requests.exceptions.RequestException as e:
        print(f"ダウンロードエラー: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析エラー: {e}")


if __name__ == "__main__":
    print("フェーズ2-02: requests基礎操作の学習\n")
    
    basic_get_requests()
    print("\n" + "="*60 + "\n")
    
    advanced_request_options()
    print("\n" + "="*60 + "\n")
    
    post_requests()
    print("\n" + "="*60 + "\n")
    
    session_management()
    print("\n" + "="*60 + "\n")
    
    error_handling_examples()
    print("\n" + "="*60 + "\n")
    
    download_file_example()
    
    print("\n学習完了！次は BeautifulSoup でのHTML解析に進みましょう。")
