"""
pandas基礎操作

データ分析の基本的な操作を学習します。
- DataFrame/Seriesの作成と操作
- データの読み込み・保存
- データの選択・フィルタリング
- 基本的な統計情報の取得
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import warnings

# matplotlib日本語対応
plt.rcParams['font.family'] = 'DejaVu Sans'
warnings.filterwarnings('ignore')

def create_sample_data() -> None:
    """サンプルデータの作成"""
    print("=== サンプルデータの作成 ===")
    
    # 1. Series（1次元データ）の作成
    print("1. Seriesの作成:")
    
    # リストからSeriesを作成
    numbers = pd.Series([1, 2, 3, 4, 5])
    print(f"数値Series:\n{numbers}")
    
    # 辞書からSeriesを作成
    grades = pd.Series({
        '数学': 85,
        '英語': 92,
        '国語': 78,
        '理科': 90,
        '社会': 88
    })
    print(f"\n成績Series:\n{grades}")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. DataFrame（2次元データ）の作成
    print("2. DataFrameの作成:")
    
    # 辞書からDataFrameを作成
    students_data = {
        '名前': ['田中太郎', '佐藤花子', '鈴木一郎', '高橋美咲', '山田次郎'],
        '年齢': [20, 19, 21, 20, 22],
        '学部': ['工学部', '文学部', '理学部', '経済学部', '法学部'],
        '数学': [85, 92, 78, 90, 88],
        '英語': [78, 88, 85, 92, 75],
        '国語': [90, 85, 88, 87, 92]
    }
    
    df = pd.DataFrame(students_data)
    print(f"学生データFrame:\n{df}")
    print(f"\nDataFrameの形状: {df.shape}")
    print(f"データ型:\n{df.dtypes}")
    
    # CSVファイルに保存
    output_path = Path("students_data.csv")
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nデータを {output_path} に保存しました")


def data_selection_and_filtering() -> None:
    """データの選択とフィルタリング"""
    print("=== データの選択とフィルタリング ===")
    
    # サンプルデータの作成
    data = {
        'ID': range(1, 11),
        '名前': ['田中', '佐藤', '鈴木', '高橋', '山田', '渡辺', '伊藤', '小林', '中村', '加藤'],
        '年齢': [25, 30, 35, 28, 42, 33, 29, 31, 27, 38],
        '部署': ['営業', '開発', '営業', '開発', '総務', '開発', '営業', '総務', '開発', '営業'],
        '給与': [350000, 450000, 380000, 480000, 420000, 500000, 360000, 440000, 470000, 390000]
    }
    
    df = pd.DataFrame(data)
    print(f"従業員データ:\n{df}")
    
    print("\n" + "-"*30 + "\n")
    
    # 1. 列の選択
    print("1. 列の選択:")
    print(f"名前列:\n{df['名前']}")
    print(f"\n複数列（名前・年齢）:\n{df[['名前', '年齢']]}")
    
    print("\n" + "-"*30 + "\n")
    
    # 2. 行の選択
    print("2. 行の選択:")
    print(f"最初の3行:\n{df.head(3)}")
    print(f"\n最後の2行:\n{df.tail(2)}")
    print(f"\n2-4行目:\n{df.iloc[1:4]}")
    
    print("\n" + "-"*30 + "\n")
    
    # 3. 条件によるフィルタリング
    print("3. 条件によるフィルタリング:")
    
    # 年齢が30歳以上
    age_filter = df['年齢'] >= 30
    print(f"30歳以上の従業員:\n{df[age_filter]}")
    
    # 開発部署
    dept_filter = df['部署'] == '開発'
    print(f"\n開発部署の従業員:\n{df[dept_filter]}")
    
    # 複数条件（AND）
    complex_filter = (df['年齢'] >= 30) & (df['部署'] == '開発')
    print(f"\n30歳以上かつ開発部署の従業員:\n{df[complex_filter]}")
    
    # 複数条件（OR）
    or_filter = (df['年齢'] >= 35) | (df['給与'] >= 450000)
    print(f"\n35歳以上または給与45万以上の従業員:\n{df[or_filter]}")
    
    # isinを使用した条件
    dept_list = ['営業', '総務']
    isin_filter = df['部署'].isin(dept_list)
    print(f"\n営業または総務部署の従業員:\n{df[isin_filter]}")


def basic_statistics() -> None:
    """基本統計情報の取得"""
    print("=== 基本統計情報の取得 ===")
    
    # サンプルデータの作成
    np.random.seed(42)
    data = {
        '商品ID': [f'P{i:03d}' for i in range(1, 101)],
        '商品名': [f'商品{i}' for i in range(1, 101)],
        'カテゴリ': np.random.choice(['電子機器', '衣料品', '食品', '書籍'], 100),
        '価格': np.random.randint(500, 10000, 100),
        '販売数': np.random.randint(1, 50, 100),
        '評価': np.random.uniform(1.0, 5.0, 100).round(1),
        '在庫': np.random.randint(0, 100, 100)
    }
    
    df = pd.DataFrame(data)
    df['売上'] = df['価格'] * df['販売数']
    
    print(f"商品データ（最初の10件）:\n{df.head(10)}")
    
    print("\n" + "-"*50 + "\n")
    
    # 1. 基本統計量
    print("1. 基本統計量:")
    print(f"データの概要:\n{df.describe()}")
    
    print("\n" + "-"*30 + "\n")
    
    # 2. 個別統計量
    print("2. 個別統計量:")
    print(f"平均価格: {df['価格'].mean():.2f}円")
    print(f"価格の中央値: {df['価格'].median():.2f}円")
    print(f"価格の標準偏差: {df['価格'].std():.2f}円")
    print(f"最高価格: {df['価格'].max()}円")
    print(f"最低価格: {df['価格'].min()}円")
    
    print("\n" + "-"*30 + "\n")
    
    # 3. カテゴリ別統計
    print("3. カテゴリ別統計:")
    category_stats = df.groupby('カテゴリ').agg({
        '価格': ['mean', 'median', 'std'],
        '販売数': ['mean', 'sum'],
        '売上': ['mean', 'sum'],
        '評価': 'mean'
    }).round(2)
    
    print(f"カテゴリ別統計:\n{category_stats}")
    
    print("\n" + "-"*30 + "\n")
    
    # 4. 値の頻度
    print("4. 値の頻度:")
    print(f"カテゴリ別商品数:\n{df['カテゴリ'].value_counts()}")
    
    # 5. 相関関係
    print("\n5. 相関関係:")
    numeric_columns = ['価格', '販売数', '評価', '在庫', '売上']
    correlation = df[numeric_columns].corr().round(3)
    print(f"相関行列:\n{correlation}")
    
    # データをCSVに保存
    output_path = Path("product_data.csv")
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n商品データを {output_path} に保存しました")


def data_cleaning_and_transformation() -> None:
    """データのクリーニングと変換"""
    print("=== データのクリーニングと変換 ===")
    
    # 欠損値を含むサンプルデータの作成
    data = {
        'ID': range(1, 11),
        '名前': ['田中', '佐藤', None, '高橋', '山田', '渡辺', '伊藤', None, '中村', '加藤'],
        '年齢': [25, 30, 35, None, 42, 33, 29, 31, None, 38],
        '部署': ['営業', '開発', '営業', '開発', None, '開発', '営業', '総務', '開発', '営業'],
        '給与': [350000, 450000, 380000, 480000, 420000, None, 360000, 440000, 470000, 390000],
        '入社日': ['2020-01-15', '2019-03-20', '2021-05-10', '2020-08-01', '2018-12-01', 
                 '2019-07-15', '2021-02-28', '2020-11-10', '2019-09-05', '2020-06-20']
    }
    
    df = pd.DataFrame(data)
    print(f"元データ（欠損値あり）:\n{df}")
    
    print("\n" + "-"*50 + "\n")
    
    # 1. 欠損値の確認
    print("1. 欠損値の確認:")
    print(f"欠損値の数:\n{df.isnull().sum()}")
    print(f"欠損値の割合:\n{(df.isnull().sum() / len(df) * 100).round(1)}%")
    
    print("\n" + "-"*30 + "\n")
    
    # 2. 欠損値の処理
    print("2. 欠損値の処理:")
    
    # 欠損値を削除
    df_dropped = df.dropna()
    print(f"欠損値削除後のデータ:\n{df_dropped}")
    
    # 欠損値を埋める
    df_filled = df.copy()
    df_filled['名前'] = df_filled['名前'].fillna('不明')
    df_filled['年齢'] = df_filled['年齢'].fillna(df_filled['年齢'].mean())
    df_filled['部署'] = df_filled['部署'].fillna('未配属')
    df_filled['給与'] = df_filled['給与'].fillna(df_filled['給与'].median())
    
    print(f"\n欠損値補完後のデータ:\n{df_filled}")
    
    print("\n" + "-"*30 + "\n")
    
    # 3. データ型の変換
    print("3. データ型の変換:")
    
    # 入社日を日付型に変換
    df_filled['入社日'] = pd.to_datetime(df_filled['入社日'])
    
    # 年齢を整数に変換
    df_filled['年齢'] = df_filled['年齢'].astype(int)
    
    print(f"データ型:\n{df_filled.dtypes}")
    
    print("\n" + "-"*30 + "\n")
    
    # 4. 新しい列の追加
    print("4. 新しい列の追加:")
    
    # 勤続年数を計算
    def calculate_years_of_service(hire_date: pd.Timestamp) -> int:
        """勤続年数を計算する型安全な関数"""
        today = pd.Timestamp.now()
        return int((today - hire_date).days // 365)
    
    df_filled['勤続年数'] = df_filled['入社日'].apply(calculate_years_of_service)
    
    # 年齢層の分類
    def categorize_age(age: int) -> str:
        if age < 30:
            return '20代'
        elif age < 40:
            return '30代'
        else:
            return '40代以上'
    
    df_filled['年齢層'] = df_filled['年齢'].apply(categorize_age)
    
    # 給与レベルの分類
    df_filled['給与レベル'] = pd.cut(df_filled['給与'], 
                                bins=[0, 400000, 450000, float('inf')],
                                labels=['低', '中', '高'])
    
    print(f"変換後のデータ:\n{df_filled}")
    
    # クリーニング済みデータを保存
    output_path = Path("cleaned_employee_data.csv")
    df_filled.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nクリーニング済みデータを {output_path} に保存しました")


def data_grouping_and_aggregation() -> None:
    """データのグループ化と集計"""
    print("=== データのグループ化と集計 ===")
    
    # サンプルデータの作成
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=365, freq='D')
    
    data = {
        '日付': np.random.choice(dates, 1000),
        '商品カテゴリ': np.random.choice(['電子機器', '衣料品', '食品', '書籍'], 1000),
        '店舗': np.random.choice(['東京店', '大阪店', '名古屋店'], 1000),
        '販売数': np.random.randint(1, 20, 1000),
        '単価': np.random.randint(100, 1000, 1000),
        '顧客年齢': np.random.randint(18, 70, 1000),
        '性別': np.random.choice(['男性', '女性'], 1000)
    }
    
    df = pd.DataFrame(data)
    df['売上'] = df['販売数'] * df['単価']
    df['月'] = df['日付'].dt.month
    df['曜日'] = df['日付'].dt.day_name()
    
    print(f"販売データ（最初の10件）:\n{df.head(10)}")
    
    print("\n" + "-"*50 + "\n")
    
    # 1. シンプルなグループ化
    print("1. シンプルなグループ化:")
    
    # カテゴリ別の売上合計
    category_sales = df.groupby('商品カテゴリ')['売上'].sum().sort_values(ascending=False)
    print(f"カテゴリ別売上合計:\n{category_sales}")
    
    # 店舗別の平均販売数
    store_avg = df.groupby('店舗')['販売数'].mean().round(2)
    print(f"\n店舗別平均販売数:\n{store_avg}")
    
    print("\n" + "-"*30 + "\n")
    
    # 2. 複数列でのグループ化
    print("2. 複数列でのグループ化:")
    
    # 店舗×カテゴリ別の売上
    store_category = df.groupby(['店舗', '商品カテゴリ'])['売上'].sum().unstack(fill_value=0)
    print(f"店舗×カテゴリ別売上:\n{store_category}")
    
    print("\n" + "-"*30 + "\n")
    
    # 3. 複数の集計関数を適用
    print("3. 複数の集計関数を適用:")
    
    multi_agg = df.groupby('商品カテゴリ').agg({
        '売上': ['sum', 'mean', 'count'],
        '販売数': ['sum', 'mean'],
        '単価': ['mean', 'min', 'max']
    }).round(2)
    
    print(f"カテゴリ別詳細統計:\n{multi_agg}")
    
    print("\n" + "-"*30 + "\n")
    
    # 4. 時系列データの集計
    print("4. 時系列データの集計:")
    
    # 月別売上
    monthly_sales = df.groupby('月')['売上'].sum().sort_index()
    print(f"月別売上:\n{monthly_sales}")
    
    # 曜日別売上（平均）
    weekday_sales = df.groupby('曜日')['売上'].mean().round(2)
    print(f"\n曜日別平均売上:\n{weekday_sales}")
    
    print("\n" + "-"*30 + "\n")
    
    # 5. 年齢層別の分析
    print("5. 年齢層別の分析:")
    
    # 年齢層を作成
    age_bins = [0, 30, 40, 50, 100]
    age_labels = ['20代', '30代', '40代', '50代以上']
    df['年齢層'] = pd.cut(df['顧客年齢'], bins=age_bins, labels=age_labels, right=False)
    
    age_analysis = df.groupby('年齢層').agg({
        '売上': ['sum', 'mean'],
        '販売数': 'sum',
        '顧客年齢': 'count'
    }).round(2)
    
    age_analysis.columns = ['売上合計', '平均売上', '販売数合計', '顧客数']
    print(f"年齢層別分析:\n{age_analysis}")
    
    # 集計結果を保存
    output_path = Path("sales_analysis.csv")
    age_analysis.to_csv(output_path, encoding='utf-8')
    print(f"\n分析結果を {output_path} に保存しました")


def data_visualization_basics() -> None:
    """データ可視化の基本"""
    print("=== データ可視化の基本 ===")
    
    # サンプルデータの作成
    np.random.seed(42)
    data = {
        '商品': ['A', 'B', 'C', 'D', 'E'],
        '売上': [1200, 800, 1500, 900, 1100],
        '利益率': [0.15, 0.12, 0.18, 0.14, 0.16]
    }
    
    df = pd.DataFrame(data)
    print(f"可視化用データ:\n{df}")
    
    print("\n可視化グラフを作成中...")
    
    # 1. 棒グラフ
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    df.plot(x='商品', y='売上', kind='bar', ax=plt.gca())
    plt.title('商品別売上')
    plt.xlabel('商品')
    plt.ylabel('売上')
    plt.xticks(rotation=0)
    
    # 2. 円グラフ
    plt.subplot(2, 2, 2)
    df.set_index('商品')['売上'].plot(kind='pie', autopct='%1.1f%%', ax=plt.gca())
    plt.title('売上構成比')
    plt.ylabel('')
    
    # 3. 散布図
    plt.subplot(2, 2, 3)
    plt.scatter(df['売上'], df['利益率'])
    plt.xlabel('売上')
    plt.ylabel('利益率')
    plt.title('売上と利益率の関係')
    
    # 4. 線グラフ
    plt.subplot(2, 2, 4)
    df.plot(x='商品', y='売上', kind='line', marker='o', ax=plt.gca())
    plt.title('売上推移')
    plt.xlabel('商品')
    plt.ylabel('売上')
    
    plt.tight_layout()
    plt.savefig('data_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("グラフを data_visualization.png に保存しました")


if __name__ == "__main__":
    print("pandas基礎操作の学習\n")
    
    create_sample_data()
    print("\n" + "="*60 + "\n")
    
    data_selection_and_filtering()
    print("\n" + "="*60 + "\n")
    
    basic_statistics()
    print("\n" + "="*60 + "\n")
    
    data_cleaning_and_transformation()
    print("\n" + "="*60 + "\n")
    
    data_grouping_and_aggregation()
    print("\n" + "="*60 + "\n")
    
    data_visualization_basics()
    
    print("\n学習完了！次は実践的なデータ分析プロジェクトに進みましょう。")
