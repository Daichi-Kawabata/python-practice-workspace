# 環境構築周辺

## venvアクティブ
```bash
.\.venv\Scripts\activate
```

## venv非アクティブ
```bash
deactivate
```

## Git管理について
- `.venv`フォルダは`.gitignore`に追加してGit管理から除外する
- 代わりに`requirements.txt`で依存関係を管理する

### requirements.txtの作成
```bash
pip freeze > requirements.txt
```

### 他の環境での環境再構築
```bash
pip install -r requirements.txt
```

---

# VS Code設定（Python開発効率化）

## 必要な拡張機能
- **Python Extension Pack** (Microsoft公式)
  - Python
  - Pylance
  - Python Debugger

## settings.json設定
```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.completeFunctionParens": true,
    "editor.inlayHints.enabled": "on",
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.analysis.inlayHints.variableTypes": true,
    "python.analysis.inlayHints.callArgumentNames": true,
    "editor.formatOnSave": true,
    "python.formatting.provider": "black"
}
```

## 便利なショートカット
| 機能 | ショートカット | 説明 |
|------|---------------|------|
| **定義へジャンプ** | `F12` | 関数・クラスの定義に移動 |
| **定義をピーク** | `Alt + F12` | 定義をポップアップで表示 |
| **参照を表示** | `Shift + F12` | 使用箇所をすべて表示 |
| **型情報表示** | `Ctrl + K, Ctrl + I` | 詳細な型情報を表示 |
| **パラメータヒント** | `Ctrl + Shift + Space` | 関数の引数情報を表示 |
| **IntelliSense** | `Ctrl + Space` | 補完候補を表示 |
| **ホバー情報** | マウスオーバー | 型情報・引数情報を表示 |

## トラブルシューティング
- Pythonインタープリター選択: `Ctrl + Shift + P` → "Python: Select Interpreter"
- 言語サーバー再起動: `Ctrl + Shift + P` → "Python: Restart Language Server"

---

# Python学習プラン

## 前提スキル
- 他言語（Ruby/Rails、Golang）での開発経験あり
- プログラミングの基礎概念（変数、制御構文、関数、DB等）は理解済み

## 学習の目標
- Python特有の文法や特徴を短期間で習得
- PythonによるWebアプリケーション開発（フレームワーク、ORMapper）に習熟すること

## フェーズ1: Python基礎文法・環境セットアップ（高速キャッチアップ）

### 学習項目
- [x] Python環境構築（仮想環境、Poetryまたはvenvなど）
- [x] 文法の差異にフォーカス（特に型システム・リスト・辞書・内包表記）
  - [x] 型システム・型ヒント（基本型、コレクション、Union、Optional、Callable、ジェネリック）
- [x] クラス定義、オブジェクト指向（継承、多重継承）
  - [x] 基本クラス定義、コンストラクタ、インスタンス・クラス・静的メソッド
  - [x] プロパティ（@property、ゲッター・セッター）
  - [x] 継承、メソッドオーバーライド、super()
  - [x] 多重継承、MRO（Method Resolution Order）
  - [x] 抽象基底クラス（ABC）、プロトコル（Protocol）
- [x] 例外処理の基本構造
  - [x] 基本的なtry/except/else/finally構文
  - [x] 複数例外のキャッチ、例外の詳細情報取得
  - [x] カスタム例外クラスの作成・階層化
  - [x] 例外の再発生（re-raise）、例外チェーン（from句）
  - [x] コンテキストマネージャー（with文）の活用
  - [x] 実践的なパターン（ログ出力、リトライ処理、トランザクション）
- [x] モジュール・パッケージ化の概念
  - [x] モジュール（.pyファイル）の作成・インポート
  - [x] パッケージ（ディレクトリ + __init__.py）の作成
  - [x] from/import文の使い分け、エイリアス
  - [x] 絶対インポート、動的インポート
  - [x] __all__による公開API制御
  - [x] モジュール検索パス、__name__/__file__属性

### 演習課題
- [x] 既存の小規模Ruby/GolangコードをPythonへ書き換える
- [x] 標準ライブラリを用いた簡単なCLIツールの作成

## フェーズ2: Pythonでのデータ操作、外部ライブラリ基礎

### 学習項目
- [x] ファイル・CSV/JSON操作
- [x] Requests、BeautifulSoupでのWebスクレイピング簡単実践
- [x] pandasで簡単なデータ操作・分析

### 演習課題
- [x] APIからJSONを取得し、CSVやExcel形式で出力するツール作成
- [ ] pandasを用いたデータ集計、グラフ描画（簡易分析）

## フェーズ3: ORMapper学習 (SQLAlchemy中心)

### 学習項目
- [ ] SQLAlchemyの基本概念（モデル作成、CRUD操作）
- [ ] DBマイグレーションツール（Alembic）利用法
- [ ] リレーションの定義（1対多、多対多の実践）
- [ ] クエリ構築、トランザクション管理

### 演習課題
- [ ] ブログモデルの設計・CRUDのCLIアプリ作成
- [ ] RubyのActiveRecordやGolangのGORMとの比較メモを作成

## フェーズ4〜5: Webフレームワーク基礎・実践（FastAPI & Flask中心）

### 学習項目
- [ ] FastAPIまたはFlaskの基本構造（ルーティング、HTTPメソッド）
- [ ] REST API作成（JSONの授受、バリデーション）
- [ ] FastAPIのasync処理の基本（非同期プログラミング）
- [ ] ミドルウェア、認証（JWT）、テストの方法（pytest）

### 演習課題
- [ ] 簡単なREST APIの構築（認証付き）
- [ ] Swaggerを活用したAPIドキュメント生成（FastAPI）
- [ ] ORMとの連携（SQLAlchemy & FastAPIの連携アプリケーション）

## フェーズ6: 応用プロジェクト・デプロイ実践（統合演習）

### 学習項目
- [ ] Webアプリケーション設計パターン（MVC、Repositoryパターン）
- [ ] 環境変数管理、設定ファイルの利用
- [ ] コンテナ化（Dockerの基本）
- [ ] デプロイ方法（HerokuまたはAWSなどのPaaSやIaaSの基礎）

### 演習課題（以下のいずれか）
- [ ] 簡易なブログアプリケーション（FastAPI + SQLAlchemy）
- [ ] ToDoリストAPI（認証・コンテナ化込みで）
- [ ] 社内用の簡易ツール（Webスクレイパーや社内システム連携API）