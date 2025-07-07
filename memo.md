# 環境構築周辺

## venv アクティブ

```bash
.\.venv\Scripts\activate
```

## venv 非アクティブ

```bash
deactivate
```

## Git 管理について

- `.venv`フォルダは`.gitignore`に追加して Git 管理から除外する
- 代わりに`requirements.txt`で依存関係を管理する

### requirements.txt の作成

```bash
pip freeze > requirements.txt
```

### 他の環境での環境再構築

```bash
pip install -r requirements.txt
```

---

# VS Code 設定（Python 開発効率化）

## 必要な拡張機能

- **Python Extension Pack** (Microsoft 公式)
  - Python
  - Pylance
  - Python Debugger

## settings.json 設定

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

| 機能                 | ショートカット         | 説明                     |
| -------------------- | ---------------------- | ------------------------ |
| **定義へジャンプ**   | `F12`                  | 関数・クラスの定義に移動 |
| **定義をピーク**     | `Alt + F12`            | 定義をポップアップで表示 |
| **参照を表示**       | `Shift + F12`          | 使用箇所をすべて表示     |
| **型情報表示**       | `Ctrl + K, Ctrl + I`   | 詳細な型情報を表示       |
| **パラメータヒント** | `Ctrl + Shift + Space` | 関数の引数情報を表示     |
| **IntelliSense**     | `Ctrl + Space`         | 補完候補を表示           |
| **ホバー情報**       | マウスオーバー         | 型情報・引数情報を表示   |

## トラブルシューティング

- Python インタープリター選択: `Ctrl + Shift + P` → "Python: Select Interpreter"
- 言語サーバー再起動: `Ctrl + Shift + P` → "Python: Restart Language Server"

---

# Python 学習プラン

## 前提スキル

- 他言語（Ruby/Rails、Golang）での開発経験あり
- プログラミングの基礎概念（変数、制御構文、関数、DB 等）は理解済み

## 学習の目標

- Python 特有の文法や特徴を短期間で習得
- Python による Web アプリケーション開発（フレームワーク、ORMapper）に習熟すること

## フェーズ 1: Python 基礎文法・環境セットアップ（高速キャッチアップ）

### 学習項目

- [x] Python 環境構築（仮想環境、Poetry または venv など）
- [x] 文法の差異にフォーカス（特に型システム・リスト・辞書・内包表記）
  - [x] 型システム・型ヒント（基本型、コレクション、Union、Optional、Callable、ジェネリック）
- [x] クラス定義、オブジェクト指向（継承、多重継承）
  - [x] 基本クラス定義、コンストラクタ、インスタンス・クラス・静的メソッド
  - [x] プロパティ（@property、ゲッター・セッター）
  - [x] 継承、メソッドオーバーライド、super()
  - [x] 多重継承、MRO（Method Resolution Order）
  - [x] 抽象基底クラス（ABC）、プロトコル（Protocol）
- [x] 例外処理の基本構造
  - [x] 基本的な try/except/else/finally 構文
  - [x] 複数例外のキャッチ、例外の詳細情報取得
  - [x] カスタム例外クラスの作成・階層化
  - [x] 例外の再発生（re-raise）、例外チェーン（from 句）
  - [x] コンテキストマネージャー（with 文）の活用
  - [x] 実践的なパターン（ログ出力、リトライ処理、トランザクション）
- [x] モジュール・パッケージ化の概念
  - [x] モジュール（.py ファイル）の作成・インポート
  - [x] パッケージ（ディレクトリ + **init**.py）の作成
  - [x] from/import 文の使い分け、エイリアス
  - [x] 絶対インポート、動的インポート
  - [x] **all**による公開 API 制御
  - [x] モジュール検索パス、**name**/**file**属性

### 演習課題

- [x] 既存の小規模 Ruby/Golang コードを Python へ書き換える
- [x] 標準ライブラリを用いた簡単な CLI ツールの作成

## フェーズ 2: Python でのデータ操作、外部ライブラリ基礎

### 学習項目

- [x] ファイル・CSV/JSON 操作
- [x] Requests、BeautifulSoup での Web スクレイピング簡単実践
- [x] pandas で簡単なデータ操作・分析

### 演習課題

- [x] API から JSON を取得し、CSV や Excel 形式で出力するツール作成
- [ ] pandas を用いたデータ集計、グラフ描画（簡易分析）

## フェーズ 3: ORMapper 学習 (SQLAlchemy 中心)

### 学習項目

- [x] SQLAlchemy の基本概念（モデル作成、CRUD 操作）
- [x] DB マイグレーションツール（Alembic）利用法
- [x] リレーションの定義（1 対多、多対多の実践）
- [x] クエリ構築、トランザクション管理

### 演習課題

- [x] ブログモデルの設計・CRUD の CLI アプリ作成 →CLI の作成は時間がかかるため BLOG モデルの操作ができるレベルまで学習済み
- [x] Ruby の ActiveRecord や Golang の GORM との比較メモを作成

### 学習状況（2025-07-04 時点）

- [x] 相対インポートエラーの解決完了（models.py, crud_operations.py, blog_cli.py）
- [x] database.py のテスト実行成功（データベース初期化・セッション作成）
- [x] models.py のテスト実行成功（テーブル作成・テストデータ挿入）
- [x] 学習用教材の整理完了（演習課題を適切に分離）
- [x] 演習課題用の骨格ファイル作成完了（exercises/crud_operations.py, exercises/blog_cli.py）
- [x] 参考実装の保存完了（exercises/\*\_template.py）
- [x] 演習課題の実装・練習（学習者が実施）

## フェーズ 4〜5: Web フレームワーク基礎・実践（FastAPI & Flask 中心）

### 学習項目

- [x] 開発環境セットアップ（FastAPI, Flask, uvicorn 等のインストール）
- [x] FastAPI の基本構造（ルーティング、HTTP メソッド）の理解
- [x] REST API 作成（JSON の授受、バリデーション）
- [ ] FastAPI の async 処理の基本（非同期プログラミング）
- [ ] ミドルウェア、認証（JWT）、テストの方法（pytest）

### 演習課題

- [ ] 簡単な REST API の構築（認証付き）
- [ ] Swagger を活用した API ドキュメント生成（FastAPI）
- [ ] ORM との連携（SQLAlchemy & FastAPI の連携アプリケーション）

## フェーズ 6: 応用プロジェクト・デプロイ実践（統合演習）

### 学習項目

- [ ] Web アプリケーション設計パターン（MVC、Repository パターン）
- [ ] 環境変数管理、設定ファイルの利用
- [ ] コンテナ化（Docker の基本）
- [ ] デプロイ方法（Heroku または AWS などの PaaS や IaaS の基礎）

### 演習課題（以下のいずれか）

- [ ] 簡易なブログアプリケーション（FastAPI + SQLAlchemy）
- [ ] ToDo リスト API（認証・コンテナ化込みで）
- [ ] 社内用の簡易ツール（Web スクレイパーや社内システム連携 API）
