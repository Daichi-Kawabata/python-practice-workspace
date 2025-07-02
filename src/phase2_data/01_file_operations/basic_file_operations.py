"""
基本的なファイル操作の学習

フェーズ1で学んだファイル操作を発展させ、より幅広い操作を学習します。
"""

from pathlib import Path
from typing import List, Optional
import os


def basic_text_file_operations():
    """基本的なテキストファイルの読み書き"""
    print("=== 基本的なテキストファイル操作 ===")
    
    # サンプルファイルのパス
    sample_file = Path("../sample_data/sample.txt")
    
    # 1. ファイル全体を読み込み
    print("1. ファイル全体を読み込み:")
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {sample_file}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. 行ごとに読み込み
    print("2. 行ごとに読み込み:")
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                print(f"行{line_num}: {line.rstrip()}")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {sample_file}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. すべての行をリストとして読み込み
    print("3. すべての行をリストとして読み込み:")
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"総行数: {len(lines)}")
            for i, line in enumerate(lines):
                print(f"  [{i}] {repr(line)}")  # repr()で改行文字も表示
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {sample_file}")


def file_writing_operations():
    """ファイル書き込み操作"""
    print("=== ファイル書き込み操作 ===")
    
    output_file = Path("output.txt")
    
    # 1. 新規ファイル作成・上書き
    print("1. 新規ファイル作成:")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("新しいファイルです。\n")
        f.write("日本語も書けます。\n")
        f.write(f"現在時刻の情報などを含めることもできます。\n")
    
    print(f"ファイル '{output_file}' を作成しました。")
    
    # 2. ファイルに追記
    print("2. ファイルに追記:")
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write("追記された内容です。\n")
        f.write("append モードで書き込みました。\n")
    
    # 3. 作成したファイルを確認
    print("3. 作成したファイルの内容:")
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    
    # 4. ファイル削除（クリーンアップ）
    if output_file.exists():
        output_file.unlink()
        print(f"ファイル '{output_file}' を削除しました。")


def pathlib_examples():
    """pathlibによるモダンなパス操作"""
    print("=== pathlib によるパス操作 ===")
    
    # 1. パスの作成
    current_dir = Path.cwd()
    sample_dir = Path("../sample_data")
    sample_file = sample_dir / "sample.txt"
    
    print(f"現在のディレクトリ: {current_dir}")
    print(f"サンプルディレクトリ: {sample_dir}")
    print(f"サンプルファイル: {sample_file}")
    print(f"絶対パス: {sample_file.resolve()}")
    
    # 2. パスの情報
    print(f"\nパス情報:")
    print(f"  親ディレクトリ: {sample_file.parent}")
    print(f"  ファイル名: {sample_file.name}")
    print(f"  拡張子: {sample_file.suffix}")
    print(f"  拡張子なしのファイル名: {sample_file.stem}")
    
    # 3. ファイル・ディレクトリの存在確認
    print(f"\n存在確認:")
    print(f"  ファイルが存在する: {sample_file.exists()}")
    print(f"  ディレクトリである: {sample_file.is_dir()}")
    print(f"  ファイルである: {sample_file.is_file()}")
    
    # 4. ディレクトリ内のファイル一覧
    print(f"\nディレクトリ内のファイル:")
    if sample_dir.exists():
        for item in sample_dir.iterdir():
            file_type = "ディレクトリ" if item.is_dir() else "ファイル"
            print(f"  {item.name} ({file_type})")


def error_handling_examples():
    """ファイル操作のエラーハンドリング"""
    print("=== エラーハンドリングの例 ===")
    
    # 1. 存在しないファイルの処理
    print("1. 存在しないファイルの処理:")
    non_existent_file = Path("存在しないファイル.txt")
    
    try:
        with open(non_existent_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"  エラー: ファイルが見つかりません - {e}")
    except PermissionError as e:
        print(f"  エラー: アクセス権限がありません - {e}")
    except Exception as e:
        print(f"  予期しないエラー: {e}")
    
    # 2. 安全なファイル読み込み関数
    def safe_read_file(file_path: Path) -> Optional[str]:
        """安全にファイルを読み込む関数"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"警告: ファイル '{file_path}' が見つかりません")
            return None
        except PermissionError:
            print(f"エラー: ファイル '{file_path}' の読み込み権限がありません")
            return None
        except UnicodeDecodeError:
            print(f"エラー: ファイル '{file_path}' の文字エンコーディングが不正です")
            return None
    
    print("2. 安全なファイル読み込み:")
    content = safe_read_file(Path("../sample_data/sample.txt"))
    if content:
        print(f"  読み込み成功: {len(content)} 文字")
    else:
        print("  読み込み失敗")


if __name__ == "__main__":
    print("フェーズ2-01: 基本的なファイル操作\n")
    
    basic_text_file_operations()
    print("\n" + "="*60 + "\n")
    
    file_writing_operations()
    print("\n" + "="*60 + "\n")
    
    pathlib_examples()
    print("\n" + "="*60 + "\n")
    
    error_handling_examples()
    
    print("\n学習完了！次は CSV操作に進みましょう。")
