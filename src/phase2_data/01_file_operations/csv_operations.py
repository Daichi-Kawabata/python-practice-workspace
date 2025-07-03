"""
CSV操作の学習

CSVファイルの読み書き、データの変換・集計・フィルタリングを学習します。
"""

import csv
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Employee:
    """従業員データクラス"""
    name: str
    age: int
    city: str
    salary: int
    
    def __post_init__(self):
        """データクラス初期化後の処理"""
        # 型の確認・変換
        self.age = int(self.age)
        self.salary = int(self.salary)


def basic_csv_reading():
    """基本的なCSV読み込み"""
    print("=== 基本的なCSV読み込み ===")
    
    csv_file = Path("../sample_data/employees.csv")
    
    # 1. csv.reader()を使った基本的な読み込み
    print("1. csv.reader()を使った読み込み:")
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # ヘッダー行を取得
            print(f"ヘッダー: {headers}")
            
            for row_num, row in enumerate(reader, 1):
                print(f"行{row_num}: {row}")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {csv_file}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. csv.DictReader()を使った辞書形式での読み込み
    print("2. csv.DictReader()を使った読み込み:")
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            print(f"フィールド名: {reader.fieldnames}")
            
            for row_num, row in enumerate(reader, 1):
                print(f"行{row_num}: {row}")
                # 特定のフィールドにアクセス
                print(f"  名前: {row['name']}, 年齢: {row['age']}")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {csv_file}")


def csv_to_dataclass():
    """CSVデータをデータクラスに変換"""
    print("=== CSVデータをデータクラスに変換 ===")
    
    csv_file = Path("../sample_data/employees.csv")
    employees: List[Employee] = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # データクラスのインスタンスを作成
                employee = Employee(
                    name=row['name'],
                    age=int(row['age']),
                    city=row['city'],
                    salary=int(row['salary'])
                )
                employees.append(employee)
        
        print(f"読み込み完了: {len(employees)}人の従業員データ")
        for emp in employees:
            print(f"  {emp}")
            
        return employees
        
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {csv_file}")
        return []


def csv_data_analysis(employees: List[Employee]):
    """CSVデータの分析・集計"""
    print("=== CSVデータの分析・集計 ===")
    
    if not employees:
        print("データがありません")
        return
    
    # 1. 基本統計
    print("1. 基本統計:")
    ages = [emp.age for emp in employees]
    salaries = [emp.salary for emp in employees]
    
    print(f"  総従業員数: {len(employees)}人")
    print(f"  平均年齢: {sum(ages) / len(ages):.1f}歳")
    print(f"  平均給与: {sum(salaries) / len(salaries):,.0f}円")
    print(f"  最高給与: {max(salaries):,}円")
    print(f"  最低給与: {min(salaries):,}円")
    
    # 2. 都市別集計
    print("\n2. 都市別集計:")
    city_count: Dict[str, int] = {}
    city_salary: Dict[str, List[int]] = {}
    
    for emp in employees:
        # 都市別人数
        city_count[emp.city] = city_count.get(emp.city, 0) + 1
        
        # 都市別給与
        if emp.city not in city_salary:
            city_salary[emp.city] = []
        city_salary[emp.city].append(emp.salary)
    
    for city in city_count:
        avg_salary = sum(city_salary[city]) / len(city_salary[city])
        print(f"  {city}: {city_count[city]}人, 平均給与: {avg_salary:,.0f}円")
    
    # 3. フィルタリング
    print("\n3. データフィルタリング:")
    
    # 30歳以上の従業員
    senior_employees = [emp for emp in employees if emp.age >= 30]
    print(f"  30歳以上: {len(senior_employees)}人")
    for emp in senior_employees:
        print(f"    {emp.name} ({emp.age}歳)")
    
    # 高給与者（40万円以上）
    high_earners = [emp for emp in employees if emp.salary >= 400000]
    print(f"  高給与者(40万円以上): {len(high_earners)}人")
    for emp in high_earners:
        print(f"    {emp.name}: {emp.salary:,}円")


