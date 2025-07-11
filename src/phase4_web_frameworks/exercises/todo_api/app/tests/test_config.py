"""
テスト用の共通設定
"""
import sys
import os


def setup_test_environment():
    """テスト環境の設定"""
    # プロジェクトのルートディレクトリをPythonパスに追加
    project_root = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


# モジュールが読み込まれた時点で設定を実行
setup_test_environment()
