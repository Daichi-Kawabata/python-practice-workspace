import requests
from typing import List, Dict, Any

class APIClient:
    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def fetch_users(self) -> List[Dict[str, Any]]:
        """
        ユーザー情報を取得するメソッド
        :return: ユーザーのリスト
        """
        try:
            url = f"{self.base_url}/users"
            response = requests.get(url)

            match response.status_code:
                case 200:
                    return response.json()
                case 404:
                    raise RecordNotFoundError()
            raise APIError(f"API Error: {response.status_code}")
        except Exception as e:
            print (f"Error: {e}")
            return []

class RecordNotFoundError(Exception):
    """ユーザーが見つからない場合の例外"""
    def __init__(self):
        super().__init__("Users not found")

class APIError(Exception):
    """API呼び出しに失敗した場合の例外"""
    def __init__(self, message: str):
        super().__init__(message)