"""
FastAPI JWT認証の基本
====================

このファイルでは、FastAPIでのJWT（JSON Web Token）認証について学習します。
JWTを使用したトークンベース認証の実装方法を理解しましょう。

- JWT トークンの生成・検証
- ログイン・ログアウト
- 認証が必要なエンドポイントの保護
- 権限（スコープ）ベースのアクセス制御
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any, Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI(title="FastAPI JWT認証", version="1.0.0")

# ===== 設定 =====

# JWT設定
SECRET_KEY = "your-secret-key-here-change-in-production"  # 本番環境では環境変数から取得
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# パスワードハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2スキーム設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ===== Pydantic モデル =====


class User(BaseModel):
    """ユーザーモデル"""
    username: str
    email: str
    full_name: str
    disabled: bool = False
    scopes: List[str] = []


class UserInDB(User):
    """データベース内のユーザーモデル（ハッシュ化されたパスワード含む）"""
    hashed_password: str


class Token(BaseModel):
    """トークンモデル"""
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    """トークンデータモデル"""
    username: Optional[str] = None
    scopes: List[str] = []


class UserCreate(BaseModel):
    """ユーザー作成モデル"""
    username: str
    email: str
    full_name: str
    password: str
    scopes: List[str] = []


class UserResponse(BaseModel):
    """ユーザーレスポンスモデル（パスワード除外）"""
    username: str
    email: str
    full_name: str
    disabled: bool
    scopes: List[str]

# ===== 疑似データベース（実際のアプリケーションではデータベースを使用） =====


fake_users_db: Dict[str, UserInDB] = {}

# サンプルユーザーを追加


def create_sample_users():
    """サンプルユーザーを作成"""
    sample_users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "full_name": "Admin User",
            "password": "admin123",
            "scopes": ["read", "write", "admin"]
        },
        {
            "username": "user1",
            "email": "user1@example.com",
            "full_name": "Regular User",
            "password": "user123",
            "scopes": ["read"]
        },
        {
            "username": "editor",
            "email": "editor@example.com",
            "full_name": "Editor User",
            "password": "editor123",
            "scopes": ["read", "write"]
        }
    ]

    for user_data in sample_users:
        password = user_data.pop("password")
        user = UserInDB(
            **user_data,
            hashed_password=pwd_context.hash(password),
            disabled=False
        )
        fake_users_db[user.username] = user


create_sample_users()

# ===== パスワードハッシュ化関数 =====


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化"""
    return pwd_context.hash(password)

# ===== ユーザー管理関数 =====


def get_user(username: str) -> Optional[UserInDB]:
    """ユーザーを取得"""
    return fake_users_db.get(username)


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """ユーザー認証"""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# ===== JWT トークン関数 =====


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """アクセストークンを作成"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """トークンを検証"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効なトークンです",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
        return token_data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なトークンです",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ===== 依存性注入関数 =====


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """現在のユーザーを取得"""
    token_data = verify_token(token)
    if not token_data.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なトークンです",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーが見つかりません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(**user.model_dump())


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """現在のアクティブユーザーを取得"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="無効なユーザーです")
    return current_user


def require_scopes(required_scopes: List[str]):
    """指定されたスコープを要求する依存性注入関数"""
    def check_scopes(
        token: Annotated[str, Depends(oauth2_scheme)]
    ) -> User:
        token_data = verify_token(token)

        # スコープチェック
        for scope in required_scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"'{scope}' 権限が必要です",
                )

        if not token_data.username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効なトークンです",
            )

        user = get_user(username=token_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ユーザーが見つかりません",
            )

        return User(**user.model_dump())

    return check_scopes

# ===== 認証エンドポイント =====


@app.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """新規ユーザー登録"""
    if user_data.username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="ユーザー名が既に存在します"
        )

    # 新しいユーザーを作成
    hashed_password = get_password_hash(user_data.password)
    new_user = UserInDB(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        disabled=False,
        scopes=user_data.scopes or ["read"]  # デフォルトは読み取り権限
    )

    fake_users_db[user_data.username] = new_user

    return UserResponse(**new_user.model_dump())


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """ログインしてアクセストークンを取得"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 秒単位
    )


@app.post("/login", response_model=Token)
async def login(username: str, password: str):
    """JSONペイロードでのログイン"""
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

# ===== 保護されたエンドポイント =====


