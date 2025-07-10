from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash, verify_password
from typing import Optional


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """IDでユーザーを取得"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """ユーザー名でユーザーを取得"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """メールアドレスでユーザーを取得"""
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """ユーザー認証"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, user: UserCreate) -> User:
    """ユーザーを作成"""
    # 重複チェック
    existing_user = db.query(User).filter(
        or_(User.username == user.username, User.email == user.email)
    ).first()

    if existing_user:
        if existing_user.username == user.username:
            raise ValueError("ユーザー名が既に存在します")
        if existing_user.email == user.email:
            raise ValueError("メールアドレスが既に存在します")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
