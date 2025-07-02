# 解答例とヒント集

⚠️ **注意**: まずは自力で実装に挑戦してください！

## 実装のヒント

### 課題1: タスク管理CLIツール

#### Task クラスのヒント
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """JSONシリアライズ用"""
        # datetime を ISO形式文字列に変換
        pass
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """JSON デシリアライズ用"""
        # ISO形式文字列を datetime に変換
        pass
```

#### 例外クラスのヒント
```python
class TaskError(Exception):
    """タスク関連のベース例外"""
    pass

class TaskNotFoundError(TaskError):
    """タスクが見つからない"""
    pass

class TaskFileError(TaskError):
    """ファイル操作エラー"""
    pass
```

#### CLI 引数解析のヒント
```python
import argparse
from typing import List

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # add サブコマンド
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('description', nargs='?', default='', help='Task description')
    
    # list サブコマンド
    list_parser = subparsers.add_parser('list', help='List all tasks')
    
    # 他のサブコマンドも追加...
    
    return parser
```

### 課題2: 設定管理ライブラリ

#### 階層アクセスのヒント
```python
class DotDict:
    """ドット記法でアクセス可能な辞書"""
    def __init__(self, data: dict):
        self._data = data
    
    def __getattr__(self, key: str):
        try:
            value = self._data[key]
            if isinstance(value, dict):
                return DotDict(value)  # 再帰的にDotDict化
            return value
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{key}'")
```

#### プロトコルベースの設計ヒント
```python
from typing import Protocol, Any

class ConfigLoader(Protocol):
    def load(self, file_path: str) -> dict:
        """設定ファイルを読み込んで辞書を返す"""
        ...

class JsonConfigLoader:
    def load(self, file_path: str) -> dict:
        # JSON読み込み実装
        pass

class YamlConfigLoader:
    def load(self, file_path: str) -> dict:
        # YAML読み込み実装
        pass
```

### 課題3: コード移植

#### Ruby → Python API クライアント
```python
import requests
from typing import List, Dict, Any

class ApiError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def fetch_users(self) -> List[Dict[str, Any]]:
        try:
            response = requests.get(f"{self.base_url}/users")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise ApiError(404, "Users not found")
            else:
                raise ApiError(response.status_code, f"API Error: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"Error: {e}")
            return []
        except ApiError as e:
            print(f"Error: {e.message}")
            return []
```

#### Go → Python ファイルプロセッサ
```python
from pathlib import Path
from typing import List

class FileProcessorError(Exception):
    pass

class FileProcessor:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
    
    def count_lines(self) -> int:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return sum(1 for _ in file)
        except (FileNotFoundError, PermissionError) as e:
            raise FileProcessorError(f"Cannot read file: {e}")
    
    def find_word(self, word: str) -> List[int]:
        try:
            line_numbers = []
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    if word in line:
                        line_numbers.append(line_num)
            return line_numbers
        except (FileNotFoundError, PermissionError) as e:
            raise FileProcessorError(f"Cannot read file: {e}")
```

## 実装時のチェックポイント

### 設計品質
- [ ] 単一責任の原則に従っているか
- [ ] 適切な抽象化レベルか
- [ ] 拡張しやすい設計か

### 型安全性
- [ ] すべての関数に型ヒントがあるか
- [ ] ジェネリック型を適切に使っているか
- [ ] mypyでチェックが通るか

### エラーハンドリング
- [ ] 適切な例外階層になっているか
- [ ] リソースの確実なクリーンアップ
- [ ] ユーザーフレンドリーなエラーメッセージ

### Pythonic
- [ ] コンテキストマネージャー（with文）の活用
- [ ] イテレーター・ジェネレーターの活用
- [ ] 標準ライブラリの適切な使用

頑張って挑戦してください！