@app.get("/users/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """現在のユーザー情報を取得"""
    return UserResponse(**current_user.model_dump())


@app.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """現在のユーザーのアイテムを取得"""
    return {
        "items": [
            {"id": 1, "title": f"{current_user.username}のアイテム1",
                "owner": current_user.username},
            {"id": 2, "title": f"{current_user.username}のアイテム2",
                "owner": current_user.username}
        ]
    }


@app.get("/protected")
async def protected_route(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """認証が必要な保護されたエンドポイント"""
    return {
        "message": f"こんにちは、{current_user.full_name}さん！",
        "user": current_user.username,
        "scopes": current_user.scopes,
        "access_time": datetime.now().isoformat()
    }

# ===== 権限ベースの保護されたエンドポイント =====


@app.get("/admin")
async def admin_only(
    current_user: Annotated[User, Depends(require_scopes(["admin"]))]
):
    """管理者のみアクセス可能"""
    return {
        "message": "管理者専用エリアです",
        "admin_user": current_user.username,
        "admin_data": {
            "total_users": len(fake_users_db),
            "system_status": "正常",
            "last_maintenance": "2024-01-01"
        }
    }


@app.get("/read-data")
async def read_data(
    current_user: Annotated[User, Depends(require_scopes(["read"]))]
):
    """読み取り権限でアクセス可能"""
    return {
        "message": "データ読み取り成功",
        "data": [
            {"id": 1, "name": "サンプルデータ1"},
            {"id": 2, "name": "サンプルデータ2"},
            {"id": 3, "name": "サンプルデータ3"}
        ],
        "user": current_user.username
    }


@app.post("/write-data")
async def write_data(
    data: Dict[str, Any],
    current_user: Annotated[User, Depends(require_scopes(["write"]))]
):
    """書き込み権限でアクセス可能"""
    return {
        "message": "データ書き込み成功",
        "written_data": data,
        "written_by": current_user.username,
        "timestamp": datetime.now().isoformat()
    }

# ===== パブリック エンドポイント =====


@app.get("/")
async def root():
    """ルートエンドポイント（認証不要）"""
    return {
        "message": "FastAPI JWT認証サンプル",
        "endpoints": {
            "public": [
                "POST /register - ユーザー登録",
                "POST /token - トークン取得（OAuth2形式）",
                "POST /login - ログイン（JSON形式）"
            ],
            "protected": [
                "GET /users/me - 現在のユーザー情報",
                "GET /users/me/items - ユーザーのアイテム",
                "GET /protected - 基本的な保護されたエンドポイント"
            ],
            "permission_based": [
                "GET /read-data - 読み取り権限必要",
                "POST /write-data - 書き込み権限必要",
                "GET /admin - 管理者権限必要"
            ]
        },
        "sample_users": [
            {"username": "admin", "password": "admin123",
                "scopes": ["read", "write", "admin"]},
            {"username": "user1", "password": "user123", "scopes": ["read"]},
            {"username": "editor", "password": "editor123",
                "scopes": ["read", "write"]}
        ]
    }


@app.get("/public")
async def public_endpoint():
    """パブリックエンドポイント（認証不要）"""
    return {
        "message": "このエンドポイントは認証不要です",
        "timestamp": datetime.now().isoformat(),
        "note": "誰でもアクセスできます"
    }


@app.get("/verify-token")
async def verify_token_endpoint(token: str):
    """トークン検証エンドポイント（デバッグ用）"""
    try:
        token_data = verify_token(token)
        user = None
        if token_data.username:
            user = get_user(token_data.username)

        return {
            "valid": True,
            "token_data": {
                "username": token_data.username,
                "scopes": token_data.scopes
            },
            "user_exists": user is not None
        }
    except HTTPException as e:
        return {
            "valid": False,
            "error": e.detail
        }

# ===== 使用方法の説明 =====


@app.get("/usage-guide")
async def usage_guide():
    """JWT認証の使用方法ガイド"""
    return {
        "title": "JWT認証の使用方法",
        "steps": [
            {
                "step": 1,
                "action": "ユーザー登録またはログイン",
                "endpoints": [
                    "POST /register - 新規ユーザー登録",
                    "POST /token - OAuth2形式でログイン",
                    "POST /login - JSON形式でログイン"
                ]
            },
            {
                "step": 2,
                "action": "トークンを取得",
                "description": "レスポンスのaccess_tokenを保存"
            },
            {
                "step": 3,
                "action": "保護されたエンドポイントにアクセス",
                "description": "Authorizationヘッダーに 'Bearer {token}' を設定"
            }
        ],
        "examples": {
            "curl_login": "curl -X POST 'http://localhost:8011/login' -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'",
            "curl_protected": "curl -X GET 'http://localhost:8011/protected' -H 'Authorization: Bearer YOUR_TOKEN_HERE'"
        },
        "swagger_ui": {
            "url": "/docs",
            "description": "Swagger UIでAuthorizeボタンをクリックしてトークンを設定"
        }
    }

# ===== 実行例 =====

if __name__ == "__main__":
    import uvicorn

    print("FastAPI JWT認証サンプル")
    print("=" * 40)
    print("このサンプルでは以下を学習します:")
    print("1. JWT トークンの生成・検証")
    print("2. ユーザー認証・登録")
    print("3. 保護されたエンドポイント")
    print("4. 権限（スコープ）ベースのアクセス制御")
    print("\nサンプルユーザー:")
    print("- admin / admin123 (権限: read, write, admin)")
    print("- user1 / user123 (権限: read)")
    print("- editor / editor123 (権限: read, write)")
    print("\nサーバーを起動します...")
    print("ブラウザで http://localhost:8011/docs にアクセスして")
    print("Authorizeボタンでトークン認証をテストしてください。")
    print("\nCtrl+C で停止")
    print("=" * 40)

    uvicorn.run(app, host="0.0.0.0", port=8011)
