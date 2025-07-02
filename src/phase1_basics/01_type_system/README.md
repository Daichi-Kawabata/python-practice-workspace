# 01. 型システム・型ヒント

## 学習項目
- 基本型（int, str, bool, float）
- コレクション型（List, Dict, Set, Tuple）
- Union、Optional、Callable
- ジェネリック型（TypeVar, Generic[T]）
- dataclass、frozen、__post_init__
- 変数の型ヒント使い分け

## ファイル構成

### `type_hints.py`
- 基本的な型ヒントから高度なジェネリック型まで
- dataclassの実践例
- Ruby/Golangとの比較

### `variable_type_hints.py`
- 変数宣言での型ヒント使い分け
- Final、ClassVar
- 型チェックツール（mypy）の活用

## 学習のポイント
1. **型安全性**: 実行時エラーを事前に発見
2. **可読性**: コードの意図を明確に表現
3. **IDE支援**: 自動補完・リファクタリングの向上
4. **ドキュメント**: 型情報がドキュメントとして機能

## 次のステップ
型ヒントを理解したら、OOPでのクラス設計に進みましょう。
クラス定義時の型ヒント活用が重要になります。
