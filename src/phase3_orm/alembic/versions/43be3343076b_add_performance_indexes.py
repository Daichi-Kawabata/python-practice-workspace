"""Add performance indexes

Revision ID: 43be3343076b
Revises: 0e97c7df4b37
Create Date: 2025-07-07 13:30:34.505719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43be3343076b'
down_revision: Union[str, Sequence[str], None] = '0e97c7df4b37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 複合インデックスの作成
    op.create_index(
        'idx_comments_post_created',
        'comments',
        ['post_id', 'created_at']
    )

    # 単一カラムインデックスの作成
    op.create_index(
        'idx_comments_approved',
        'comments',
        ['is_approved']
    )

    # 記事の公開日時インデックス
    op.create_index(
        'idx_posts_published_at',
        'posts',
        ['published_at']
    )

    # ユーザーの最終ログイン日時インデックス
    op.create_index(
        'idx_users_last_login',
        'users',
        ['last_login']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # インデックスの削除（作成と逆順）
    op.drop_index('idx_users_last_login', table_name='users')
    op.drop_index('idx_posts_published_at', table_name='posts')
    op.drop_index('idx_comments_approved', table_name='comments')
    op.drop_index('idx_comments_post_created', table_name='comments')