def csv_writing_operations():
    """CSV書き込み操作"""
    print("=== CSV書き込み操作 ===")
    
    # 新しいCSVファイルを作成
    output_file = Path("new_employees.csv")
    
    # 1. csv.writer()を使った書き込み
    print("1. csv.writer()を使った書き込み:")
    
    new_data = [
        ["name", "age", "city", "salary", "department"],
        ["山田太郎", 26, "東京", 350000, "開発"],
        ["田中花子", 31, "大阪", 450000, "営業"],
        ["佐藤次郎", 28, "名古屋", 400000, "開発"]
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(new_data)
    
    print(f"ファイル '{output_file}' を作成しました")
    
    # 2. csv.DictWriter()を使った書き込み
    print("2. csv.DictWriter()を使った書き込み:")
    
    dict_output_file = Path("employees_dict.csv")
    fieldnames = ["name", "age", "city", "salary", "hire_date"]
    
    employees_data = [
        {"name": "鈴木一郎", "age": 24, "city": "福岡", "salary": 320000, "hire_date": "2024-04-01"},
        {"name": "高橋美咲", "age": 29, "city": "札幌", "salary": 420000, "hire_date": "2023-10-15"},
        {"name": "渡辺健太", "age": 33, "city": "東京", "salary": 480000, "hire_date": "2022-01-20"}
    ]
    
    with open(dict_output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # ヘッダー行を書き込み
        writer.writerows(employees_data)
    
    print(f"ファイル '{dict_output_file}' を作成しました")
    
    # 3. 作成したファイルの確認
    print("\n3. 作成したファイルの確認:")
    for file_path in [output_file, dict_output_file]:
        print(f"\n  ファイル: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"  内容:\n{content}")
    
    # 4. ファイル削除（クリーンアップ）
    for file_path in [output_file, dict_output_file]:
        if file_path.exists():
            file_path.unlink()
            print(f"ファイル '{file_path}' を削除しました")


def csv_data_transformation():
    """CSVデータの変換・加工"""
    print("=== CSVデータの変換・加工 ===")
    
    csv_file = Path("../sample_data/employees.csv")
    
    try:
        # 元データを読み込み
        employees = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            employees = list(reader)
        
        print(f"元データ: {len(employees)}件")
        
        # データの変換・加工
        transformed_data = []
        for emp in employees:
            # 給与を年収に変換（月給 × 12 + ボーナス）
            monthly_salary = int(emp['salary'])
            annual_salary = monthly_salary * 12 + monthly_salary * 2  # ボーナス2ヶ月分
            
            # 年齢グループを追加
            age = int(emp['age'])
            if age < 25:
                age_group = "若手"
            elif age < 35:
                age_group = "中堅"
            else:
                age_group = "ベテラン"
            
            # 変換されたデータ
            transformed_emp = {
                'name': emp['name'],
                'age': age,
                'age_group': age_group,
                'city': emp['city'],
                'monthly_salary': monthly_salary,
                'annual_salary': annual_salary,
                'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            transformed_data.append(transformed_emp)
        
        # 変換後データの表示
        print("\n変換後データ:")
        for emp in transformed_data:
            print(f"  {emp['name']} ({emp['age_group']}): 年収 {emp['annual_salary']:,}円")
        
        # 変換後データをCSVに保存
        output_file = Path("transformed_employees.csv")
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if transformed_data:
                fieldnames = transformed_data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(transformed_data)
        
        print(f"\n変換後データを '{output_file}' に保存しました")
        
        # クリーンアップ
        if output_file.exists():
            output_file.unlink()
            print(f"ファイル '{output_file}' を削除しました")
        
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {csv_file}")


if __name__ == "__main__":
    print("フェーズ2-01: CSV操作の学習\n")
    
    basic_csv_reading()
    print("\n" + "="*60 + "\n")
    
    employees = csv_to_dataclass()
    print("\n" + "="*60 + "\n")
    
    csv_data_analysis(employees)
    print("\n" + "="*60 + "\n")
    
    csv_writing_operations()
    print("\n" + "="*60 + "\n")
    
    csv_data_transformation()
    
    print("\n学習完了！次は JSON操作に進みましょう。")
