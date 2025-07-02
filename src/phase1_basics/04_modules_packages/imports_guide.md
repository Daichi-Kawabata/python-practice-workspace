# Pythonインポート完全ガイド

## 基本概念

### インポートとは
- **モジュール**: 1つの`.py`ファイル = 1つのモジュール
- **パッケージ**: ディレクトリ + `__init__.py` = パッケージ
- **インポート**: 他のファイル（モジュール）の機能を現在のファイルで使用可能にすること

## インポートの基本パターン

### 1. モジュール全体のインポート（推奨）

```python
import json
import datetime
import sys

# 使用時はモジュール名.関数名
data = {"name": "Python"}
json_str = json.dumps(data)  # json.dumps()
now = datetime.datetime.now()  # datetime.datetime.now()
paths = sys.path  # sys.path
```

**メリット:**
- どのモジュールの機能かが明確
- 名前の衝突が起こりにくい
- コードの可読性が高い

### 2. 特定の関数・クラスのみインポート

```python
from json import dumps, loads
from datetime import datetime, timedelta
from pathlib import Path

# 使用時はそのまま関数名
json_str = dumps(data)  # dumps() 直接呼び出し
now = datetime.now()  # datetime.now()
path = Path(__file__)  # Path()
```

**メリット:**
- 短く書ける
- よく使う関数の場合は便利

**デメリット:**
- どのモジュール由来か分からない場合がある
- 名前の衝突の可能性

### 3. エイリアス付きインポート

```python
import json as js
import numpy as np  # 慣例的なエイリアス
import pandas as pd  # 慣例的なエイリアス
import matplotlib.pyplot as plt  # 慣例的なエイリアス

# 使用時はエイリアス.関数名
json_str = js.dumps(data)
array = np.array([1, 2, 3])
df = pd.DataFrame({"col": [1, 2, 3]})
```

**メリット:**
- 長いモジュール名を短縮できる
- 慣例的なエイリアスは認識しやすい

### 4. ワイルドカードインポート（非推奨）

```python
from json import *  # ❌ 避けるべき
from datetime import *  # ❌ 避けるべき

# 使用時
dumps(data)  # どこから来た関数か分からない
```

**デメリット:**
- 名前空間の汚染
- どこから来た関数か分からない
- 予期しない名前の衝突

## インポートの使い分け指針

### ✅ 推奨パターン

```python
# 標準ライブラリ - モジュール全体
import json
import datetime
import pathlib
import sys
import os

# 慣例的なエイリアス
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 型ヒント - 特定の要素のみ（例外的にOK）
from typing import List, Dict, Optional, Union, Any

# よく使う基本的な関数・クラス
from pathlib import Path
from datetime import datetime
from collections import defaultdict
```

### ⚠️ 注意が必要なパターン

```python
# 避けるべき - すべてをインポート
from json import *  # ❌ 名前空間が汚染される
from datetime import *  # ❌ どこから来た関数か分からない

# 長すぎる場合はエイリアスを検討
import very_long_module_name_that_is_hard_to_type  # ❌ 長すぎる
# ↓ 改善
import very_long_module_name_that_is_hard_to_type as vlm  # ✅
```

## カスタムモジュールのインポート

### ファイル構造例

```
my_project/
├── main.py
├── utils.py
├── config.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
└── helpers/
    ├── __init__.py
    ├── math_utils.py
    └── string_utils.py
```

### インポート例

```python
# main.py での各種インポート

# 同じディレクトリのモジュール
import utils        # utils.pyファイル全体
import config       # config.pyファイル全体

# パッケージから
import models                     # modelsパッケージ全体
from models import user           # 特定のモジュール
from models.user import User      # 特定のクラス

# サブパッケージから
import helpers.math_utils                    # 特定のモジュール
from helpers.string_utils import clean_text  # 特定の関数

# 使用例
result = utils.some_function()
setting = config.DATABASE_URL
user_instance = User("Alice")
text = clean_text("  hello  ")
```

## 絶対インポート vs 相対インポート

### 絶対インポート（推奨）

```python
# プロジェクトのルートから指定
from myproject.models.user import User
from myproject.helpers.math_utils import calculate
from myproject.config import settings
```

### 相対インポート

```python
# 同じパッケージ内での相対参照
from .user import User           # 同じディレクトリ
from ..helpers.math_utils import calculate  # 親ディレクトリのhelpers
from ...config import settings   # 2つ上の階層のconfig
```

**相対インポートの注意点:**
- パッケージ内からのみ使用可能
- スクリプトとして直接実行できない場合がある
- 可読性が劣る場合がある

## 動的インポート

### importlibを使用

```python
import importlib

# モジュール名を文字列で指定
module_name = "json"
json_module = importlib.import_module(module_name)

# 使用
data = {"dynamic": True}
result = json_module.dumps(data)

# 関数の動的取得
func_name = "loads"
loads_func = getattr(json_module, func_name)
parsed = loads_func(result)
```

