"""
Web API呼び出しとデータ処理

RESTful APIの呼び出し、JSON処理、APIレスポンスの効率的な処理方法を学習します。
requestsライブラリとjsonモジュールを組み合わせて実践的なAPIクライアントを作成します。
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse
import csv
from pathlib import Path


@dataclass
class ApiResponse:
    """API レスポンスを表すクラス"""
    status_code: int
    data: Any
    headers: Dict[str, str]
    url: str
    success: bool
    error_message: Optional[str] = None


@dataclass
class ApiClient:
    """API クライアントクラス"""
    base_url: str
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: int = 30
    session: requests.Session = field(init=False)
    
    def __post_init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)


def basic_api_calls():
    """基本的なAPI呼び出し"""
    print("=== 基本的なAPI呼び出し ===")
    
    # 1. JSONPlaceholder API（テスト用の無料API）
    base_url = "https://jsonplaceholder.typicode.com"
    
    # GET リクエスト
    print("1. GETリクエスト:")
    try:
        response = requests.get(f"{base_url}/posts/1", timeout=10)
        response.raise_for_status()
        
        post_data = response.json()
        print(f"   ステータス: {response.status_code}")
        print(f"   投稿ID: {post_data['id']}")
        print(f"   タイトル: {post_data['title']}")
        print(f"   本文: {post_data['body'][:50]}...")
        
    except requests.RequestException as e:
        print(f"   エラー: {e}")
    
    # 複数のリソースを取得
    print("\n2. 複数のリソースを取得:")
    try:
        response = requests.get(f"{base_url}/posts", timeout=10)
        response.raise_for_status()
        
        posts = response.json()
        print(f"   投稿数: {len(posts)}")
        print("   最初の3投稿:")
        for post in posts[:3]:
            print(f"     ID: {post['id']}, タイトル: {post['title'][:30]}...")
        
    except requests.RequestException as e:
        print(f"   エラー: {e}")
    
    print()


def query_parameters_demo():
    """クエリパラメータの使用"""
    print("=== クエリパラメータの使用 ===")
    
    base_url = "https://jsonplaceholder.typicode.com"
    
    # 1. URLパラメータを使用してフィルタリング
    print("1. 特定のユーザーの投稿を取得:")
    try:
        params = {'userId': 1}
        response = requests.get(f"{base_url}/posts", params=params, timeout=10)
        response.raise_for_status()
        
        user_posts = response.json()
        print(f"   ユーザー1の投稿数: {len(user_posts)}")
        print(f"   実際のURL: {response.url}")
        
    except requests.RequestException as e:
        print(f"   エラー: {e}")
    
    # 2. 複数のパラメータを使用
    print("\n2. 複数のパラメータを使用:")
    try:
        # GitHub API（公開リポジトリ検索）
        github_url = "https://api.github.com/search/repositories"
        params = {
            'q': 'python',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 3
        }
        
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Python-Learning-Script'
        }
        
        response = requests.get(github_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"   検索結果総数: {data['total_count']}")
        print("   上位3リポジトリ:")
        for repo in data['items'][:3]:
            print(f"     名前: {repo['name']}")
            print(f"     スター数: {repo['stargazers_count']}")
            print(f"     言語: {repo['language']}")
            print(f"     説明: {repo['description'][:50] if repo['description'] else 'なし'}...")
            print()
        
    except requests.RequestException as e:
        print(f"   エラー: {e}")
    
    print()


def post_requests_demo():
    """POSTリクエストの例"""
    print("=== POSTリクエストの例 ===")
    
    base_url = "https://jsonplaceholder.typicode.com"
    
    # 1. JSONデータを送信
    print("1. 新しい投稿を作成:")
    try:
        post_data = {
            'title': 'Python学習記録',
            'body': 'BeautifulSoupとrequestsライブラリの学習を完了しました。',
            'userId': 1
        }
        
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(
            f"{base_url}/posts",
            json=post_data,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        created_post = response.json()
        print(f"   ステータス: {response.status_code}")
        print(f"   作成された投稿ID: {created_post['id']}")
        print(f"   タイトル: {created_post['title']}")
        
    except requests.RequestException as e:
        print(f"   エラー: {e}")
    
    # 2. フォームデータを送信
    print("\n2. フォームデータを送信:")
    try:
        form_data = {
            'name': '田中太郎',
            'email': 'tanaka@example.com',
            'message': 'お問い合わせ内容です'
        }
        
        # HTTPbin (テスト用サービス) に送信
        response = requests.post(
            'https://httpbin.org/post',
            data=form_data,
            timeout=10
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"   ステータス: {response.status_code}")
        print(f"   送信されたデータ: {result['form']}")
        
    except requests.RequestException as e:
        print(f"   エラー: {e}")
    
    print()


def session_management():
    """セッション管理とCookie"""
    print("=== セッション管理とCookie ===")
    
    # 1. セッションを使用してCookieを維持
    print("1. セッションを使用:")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Python-Learning-Script'
    })
    
    try:
        # HTTPbinでCookieをセット
        response1 = session.get('https://httpbin.org/cookies/set/session_id/12345', timeout=10)
        print(f"   Cookieセット: {response1.status_code}")
        
        # Cookieが保持されているか確認
        response2 = session.get('https://httpbin.org/cookies', timeout=10)
        response2.raise_for_status()
        
        cookies_data = response2.json()
        print(f"   保持されたCookie: {cookies_data['cookies']}")
        
    except requests.RequestException as e:
        print(f"   エラー: {e}")
    
    # 2. 認証が必要なAPIの例（模擬）
    print("\n2. API認証のパターン:")
    print("   - APIキー: headers={'Authorization': 'Bearer YOUR_API_KEY'}")
    print("   - Basic認証: auth=('username', 'password')")
    print("   - カスタムヘッダー: headers={'X-API-Key': 'your_key'}")
    
    print()


def error_handling_demo():
    """エラーハンドリングの実践"""
    print("=== エラーハンドリングの実践 ===")
    
    def safe_api_call(url: str, **kwargs) -> ApiResponse:
        """安全なAPI呼び出し"""
        try:
            response = requests.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            
            # JSONとして解析を試行
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = response.text
            
            return ApiResponse(
                status_code=response.status_code,
                data=data,
                headers=dict(response.headers),
                url=response.url,
                success=True
            )
            
        except requests.exceptions.Timeout:
            return ApiResponse(
                status_code=0,
                data=None,
                headers={},
                url=url,
                success=False,
                error_message="リクエストがタイムアウトしました"
            )
        except requests.exceptions.ConnectionError:
            return ApiResponse(
                status_code=0,
                data=None,
                headers={},
                url=url,
                success=False,
                error_message="接続エラーが発生しました"
            )
        except requests.exceptions.HTTPError as e:
            return ApiResponse(
                status_code=e.response.status_code if e.response else 0,
                data=None,
                headers={},
                url=url,
                success=False,
                error_message=f"HTTPエラー: {e}"
            )
        except Exception as e:
            return ApiResponse(
                status_code=0,
                data=None,
                headers={},
                url=url,
                success=False,
                error_message=f"予期しないエラー: {e}"
            )
    
    # テスト実行
    print("1. 正常なAPIコール:")
    result1 = safe_api_call("https://jsonplaceholder.typicode.com/posts/1")
    if result1.success:
        print(f"   成功: {result1.data['title']}")
    else:
        print(f"   失敗: {result1.error_message}")
    
    print("\n2. 存在しないエンドポイント:")
    result2 = safe_api_call("https://jsonplaceholder.typicode.com/nonexistent")
    if result2.success:
        print(f"   成功: {result2.status_code}")
    else:
        print(f"   失敗: {result2.error_message} (ステータス: {result2.status_code})")
    
    print("\n3. 存在しないドメイン:")
    result3 = safe_api_call("https://this-domain-does-not-exist-123456.com/api")
    if result3.success:
        print(f"   成功: {result3.status_code}")
    else:
        print(f"   失敗: {result3.error_message}")
    
    print()


def rate_limiting_demo():
    """レート制限の実装"""
    print("=== レート制限の実装 ===")
    
    def api_call_with_rate_limit(urls: List[str], delay: float = 1.0) -> List[ApiResponse]:
        """レート制限付きAPI呼び出し"""
        results = []
        
        for i, url in enumerate(urls):
            print(f"   {i+1}/{len(urls)}: {url} を処理中...")
            
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                result = ApiResponse(
                    status_code=response.status_code,
                    data=data,
                    headers=dict(response.headers),
                    url=response.url,
                    success=True
                )
                results.append(result)
                
                # レート制限
                if i < len(urls) - 1:  # 最後以外は待機
                    time.sleep(delay)
                
            except Exception as e:
                result = ApiResponse(
                    status_code=0,
                    data=None,
                    headers={},
                    url=url,
                    success=False,
                    error_message=str(e)
                )
                results.append(result)
        
        return results
    
    # テスト実行
    test_urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]
    
    print("1. レート制限付きで複数のAPIを呼び出し:")
    results = api_call_with_rate_limit(test_urls, delay=0.5)
    
    print("\n2. 結果サマリー:")
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    
    print(f"   成功: {len(successful)}")
    print(f"   失敗: {len(failed)}")
    
    if successful:
        print("   成功した投稿:")
        for result in successful:
            if result.data:
                print(f"     ID: {result.data['id']}, タイトル: {result.data['title'][:30]}...")
    
    print()


def data_export_demo():
    """API データのCSVエクスポート"""
    print("=== API データのCSVエクスポート ===")
    
    try:
        # ユーザー情報を取得
        response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
        response.raise_for_status()
        
        users = response.json()
        
        # CSVファイルに保存
        output_file = Path("users_data.csv")
        
        print(f"1. {len(users)}人のユーザーデータを取得")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            # ヘッダーを定義
            fieldnames = ['id', 'name', 'username', 'email', 'phone', 'website', 'company']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # ヘッダー行を書き込み
            writer.writeheader()
            
            # データ行を書き込み
            for user in users:
                # ネストしたデータを平坦化
                row = {
                    'id': user['id'],
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'phone': user['phone'],
                    'website': user['website'],
                    'company': user['company']['name'] if user.get('company') else ''
                }
                writer.writerow(row)
        
        print(f"2. データを {output_file} に保存しました")
        print("   CSV ファイルの内容（最初の3行）:")
        
        # 保存したファイルを読み込んで確認
        with open(output_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i < 4:  # ヘッダー + 3行
                    print(f"     {', '.join(row)}")
                else:
                    break
        
    except Exception as e:
        print(f"   エラー: {e}")
    
    print()


def json_processing_demo():
    """JSON データの高度な処理"""
    print("=== JSON データの高度な処理 ===")
    
    try:
        # 複雑なJSON構造を持つデータを取得
        response = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)
        response.raise_for_status()
        
        user_data = response.json()
        
        print("1. 取得したJSONデータの構造:")
        print(json.dumps(user_data, indent=2, ensure_ascii=False)[:300] + "...")
        
        print("\n2. ネストしたデータの抽出:")
        print(f"   名前: {user_data['name']}")
        print(f"   住所: {user_data['address']['city']}, {user_data['address']['zipcode']}")
        print(f"   会社: {user_data['company']['name']}")
        print(f"   緯度経度: ({user_data['address']['geo']['lat']}, {user_data['address']['geo']['lng']})")
        
        print("\n3. データの変換と整形:")
        # フラットな構造に変換
        flat_data = {
            'id': user_data['id'],
            'name': user_data['name'],
            'email': user_data['email'],
            'city': user_data['address']['city'],
            'zipcode': user_data['address']['zipcode'],
            'company': user_data['company']['name'],
            'lat': float(user_data['address']['geo']['lat']),
            'lng': float(user_data['address']['geo']['lng'])
        }
        
        print("   フラット化されたデータ:")
        for key, value in flat_data.items():
            print(f"     {key}: {value}")
        
    except Exception as e:
        print(f"   エラー: {e}")
    
    print()


def api_client_class_demo():
    """API クライアントクラスの使用例"""
    print("=== API クライアントクラスの使用例 ===")
    
    # JSONPlaceholder API クライアント
    client = ApiClient(
        base_url="https://jsonplaceholder.typicode.com",
        headers={'User-Agent': 'Python-Learning-Script'},
        timeout=10
    )
    
    def get_posts(client: ApiClient, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """投稿を取得する関数"""
        url = f"{client.base_url}/posts"
        params = {'userId': user_id} if user_id else {}
        
        try:
            response = client.session.get(url, params=params, timeout=client.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"     エラー: {e}")
            return []
    
    def get_user_info(client: ApiClient, user_id: int) -> Optional[Dict[str, Any]]:
        """ユーザー情報を取得する関数"""
        url = f"{client.base_url}/users/{user_id}"
        
        try:
            response = client.session.get(url, timeout=client.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"     エラー: {e}")
            return None
    
    # 使用例
    print("1. 特定ユーザーの投稿を取得:")
    user_posts = get_posts(client, user_id=1)
    print(f"   ユーザー1の投稿数: {len(user_posts)}")
    
    print("\n2. ユーザー情報を取得:")
    user_info = get_user_info(client, user_id=1)
    if user_info:
        print(f"   ユーザー名: {user_info['name']}")
        print(f"   メール: {user_info['email']}")
    
    print("\n3. 全投稿を取得:")
    all_posts = get_posts(client)
    print(f"   全投稿数: {len(all_posts)}")
    
    # セッションを閉じる
    client.session.close()
    
    print()


def main():
    """メイン実行関数"""
    print("Web API 学習プログラム")
    print("=" * 50)
    
    basic_api_calls()
    query_parameters_demo()
    post_requests_demo()
    session_management()
    error_handling_demo()
    rate_limiting_demo()
    data_export_demo()
    json_processing_demo()
    api_client_class_demo()
    
    print("学習完了！")
    print("\n次のステップ:")
    print("1. 認証が必要なAPIの実装")
    print("2. 非同期API呼び出し（asyncio）")
    print("3. GraphQL APIの処理")
    print("4. APIレスポンスのキャッシュ機能")


if __name__ == "__main__":
    main()
