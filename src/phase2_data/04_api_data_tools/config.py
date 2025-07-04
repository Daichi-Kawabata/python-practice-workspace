"""
API データ取得・変換ツール - 設定ファイル

各APIのエンドポイント、パラメータ、データ変換ルールを定義
"""

from typing import Dict, Any

# API エンドポイント設定
API_ENDPOINTS: Dict[str, str] = {
    'jsonplaceholder': 'https://jsonplaceholder.typicode.com/posts',
    'catfacts': 'https://catfact.ninja/facts',
    'randomuser': 'https://randomuser.me/api/?results=50',
    'github': 'https://api.github.com/users/octocat/repos'
}

# データ変換ルール（各APIの重要フィールドを定義）
DATA_MAPPING: Dict[str, Dict[str, str]] = {
    'jsonplaceholder': {
        'id': 'id',
        'title': 'title',
        'content': 'body',
        'user_id': 'userId'
    },
    'catfacts': {
        'fact': 'fact',
        'length': 'length'
    },
    'randomuser': {
        'name': 'name.first',
        'lastname': 'name.last',
        'email': 'email',
        'country': 'location.country'
    },
    'github': {
        'name': 'name',
        'description': 'description',
        'language': 'language',
        'stars': 'stargazers_count'
    }
}

# タイムアウト設定
REQUEST_TIMEOUT = 10

# 出力ファイル設定
DEFAULT_OUTPUT_FILENAME = 'api_data'
SUPPORTED_FORMATS = ['csv', 'excel', 'both']

# ログ設定
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
