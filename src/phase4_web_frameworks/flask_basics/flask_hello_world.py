"""
Flask基礎学習 - Hello World & 基本概念

このファイルでは、Flaskの基本的な使い方を学習します：
- 基本的なルーティング
- HTTPメソッド（GET, POST, PUT, DELETE）
- パスパラメータ & クエリパラメータ
- リクエストボディ（JSON）
- レスポンス（JSON）
- エラーハンドリング
"""

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from datetime import datetime
from typing import Dict, List, Optional
import json

# Flaskアプリケーションの作成
app = Flask(__name__)
CORS(app)  # CORS設定（開発用）

# --- インメモリデータベース（学習用） ---

users_db: List[Dict] = []
next_user_id = 1

# --- ヘルパー関数 ---


def validate_email(email: str) -> bool:
    """簡単なメールアドレス検証"""
    return '@' in email and '.' in email.split('@')[1]


def find_user_by_id(user_id: int) -> Optional[Dict]:
    """IDでユーザーを検索"""
    return next((u for u in users_db if u['id'] == user_id), None)


def validate_user_data(data: Dict, required_fields: Optional[List[str]] = None) -> Dict:
    """ユーザーデータの検証"""
    errors = {}

    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                errors[field] = f"{field}は必須です"

    if 'email' in data and data['email']:
        if not validate_email(data['email']):
            errors['email'] = "有効なメールアドレスを入力してください"
        elif any(u['email'] == data['email'] for u in users_db):
            errors['email'] = "メールアドレスが既に存在します"

    if 'age' in data and data['age'] is not None:
        try:
            age = int(data['age'])
            if age < 0 or age > 150:
                errors['age'] = "年齢は0-150の範囲で入力してください"
        except (ValueError, TypeError):
            errors['age'] = "年齢は数値で入力してください"

    return errors

# --- エラーハンドラー ---


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad Request",
        "message": "リクエストが正しくありません"
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "リソースが見つかりません"
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "サーバー内部エラーが発生しました"
    }), 500

# --- ルートエンドポイント ---


@app.route('/')
def root():
    """ルートエンドポイント"""
    return jsonify({
        "message": "Flask基礎学習へようこそ！",
        "endpoints": {
            "users": "/users",
            "health": "/health",
            "examples": "/examples"
        }
    })


