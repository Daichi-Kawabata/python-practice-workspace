"""
Alembicマイグレーション実習課題

このファイルでは、Alembicを使用したデータベーススキーマの変更管理を学習します。
実際のプロジェクトでよく行われるマイグレーション操作を体験できます。

実習内容：
1. 新しいテーブルの追加
2. 既存テーブルへのカラム追加
3. インデックスの作成
4. マイグレーションの実行とロールバック
"""

import os
import subprocess
from datetime import datetime
from typing import List, Optional


class AlembicPractice:
    """Alembicマイグレーション実習クラス"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.dirname(self.base_dir)
        
    def run_alembic_command(self, command: str) -> tuple[bool, str]:
        """
        Alembicコマンドを実行する
        
        Args:
            command: 実行するAlembicコマンド
            
        Returns:
            (成功フラグ, 出力メッセージ)
        """
        try:
            # プロジェクトディレクトリに移動してコマンド実行
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            print(f"🔧 コマンド実行: {command}")
            print(f"📋 結果: {'成功' if success else '失敗'}")
            print(f"📄 出力:\n{output}")
            
            return success, output
            
        except Exception as e:
            error_msg = f"コマンド実行エラー: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def check_current_revision(self) -> Optional[str]:
        """
        現在のリビジョンを確認
        
        Returns:
            現在のリビジョンID、エラー時はNone
        """
        success, output = self.run_alembic_command("alembic current")
        if success:
            # 出力からリビジョンIDを抽出
            lines = output.strip().split('\n')
            for line in lines:
                if 'INFO' not in line and line.strip():
                    return line.strip()
        return None
    
    def show_migration_history(self) -> bool:
        """
        マイグレーション履歴を表示
        
        Returns:
            成功フラグ
        """
        print("\n📚 マイグレーション履歴:")
        success, output = self.run_alembic_command("alembic history --verbose")
        return success
    
    def create_migration(self, message: str, auto_generate: bool = True) -> bool:
        """
        新しいマイグレーションを作成
        
        Args:
            message: マイグレーションのメッセージ
            auto_generate: 自動生成するかどうか
            
        Returns:
            成功フラグ
        """
        command = f"alembic revision"
        if auto_generate:
            command += " --autogenerate"
        command += f" -m \"{message}\""
        
        success, output = self.run_alembic_command(command)
        return success
    
    def upgrade_database(self, revision: str = "head") -> bool:
        """
        データベースをアップグレード
        
        Args:
            revision: アップグレード先のリビジョン（デフォルトは最新）
            
        Returns:
            成功フラグ
        """
        success, output = self.run_alembic_command(f"alembic upgrade {revision}")
        return success
    
    def downgrade_database(self, revision: str = "-1") -> bool:
        """
        データベースをダウングレード
        
        Args:
            revision: ダウングレード先のリビジョン（デフォルトは1つ前）
            
        Returns:
            成功フラグ
        """
        success, output = self.run_alembic_command(f"alembic downgrade {revision}")
        return success


def practice_1_add_new_table():
    """
    実習1: 新しいテーブルの追加
    
    課題: Commentテーブルを追加するマイグレーションを作成・実行
    """
    print("\n🎯 実習1: 新しいテーブルの追加")
    print("=" * 50)
    
    # まず、models.pyにCommentモデルを追加する必要があります
    print("📝 手順:")
    print("1. models.pyにCommentモデルを追加")
    print("2. マイグレーションファイルを生成")
    print("3. マイグレーションを実行")
    
    # ここでは実際のテーブル追加は行わず、手順の説明のみ
    print("\n💡 Commentモデルの例:")
    print("""
