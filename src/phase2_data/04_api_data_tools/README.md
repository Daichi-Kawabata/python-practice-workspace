# API データ取得・変換ツール - 演習課題

## 🎯 課題概要
複数のWeb APIからJSONデータを取得し、CSV/Excel形式で出力するPythonツールを作成してください。

## 📋 要件

### 基本要件
1. **複数のAPIからデータを取得**
   - 最低3つの異なるAPIを使用
   - JSONレスポンスを適切に処理
   - エラーハンドリングを実装

2. **データ形式の変換**
   - JSON → CSV変換
   - JSON → Excel変換
   - 適切なデータ構造に整形

3. **コマンドライン引数の処理**
   - 出力形式の指定（csv/excel/both）
   - 出力ファイル名の指定
   - APIの選択オプション

### 推奨API一覧
以下のAPIから選択してください（すべて無料・認証不要）：

1. **JSONPlaceholder API**
   - URL: `https://jsonplaceholder.typicode.com/posts`
   - 用途: ブログ投稿データ

2. **Open Weather Map API（一部無料）**
   - URL: `https://api.openweathermap.org/data/2.5/weather?q=Tokyo&appid=YOUR_API_KEY`
   - 用途: 天気予報データ
   - 注意: 無料アカウント登録が必要

3. **REST Countries API**
   - URL: `https://restcountries.com/v3.1/all`
   - 用途: 国の情報データ

4. **Cat Facts API**
   - URL: `https://catfact.ninja/facts`
   - 用途: 猫の雑学データ

5. **Random User API**
   - URL: `https://randomuser.me/api/?results=50`
   - 用途: ランダムユーザー情報

6. **GitHub API（認証不要の部分）**
   - URL: `https://api.github.com/users/octocat/repos`
   - 用途: GitHubリポジトリ情報

## 🛠️ 実装すべき機能

### 1. データ取得機能
```python
def fetch_api_data(api_name: str) -> dict:
    """指定されたAPIからデータを取得"""
    pass

def fetch_all_apis() -> dict:
    """すべてのAPIからデータを取得"""
    pass
```

### 2. データ変換機能
```python
def json_to_csv(data: dict, output_file: str) -> None:
    """JSONデータをCSVに変換"""
    pass

def json_to_excel(data: dict, output_file: str) -> None:
    """JSONデータをExcelに変換"""
    pass
```

### 3. コマンドライン機能
```python
def main():
    """メイン関数 - コマンドライン引数を処理"""
    pass

if __name__ == "__main__":
    main()
```

## 📊 期待される出力例

### CSV出力例
```csv
source,id,title,description,created_at
jsonplaceholder,1,Blog Post Title,Post content here,2024-01-01
countries,JP,Japan,Asian country,N/A
```

### Excel出力例
- シート1: JSONPlaceholder データ
- シート2: Countries データ
- シート3: API Summary

## 🔧 技術要件

### 必要なライブラリ
```python
import requests
import json
import csv
import pandas as pd
import argparse
from typing import Dict, List, Optional
from datetime import datetime
```

### エラーハンドリング
- HTTP エラー (404, 500, etc.)
- ネットワーク エラー
- JSON パースエラー
- ファイル書き込みエラー

### 型ヒント
- すべての関数に型ヒントを付ける
- 複雑なデータ構造はTypeAlias を使用

## 💡 実装のヒント

### 1. API レスポンスの構造を理解する
```python
# 各APIのレスポンス例を確認
response = requests.get(url)
print(json.dumps(response.json(), indent=2))
```

### 2. データの正規化
```python
# 異なるAPIの構造を統一形式に変換
def normalize_data(api_name: str, raw_data: dict) -> List[dict]:
    """APIデータを統一形式に変換"""
    pass
```

### 3. 設定ファイルの活用
```python
# config.py
API_ENDPOINTS = {
    'jsonplaceholder': 'https://jsonplaceholder.typicode.com/posts',
    'countries': 'https://restcountries.com/v3.1/all',
    'catfacts': 'https://catfact.ninja/facts'
}
```

## 🎯 実行例

### 基本実行
```bash
python api_data_tool.py --format csv --output result.csv --apis jsonplaceholder,countries
```

### 詳細実行
```bash
python api_data_tool.py --format both --output mydata --apis all --verbose
```

## 🏆 評価ポイント

### 基本点（60点）
- [ ] 3つのAPIからデータを取得
- [ ] CSV出力機能
- [ ] 基本的なエラーハンドリング

### 標準点（80点）
- [ ] Excel出力機能
- [ ] コマンドライン引数の処理
- [ ] 適切な型ヒント

### 高得点（100点）
- [ ] 複数シートのExcel出力
- [ ] 詳細なエラーメッセージ
- [ ] ログ機能
- [ ] 設定ファイルの活用
- [ ] ユニットテストの作成

## 📚 参考資料

### requests ライブラリ
```python
import requests

response = requests.get(url, timeout=10)
response.raise_for_status()  # HTTPエラーチェック
data = response.json()
```

### pandas Excel出力
```python
import pandas as pd

df = pd.DataFrame(data)
df.to_excel('output.xlsx', index=False, sheet_name='Sheet1')
```

### argparse の使用
```python
import argparse

parser = argparse.ArgumentParser(description='API Data Tool')
parser.add_argument('--format', choices=['csv', 'excel', 'both'], default='csv')
parser.add_argument('--output', required=True)
args = parser.parse_args()
```

## 🎉 完成目標

最終的に以下のようなツールが完成することを目指してください：

1. **使いやすいCLI**: シンプルで直感的なコマンドライン
2. **堅牢性**: エラーが発生しても適切に処理
3. **拡張性**: 新しいAPIを簡単に追加可能
4. **可読性**: 他の開発者が理解しやすいコード

頑張って実装してみてください！質問があれば、遠慮なくお聞きください。 🚀
