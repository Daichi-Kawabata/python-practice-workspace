"""
JSON操作の学習

JSONファイルの読み書き、データの変換・バリデーション・操作を学習します。
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, date
import re


@dataclass
class User:
    """ユーザーデータクラス"""
    id: int
    name: str
    email: str
    age: int
    city: str
    hobbies: List[str]
    active: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """辞書からインスタンスを作成"""
        return cls(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            age=data['profile']['age'],
            city=data['profile']['city'],
            hobbies=data['profile']['hobbies'],
            active=data['active']
        )


def basic_json_reading():
    """基本的なJSON読み込み"""
    print("=== 基本的なJSON読み込み ===")
    
    json_file = Path("../sample_data/users.json")
    
    # 1. JSON全体を読み込み
    print("1. JSON全体を読み込み:")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"データ型: {type(data)}")
            print(f"キー: {list(data.keys())}")
            print(f"メタデータ: {data['metadata']}")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {json_file}")
    except json.JSONDecodeError as e:
        print(f"JSON解析エラー: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. ユーザーデータの取得
    print("2. ユーザーデータの取得:")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            users = data['users']
            
            print(f"ユーザー数: {len(users)}人")
            for user in users:
                print(f"  ID: {user['id']}, 名前: {user['name']}")
                print(f"    年齢: {user['profile']['age']}歳, 都市: {user['profile']['city']}")
                print(f"    趣味: {', '.join(user['profile']['hobbies'])}")
                print(f"    アクティブ: {user['active']}")
                print()
                
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {json_file}")


def json_to_dataclass():
    """JSONデータをデータクラスに変換"""
    print("=== JSONデータをデータクラスに変換 ===")
    
    json_file = Path("../sample_data/users.json")
    users: List[User] = []
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for user_data in data['users']:
                user = User.from_dict(user_data)
                users.append(user)
        
        print(f"読み込み完了: {len(users)}人のユーザーデータ")
        for user in users:
            print(f"  {user}")
            
        return users
        
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {json_file}")
        return []
    except KeyError as e:
        print(f"必要なキーが見つかりません: {e}")
        return []


def json_data_manipulation(users: List[User]):
    """JSONデータの操作・分析"""
    print("=== JSONデータの操作・分析 ===")
    
    if not users:
        print("データがありません")
        return
    
    # 1. 基本統計
    print("1. 基本統計:")
    ages = [user.age for user in users]
    active_users = [user for user in users if user.active]
    
    print(f"  総ユーザー数: {len(users)}人")
    print(f"  アクティブユーザー: {len(active_users)}人")
    print(f"  平均年齢: {sum(ages) / len(ages):.1f}歳")
    print(f"  最年少: {min(ages)}歳")
    print(f"  最年長: {max(ages)}歳")
    
    # 2. 都市別分析
    print("\n2. 都市別分析:")
    city_count: Dict[str, int] = {}
    for user in users:
        city_count[user.city] = city_count.get(user.city, 0) + 1
    
    for city, count in city_count.items():
        print(f"  {city}: {count}人")
    
    # 3. 趣味の分析
    print("\n3. 趣味の分析:")
    all_hobbies: List[str] = []
    for user in users:
        all_hobbies.extend(user.hobbies)
    
    hobby_count: Dict[str, int] = {}
    for hobby in all_hobbies:
        hobby_count[hobby] = hobby_count.get(hobby, 0) + 1
    
    # 人気順にソート
    sorted_hobbies = sorted(hobby_count.items(), key=lambda x: x[1], reverse=True)
    for hobby, count in sorted_hobbies:
        print(f"  {hobby}: {count}人")
    
    # 4. フィルタリング
    print("\n4. データフィルタリング:")
    
    # 30歳以上のアクティブユーザー
    senior_active = [user for user in users if user.age >= 30 and user.active]
    print(f"  30歳以上のアクティブユーザー: {len(senior_active)}人")
    for user in senior_active:
        print(f"    {user.name} ({user.age}歳, {user.city})")
    
    # プログラミングが趣味のユーザー
    programmers = [user for user in users if "プログラミング" in user.hobbies]
    print(f"  プログラミングが趣味: {len(programmers)}人")
    for user in programmers:
        print(f"    {user.name}")


def json_writing_operations():
    """JSON書き込み操作"""
    print("=== JSON書き込み操作 ===")
    
    # 1. 新しいJSONデータの作成
    print("1. 新しいJSONデータの作成:")
    
    new_users = [
        User(
            id=4,
            name="林大輝",
            email="hayashi@example.com",
            age=27,
            city="京都",
            hobbies=["写真", "旅行", "カフェ巡り"],
            active=True
        ),
        User(
            id=5,
            name="森美穂",
            email="mori@example.com",
            age=24,
            city="神戸",
            hobbies=["読書", "映画鑑賞", "ヨガ"],
            active=False
        )
    ]
    
    # データクラスを辞書に変換
    users_data = [user.to_dict() for user in new_users]
    
    # JSON形式で出力
    output_data = {
        "users": users_data,
        "metadata": {
            "total_count": len(users_data),
            "created_at": datetime.now().isoformat(),
            "version": "2.0"
        }
    }
    
    output_file = Path("new_users.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"ファイル '{output_file}' を作成しました")
    
    # 2. 美しいJSON出力
    print("\n2. 美しいJSON出力:")
    print(json.dumps(output_data, ensure_ascii=False, indent=2))
    
    # 3. 作成したファイルの確認
    print("\n3. 作成したファイルの確認:")
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    
    # 4. ファイル削除（クリーンアップ）
    if output_file.exists():
        output_file.unlink()
        print(f"\nファイル '{output_file}' を削除しました")


def json_data_transformation():
    """JSONデータの変換・加工"""
    print("=== JSONデータの変換・加工 ===")
    
    json_file = Path("../sample_data/users.json")
    
    try:
        # 元データを読み込み
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"元データ: {len(data['users'])}人のユーザー")
        
        # データの変換・加工
        transformed_users = []
        for user_data in data['users']:
            user = user_data.copy()
            profile = user['profile']
            
            # 年齢グループを追加
            age = profile['age']
            if age < 25:
                age_group = "若年層"
            elif age < 35:
                age_group = "中年層"
            else:
                age_group = "シニア層"
            
            # 趣味数を追加
            hobby_count = len(profile['hobbies'])
            
            # メールドメインを追加
            email_domain = user['email'].split('@')[1]
            
            # 変換されたユーザーデータ
            transformed_user = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'email_domain': email_domain,
                'age': age,
                'age_group': age_group,
                'city': profile['city'],
                'hobbies': profile['hobbies'],
                'hobby_count': hobby_count,
                'active': user['active'],
                'last_updated': datetime.now().isoformat()
            }
            transformed_users.append(transformed_user)
        
        # 変換後データの表示
        print("\n変換後データ:")
        for user in transformed_users:
            print(f"  {user['name']} ({user['age_group']})")
            print(f"    趣味数: {user['hobby_count']}個, ドメイン: {user['email_domain']}")
        
        # 変換後データをJSONに保存
        output_data = {
            "users": transformed_users,
            "summary": {
                "total_users": len(transformed_users),
                "active_users": sum(1 for u in transformed_users if u['active']),
                "average_hobbies": sum(u['hobby_count'] for u in transformed_users) / len(transformed_users),
                "processed_at": datetime.now().isoformat()
            }
        }
        
        output_file = Path("transformed_users.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n変換後データを '{output_file}' に保存しました")
        
        # サマリー表示
        print(f"\nサマリー:")
        print(f"  総ユーザー数: {output_data['summary']['total_users']}人")
        print(f"  アクティブユーザー: {output_data['summary']['active_users']}人")
        print(f"  平均趣味数: {output_data['summary']['average_hobbies']:.1f}個")
        
        # クリーンアップ
        if output_file.exists():
            output_file.unlink()
            print(f"\nファイル '{output_file}' を削除しました")
        
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {json_file}")
    except json.JSONDecodeError as e:
        print(f"JSON解析エラー: {e}")


def json_validation_and_schema():
    """JSON データのバリデーションとスキーマ検証"""
    print("=== JSONデータのバリデーション ===")
    
    def validate_user_data(user_data: Dict[str, Any]) -> List[str]:
        """ユーザーデータのバリデーション"""
        errors = []
        
        # 必須フィールドの確認
        required_fields = ['id', 'name', 'email', 'profile', 'active']
        for field in required_fields:
            if field not in user_data:
                errors.append(f"必須フィールド '{field}' がありません")
        
        # データ型の確認
        if 'id' in user_data and not isinstance(user_data['id'], int):
            errors.append("'id' は整数である必要があります")
        
        if 'name' in user_data and not isinstance(user_data['name'], str):
            errors.append("'name' は文字列である必要があります")
        
        # メールアドレスの形式確認
        if 'email' in user_data:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, user_data['email']):
                errors.append("'email' の形式が正しくありません")
        
        # プロファイルの確認
        if 'profile' in user_data:
            profile = user_data['profile']
            profile_required = ['age', 'city', 'hobbies']
            for field in profile_required:
                if field not in profile:
                    errors.append(f"プロファイルに '{field}' がありません")
            
            # 年齢の範囲確認
            if 'age' in profile:
                age = profile['age']
                if not isinstance(age, int) or age < 0 or age > 120:
                    errors.append("'age' は0-120の整数である必要があります")
            
            # 趣味がリストか確認
            if 'hobbies' in profile and not isinstance(profile['hobbies'], list):
                errors.append("'hobbies' はリストである必要があります")
        
        return errors
    
    # テストデータでバリデーション
    test_data = [
        {
            "id": 1,
            "name": "山田太郎",
            "email": "yamada@example.com",
            "profile": {
                "age": 30,
                "city": "東京",
                "hobbies": ["読書", "映画"]
            },
            "active": True
        },
        {
            "id": "invalid",  # エラー: 文字列
            "name": "田中花子",
            "email": "invalid-email",  # エラー: 不正な形式
            "profile": {
                "age": 150,  # エラー: 範囲外
                "city": "大阪"
                # エラー: hobbies がない
            },
            "active": True
        }
    ]
    
    print("バリデーション結果:")
    for i, user_data in enumerate(test_data, 1):
        print(f"\nユーザー {i}:")
        errors = validate_user_data(user_data)
        if errors:
            print("  エラー:")
            for error in errors:
                print(f"    - {error}")
        else:
            print("  ✅ バリデーション成功")


def advanced_json_operations():
    """高度なJSON操作"""
    print("=== 高度なJSON操作 ===")
    
    # 1. ネストしたJSONの操作
    print("1. ネストしたJSONの操作:")
    complex_data = {
        "company": {
            "name": "テック株式会社",
            "departments": [
                {
                    "name": "開発部",
                    "employees": [
                        {"name": "田中", "role": "エンジニア", "skills": ["Python", "JavaScript"]},
                        {"name": "佐藤", "role": "デザイナー", "skills": ["Figma", "Photoshop"]}
                    ]
                },
                {
                    "name": "営業部",
                    "employees": [
                        {"name": "山田", "role": "営業", "skills": ["交渉", "プレゼン"]}
                    ]
                }
            ]
        }
    }
    
    # 全従業員のスキル一覧を取得
    all_skills = []
    for dept in complex_data["company"]["departments"]:
        for emp in dept["employees"]:
            all_skills.extend(emp["skills"])
    
    unique_skills = list(set(all_skills))
    print(f"  全スキル: {unique_skills}")
    
    # 2. JSON Path的なアクセス
    print("\n2. 深いネスト構造への安全なアクセス:")
    
    def safe_get(data: Dict[str, Any], path: str, default=None):
        """安全にネストした値を取得"""
        keys = path.split('.')
        current = data
        
        try:
            for key in keys:
                if '[' in key and ']' in key:
                    # 配列インデックスの処理
                    array_key, index_str = key.split('[')
                    index = int(index_str.rstrip(']'))
                    current = current[array_key][index]
                else:
                    current = current[key]
            return current
        except (KeyError, IndexError, ValueError):
            return default
    
    # 使用例
    company_name = safe_get(complex_data, "company.name")
    first_dept_name = safe_get(complex_data, "company.departments[0].name")
    nonexistent = safe_get(complex_data, "company.nonexistent.field", "デフォルト値")
    
    print(f"  会社名: {company_name}")
    print(f"  最初の部署: {first_dept_name}")
    print(f"  存在しないフィールド: {nonexistent}")


if __name__ == "__main__":
    print("フェーズ2-01: JSON操作の学習\n")
    
    basic_json_reading()
    print("\n" + "="*60 + "\n")
    
    users = json_to_dataclass()
    print("\n" + "="*60 + "\n")
    
    json_data_manipulation(users)
    print("\n" + "="*60 + "\n")
    
    json_writing_operations()
    print("\n" + "="*60 + "\n")
    
    json_data_transformation()
    print("\n" + "="*60 + "\n")
    
    json_validation_and_schema()
    print("\n" + "="*60 + "\n")
    
    advanced_json_operations()
    
    print("\n学習完了！次は Webスクレイピングに進みましょう。")