class Comment(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    author_email: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # 外部キー: 記事への参照
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    
    # リレーション
    post = relationship("Post", back_populates="comments")
    """)
    
    alembic = AlembicPractice()
    
    # 現在の状態確認
    current = alembic.check_current_revision()
    print(f"\n📍 現在のリビジョン: {current}")
    
    # 履歴表示
    alembic.show_migration_history()
    
    return alembic


def practice_2_add_column():
    """
    実習2: 既存テーブルへのカラム追加
    
    課題: Userテーブルにprofile_imageカラムを追加
    """
    print("\n🎯 実習2: 既存テーブルへのカラム追加")
    print("=" * 50)
    
    print("📝 手順:")
    print("1. models.pyのUserモデルにprofile_imageカラムを追加")
    print("2. マイグレーションファイルを生成")
    print("3. マイグレーションを実行")
    
    print("\n💡 追加するカラムの例:")
    print("""
# Userモデルに追加
profile_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    """)
    
    alembic = AlembicPractice()
    
    # 実際にカラム追加のマイグレーションを作成してみる
    print("\n🔧 マイグレーション作成の実演:")
    
    # 注意: この段階ではmodels.pyを実際に変更していないため、
    # 実際にはマイグレーションファイルは生成されない
    
    return alembic


def practice_3_create_index():
    """
    実習3: インデックスの作成
    
    課題: パフォーマンス向上のためのインデックスを追加
    """
    print("\n🎯 実習3: インデックスの作成")
    print("=" * 50)
    
    print("📝 手順:")
    print("1. インデックスが必要なカラムを特定")
    print("2. 手動でマイグレーションファイルを作成")
    print("3. インデックス作成のDDLを記述")
    print("4. マイグレーションを実行")
    
    print("\n💡 インデックス作成の例:")
    print("""
# マイグレーションファイル内で
def upgrade():
    # 複合インデックスの作成
    op.create_index(
        'idx_posts_author_created', 
        'posts', 
        ['author_id', 'created_at']
    )
    
    # 単一カラムインデックスの作成
    op.create_index(
        'idx_posts_published_at', 
        'posts', 
        ['published_at']
    )

def downgrade():
    # インデックスの削除
    op.drop_index('idx_posts_published_at', table_name='posts')
    op.drop_index('idx_posts_author_created', table_name='posts')
    """)
    
    alembic = AlembicPractice()
    return alembic


def practice_4_rollback():
    """
    実習4: マイグレーションの実行とロールバック
    
    課題: マイグレーションの前進と後退を体験
    """
    print("\n🎯 実習4: マイグレーションの実行とロールバック")
    print("=" * 50)
    
    print("📝 手順:")
    print("1. 現在のリビジョンを確認")
    print("2. マイグレーションを実行 (upgrade)")
    print("3. データベースの状態を確認")
    print("4. ロールバックを実行 (downgrade)")
    print("5. データベースの状態を再確認")
    
    alembic = AlembicPractice()
    
    # 現在の状態確認
    current = alembic.check_current_revision()
    print(f"\n📍 現在のリビジョン: {current}")
    
    # 履歴表示
    alembic.show_migration_history()
    
    print("\n💡 よく使うコマンド:")
    print("- alembic upgrade head     # 最新までアップグレード")
    print("- alembic upgrade +1       # 1つ進む")
    print("- alembic downgrade -1     # 1つ戻る")
    print("- alembic downgrade base   # 最初まで戻る")
    print("- alembic current          # 現在のリビジョン")
    print("- alembic history          # 履歴表示")
    
    return alembic


def main():
    """メイン実習関数"""
    print("🔧 Alembicマイグレーション実習")
    print("=" * 60)
    
    print("\n📖 Alembicとは:")
    print("- SQLAlchemyのマイグレーションツール")
    print("- データベーススキーマの変更を管理")
    print("- バージョン管理とロールバック機能")
    print("- チーム開発での整合性を保つ")
    
    # 各実習を順番に実行
    practice_1_add_new_table()
    practice_2_add_column()
    practice_3_create_index()
    practice_4_rollback()
    
    print("\n✅ 実習完了")
    print("\n📚 次のステップ:")
    print("1. 実際にmodels.pyを変更してマイグレーションを体験")
    print("2. 本番環境でのマイグレーション戦略を学習")
    print("3. データマイグレーション（データの移行）を学習")
    print("4. 複雑なスキーマ変更（テーブル名変更、カラム型変更）を学習")


if __name__ == "__main__":
    main()
