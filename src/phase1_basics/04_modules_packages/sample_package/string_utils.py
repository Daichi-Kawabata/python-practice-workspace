"""
string_utils.py - 文字列関連のユーティリティ

文字列操作の便利なメソッドを提供
"""

import re
from typing import List, Optional, Dict, Any
import unicodedata

class StringUtil:
    """文字列ユーティリティクラス"""
    
    @staticmethod
    def reverse(text: str) -> str:
        """文字列を逆順にする"""
        return text[::-1]
    
    @staticmethod
    def is_palindrome(text: str) -> bool:
        """回文かどうかを判定"""
        # 大文字小文字を無視し、空白を除去
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
        return cleaned == cleaned[::-1]
    
    @staticmethod
    def count_words(text: str) -> int:
        """単語数をカウント"""
        return len(text.split())
    
    @staticmethod
    def count_characters(text: str, exclude_spaces: bool = False) -> int:
        """文字数をカウント"""
        if exclude_spaces:
            return len(text.replace(' ', ''))
        return len(text)
    
    @staticmethod
    def capitalize_words(text: str) -> str:
        """各単語の最初を大文字に"""
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def snake_to_camel(snake_str: str) -> str:
        """snake_case を camelCase に変換"""
        components = snake_str.split('_')
        return components[0] + ''.join(word.capitalize() for word in components[1:])
    
    @staticmethod
    def camel_to_snake(camel_str: str) -> str:
        """camelCase を snake_case に変換"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """文字列から数値を抽出"""
        return re.findall(r'\d+\.?\d*', text)
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """文字列からメールアドレスを抽出"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def remove_html_tags(html_text: str) -> str:
        """HTMLタグを除去"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html_text)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """空白文字を正規化（連続する空白を1つに）"""
        return re.sub(r'\s+', ' ', text.strip())
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """文字列を指定長で切り詰め"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def starts_with_vowel(text: str) -> bool:
        """母音で始まるかどうかを判定"""
        return text.lower().startswith(('a', 'e', 'i', 'o', 'u'))
    
    @staticmethod
    def char_frequency(text: str) -> Dict[str, int]:
        """文字の出現頻度を計算"""
        frequency = {}
        for char in text.lower():
            if char.isalpha():
                frequency[char] = frequency.get(char, 0) + 1
        return frequency
    
    @staticmethod
    def is_ascii(text: str) -> bool:
        """ASCII文字のみかどうかを判定"""
        return all(ord(char) < 128 for char in text)
    
    @staticmethod
    def normalize_unicode(text: str, form: str = 'NFC') -> str:
        """Unicode正規化"""
        # type: ignore でエラーを抑制
        return unicodedata.normalize(form, text)  # type: ignore

def levenshtein_distance(s1: str, s2: str) -> int:
    """レーベンシュタイン距離を計算"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def similarity_ratio(s1: str, s2: str) -> float:
    """文字列の類似度を0-1で返す"""
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    
    distance = levenshtein_distance(s1, s2)
    return 1.0 - (distance / max_len)

def generate_random_string(length: int, 
                         include_uppercase: bool = True,
                         include_lowercase: bool = True,
                         include_digits: bool = True,
                         include_symbols: bool = False) -> str:
    """ランダム文字列を生成"""
    import random
    import string
    
    characters = ""
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*"
    
    if not characters:
        raise ValueError("At least one character type must be included")
    
    return ''.join(random.choice(characters) for _ in range(length))
