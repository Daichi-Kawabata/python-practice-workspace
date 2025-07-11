from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db_session
from ..schemas.user import UserCreate, UserResponse
from ..schemas.token import Token
from ..crud.user import create_user, authenticate_user
from ..core.security import create_access_token
from ..core.config import settings
from ..core.dependencies import get_current_active_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db_session)):
    """ユーザー登録"""
    try:
        db_user = create_user(db=db, user=user)
        return db_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session)
) -> Token:
    """ユーザーログイン"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """現在のユーザー情報を取得"""
    return current_user
