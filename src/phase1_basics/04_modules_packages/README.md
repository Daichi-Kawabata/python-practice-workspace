# 04. モジュール・パッケージ化

## 学習項目
- モジュール（.pyファイル）の作成・インポート
- パッケージ（ディレクトリ + __init__.py）の作成
- from/import文の使い分け、エイリアス
- 絶対インポート、動的インポート
- __all__による公開API制御
- モジュール検索パス、__name__/__file__属性

## ファイル構成

### `modules.py`
- モジュールの基本概念と実践
- インポート方法の比較
- __name__ == "__main__" パターン
- Ruby/Golangとの比較

### `imports_guide.md`
- インポートの完全ガイド
- ベストプラクティス集
- 実践例・ユースケース
- パフォーマンス考慮事項

### `package_test.py`
- パッケージの各種インポート方法テスト
- sample_packageを使った実践例

### `sample_package/`
実践的なパッケージ例
- `__init__.py`: パッケージ初期化・公開API制御
- `math_utils.py`: 数学ユーティリティ
- `string_utils.py`: 文字列ユーティリティ
- `logging_utils.py`: ログユーティリティ

## 学習のポイント
1. **モジュール化**: 機能ごとにファイル分割
2. **名前空間**: パッケージでの階層化
3. **再利用性**: インポートによるコード共有
4. **保守性**: 適切な依存関係の管理

## インポートパターン
```python
# モジュール全体（推奨）
import json
import my_module

# 特定要素のみ
from json import dumps, loads
from my_module import MyClass

# エイリアス
import numpy as np
import pandas as pd

# 動的インポート（特殊用途）
import importlib
module = importlib.import_module('json')
```

## パッケージ設計原則
- **単一責任**: 1つのモジュールは1つの責任
- **疎結合**: モジュール間の依存を最小化
- **高凝集**: 関連する機能をまとめる
- **明確なAPI**: __all__で公開範囲を制御

## 次のステップ
モジュール・パッケージ化を理解したら、フェーズ2に進んで
外部ライブラリを活用したデータ操作を学びましょう。