@app.route('/health')
def health_check():
    """ヘルスチェック"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users_db)
    })

# --- ユーザー管理エンドポイント ---


@app.route('/users', methods=['GET'])
def get_users():
    """ユーザー一覧取得"""
    # クエリパラメータの取得
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    name_filter = request.args.get('name_filter', '')

    # バリデーション
    if limit < 1 or limit > 100:
        return jsonify({"error": "limitは1-100の範囲で指定してください"}), 400
    if offset < 0:
        return jsonify({"error": "offsetは0以上で指定してください"}), 400

    # フィルタリング
    filtered_users = users_db
    if name_filter:
        filtered_users = [
            u for u in filtered_users if name_filter.lower() in u['name'].lower()]

    # ページネーション
    paginated_users = filtered_users[offset:offset + limit]

    return jsonify({
        "users": paginated_users,
        "total": len(filtered_users),
        "limit": limit,
        "offset": offset
    })


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ユーザー詳細取得"""
    user = find_user_by_id(user_id)
    if not user:
        abort(404)

    return jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    """ユーザー作成"""
    global next_user_id

    # リクエストボディの取得
    if not request.is_json:
        return jsonify({"error": "Content-Type: application/json が必要です"}), 400

    data = request.get_json()

    # バリデーション
    errors = validate_user_data(data, required_fields=['name', 'email'])
    if errors:
        return jsonify({"errors": errors}), 400

    # ユーザー作成
    new_user = {
        "id": next_user_id,
        "name": data['name'],
        "email": data['email'],
        "age": data.get('age'),
        "created_at": datetime.now().isoformat()
    }

    users_db.append(new_user)
    next_user_id += 1

    return jsonify(new_user), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """ユーザー更新"""
    user = find_user_by_id(user_id)
    if not user:
        abort(404)

    # リクエストボディの取得
    if not request.is_json:
        return jsonify({"error": "Content-Type: application/json が必要です"}), 400

    data = request.get_json()

    # バリデーション（既存ユーザーの更新なので、メール重複チェックは除外）
    errors = {}

    if 'email' in data and data['email']:
        if not validate_email(data['email']):
            errors['email'] = "有効なメールアドレスを入力してください"
        elif any(u['email'] == data['email'] and u['id'] != user_id for u in users_db):
            errors['email'] = "メールアドレスが既に存在します"

    if 'age' in data and data['age'] is not None:
        try:
            age = int(data['age'])
            if age < 0 or age > 150:
                errors['age'] = "年齢は0-150の範囲で入力してください"
        except (ValueError, TypeError):
            errors['age'] = "年齢は数値で入力してください"

    if errors:
        return jsonify({"errors": errors}), 400

    # 更新
    if user:  # 型チェック用にNoneチェックを追加
        for key, value in data.items():
            if key in ['name', 'email', 'age']:
                user[key] = value

    return jsonify(user)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ユーザー削除"""
    global users_db

    user = find_user_by_id(user_id)
    if not user:
        abort(404)

    users_db = [u for u in users_db if u['id'] != user_id]

    return jsonify({"message": "ユーザーを削除しました"})

# --- 学習用エンドポイント ---


@app.route('/examples')
def examples():
    """学習用エンドポイント一覧"""
    return jsonify({
        "examples": [
            {"path": "/examples/query-params",
                "method": "GET", "description": "クエリパラメータの例"},
            {"path": "/examples/path-params/<item_id>",
                "method": "GET", "description": "パスパラメータの例"},
            {"path": "/examples/request-body",
                "method": "POST", "description": "リクエストボディの例"},
            {"path": "/examples/error-handling",
                "method": "GET", "description": "エラーハンドリングの例"}
        ]
    })


@app.route('/examples/query-params')
def query_params_example():
    """クエリパラメータの例"""
    required_param = request.args.get('required_param')
    optional_param = request.args.get('optional_param')
    default_param = request.args.get('default_param', 'デフォルト値')
    int_param = request.args.get('int_param', type=int)
    list_param = request.args.getlist('list_param')

    if not required_param:
        return jsonify({"error": "required_paramが必要です"}), 400

    return jsonify({
        "required_param": required_param,
        "optional_param": optional_param,
        "default_param": default_param,
        "int_param": int_param,
        "list_param": list_param
    })


@app.route('/examples/path-params/<int:item_id>')
def path_params_example(item_id):
    """パスパラメータの例"""
    category = request.args.get('category', 'default')

    return jsonify({
        "item_id": item_id,
        "category": category,
        "message": f"アイテム{item_id}（カテゴリ：{category}）"
    })


@app.route('/examples/request-body', methods=['POST'])
def request_body_example():
    """リクエストボディの例"""
    if not request.is_json:
        return jsonify({"error": "Content-Type: application/json が必要です"}), 400

    data = request.get_json()

    # 簡単なバリデーション
    if 'title' not in data:
        return jsonify({"error": "titleが必要です"}), 400

    return jsonify({
        "received_data": data,
        "message": "データを受信しました"
    })


@app.route('/examples/error-handling')
def error_handling_example():
    """エラーハンドリングの例"""
    error_type = request.args.get('error_type', 'none')

    if error_type == '400':
        abort(400)
    elif error_type == '404':
        abort(404)
    elif error_type == '500':
        abort(500)
    else:
        return jsonify({"message": "エラーは発生しませんでした"})

# --- 実行用の設定 ---


if __name__ == '__main__':
    print("🚀 Flask基礎学習サーバーを起動中...")
    print("📖 サーバー: http://localhost:5000")
    print("🔧 サーバー停止: Ctrl+C")

    # サンプルデータの追加
    users_db.extend([
        {
            "id": 1,
            "name": "田中太郎",
            "email": "tanaka@example.com",
            "age": 25,
            "created_at": datetime.now().isoformat()
        },
        {
            "id": 2,
            "name": "佐藤花子",
            "email": "sato@example.com",
            "age": 30,
            "created_at": datetime.now().isoformat()
        }
    ])
    next_user_id = 3

    app.run(debug=True, host='0.0.0.0', port=5000)