### 活用場面
- 設定ファイルで指定されたモジュールを読み込む
- プラグインシステムの実装
- 条件によって異なるモジュールを使用

## エラーハンドリング

### インポートエラーの処理

```python
try:
    import optional_module
except ImportError:
    print("optional_module is not available")
    optional_module = None

# 使用時の条件分岐
if optional_module:
    result = optional_module.some_function()
else:
    result = "default_value"
```

### 特定の関数・クラスのインポートエラー

```python
try:
    from advanced_module import AdvancedClass
except ImportError:
    print("AdvancedClass is not available, using basic implementation")
    from basic_module import BasicClass as AdvancedClass
```

## モジュール検索パス

### sys.pathの確認と操作

```python
import sys

# 現在の検索パス
for i, path in enumerate(sys.path):
    print(f"{i+1}. {path}")

# パスの追加（通常は避ける）
import os
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)  # 最優先で検索
    # または
    sys.path.append(current_dir)     # 最後に検索
```

## 他言語との比較

### Ruby

```ruby
# ファイル全体を読み込み
require 'json'
require_relative 'my_module'  # 相対パス

# 使用
JSON.parse('{"key": "value"}')

# モジュール定義
module MyModule
  def self.function
    # ...
  end
end
```

### Go

```go
// パッケージ全体をインポート
import "encoding/json"
import "fmt"

// エイリアス付き
import j "encoding/json"

// 使用
json.Marshal(data)
j.Marshal(data)  // エイリアス使用

// パッケージ宣言
package main

// 公開/非公開は大文字・小文字で制御
func PublicFunction() {}   // 公開
func privateFunction() {}  // 非公開
```

### Python

```python
# モジュール全体をインポート
import json
import my_module  # 同じディレクトリの場合

# エイリアス付き
import json as js

# 特定の要素のみ
from json import dumps, loads

# 使用
json.dumps(data)
js.dumps(data)  # エイリアス使用
dumps(data)     # 直接使用
```

## ベストプラクティス

### 1. インポートの順序

```python
# 1. 標準ライブラリ
import json
import sys
import os

# 2. サードパーティライブラリ
import numpy as np
import pandas as pd
import requests

# 3. 自作モジュール
import my_module
from my_package import my_class
```

### 2. インポート文の配置

```python
"""
モジュールのドキュメント文字列
"""

# すべてのインポートをファイルの先頭に配置
import json
from datetime import datetime

# グローバル変数
VERSION = "1.0.0"

# 関数・クラス定義
def my_function():
    # 関数内でのインポートは特別な場合のみ
    import time  # 遅延インポート
    return time.time()
```

### 3. 命名規則

```python
# モジュール名: 小文字、アンダースコア
import my_module
from my_package import sub_module

# エイリアス: 短縮形、分かりやすい名前
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 避けるべき
import numpy as n  # ❌ 短すぎる
import pandas as dataframe_library  # ❌ 長すぎる
```

### 4. パフォーマンス考慮

```python
# ✅ 推奨: モジュールレベルでインポート
import json

def process_data(data):
    return json.dumps(data)

# ❌ 避ける: 関数内での不要なインポート
def process_data(data):
    import json  # 毎回インポートされる
    return json.dumps(data)

# ✅ 例外: 遅延インポート（条件付きインポート）
def optional_feature():
    try:
        import optional_library
        return optional_library.do_something()
    except ImportError:
        return "Feature not available"
```

## 実践例

### Webアプリケーションでの典型的なインポート

```python
# app.py
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

# サードパーティ
import requests
from flask import Flask, request, jsonify

# 自作モジュール
from models.user import User
from services.email_service import EmailService
from utils.validators import validate_email
from config import settings

app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not validate_email(data.get('email')):
        return jsonify({'error': 'Invalid email'}), 400
    
    user = User(data['name'], data['email'])
    
    # メール送信
    email_service = EmailService()
    email_service.send_welcome_email(user)
    
    return jsonify({'message': 'User created'}), 201
```

### データ分析でのインポート

```python
# analysis.py
import json
from pathlib import Path
from datetime import datetime

# データ分析ライブラリ
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 自作ユーティリティ
from utils.data_cleaner import clean_dataset
from utils.visualizer import create_charts

def analyze_sales_data(file_path: str):
    # データ読み込み
    df = pd.read_csv(file_path)
    
    # データクリーニング
    df_clean = clean_dataset(df)
    
    # 分析
    summary = df_clean.describe()
    
    # 可視化
    charts = create_charts(df_clean)
    
    return summary, charts
```

## まとめ

1. **基本はモジュール全体のインポート**を使用する
2. **よく使う関数は個別インポート**も可
3. **慣例的なエイリアス**は積極的に使用
4. **ワイルドカードインポートは避ける**
5. **インポート順序**を統一する（標準→サードパーティ→自作）
6. **エラーハンドリング**を適切に行う
7. **パフォーマンス**を考慮してインポート位置を決める

これらの原則を守ることで、保守性が高く読みやすいPythonコードを書くことができます。
