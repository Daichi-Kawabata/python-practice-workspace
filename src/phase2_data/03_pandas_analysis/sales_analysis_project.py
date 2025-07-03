"""
実践的データ分析プロジェクト

売上データの分析とレポート作成
- 時系列分析
- 顧客セグメンテーション
- 売上予測の基礎
- レポートの自動生成
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json

# スタイル設定
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SalesAnalyzer:
    """売上分析クラス"""
    
    def __init__(self, data_path: Optional[str] = None):
        self.df: Optional[pd.DataFrame] = None
        self.analysis_results: Dict[str, Any] = {}
        
        if data_path:
            self.load_data(data_path)
        else:
            self.generate_sample_data()
    
    def generate_sample_data(self) -> None:
        """サンプルデータの生成"""
        print("サンプル売上データを生成中...")
        
        # 日付範囲（過去1年）
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # サンプルデータの作成
        np.random.seed(42)
        n_records = 5000
        
        data = {
            '日付': np.random.choice(dates, n_records),
            '顧客ID': np.random.randint(1000, 9999, n_records),
            '商品カテゴリ': np.random.choice([
                'エレクトロニクス', 'ファッション', 'ホーム&キッチン', 
                'スポーツ', '書籍', 'ビューティー'
            ], n_records),
            '商品名': [f'商品_{i}' for i in np.random.randint(1, 500, n_records)],
            '単価': np.random.randint(500, 50000, n_records),
            '数量': np.random.randint(1, 10, n_records),
            '割引率': np.random.choice([0, 0.1, 0.2, 0.3], n_records, p=[0.5, 0.3, 0.15, 0.05]),
            '地域': np.random.choice(['東京', '大阪', '名古屋', '福岡', '札幌'], n_records),
            '顧客年齢': np.random.randint(18, 70, n_records),
            '性別': np.random.choice(['男性', '女性'], n_records),
            '会員レベル': np.random.choice(['ブロンズ', 'シルバー', 'ゴールド', 'プラチナ'], 
                                   n_records, p=[0.4, 0.3, 0.2, 0.1])
        }
        
        self.df = pd.DataFrame(data)
        
        # 売上金額の計算
        self.df['売上金額'] = self.df['単価'] * self.df['数量'] * (1 - self.df['割引率'])
        
        # 日付情報の拡張
        self.df['年'] = self.df['日付'].dt.year
        self.df['月'] = self.df['日付'].dt.month
        self.df['曜日'] = self.df['日付'].dt.day_name()
        self.df['週'] = self.df['日付'].dt.isocalendar().week
        
        # 顧客年齢層の分類
        self.df['年齢層'] = pd.cut(self.df['顧客年齢'], 
                              bins=[0, 30, 40, 50, 100], 
                              labels=['20代', '30代', '40代', '50代以上'])
        
        print(f"サンプルデータを生成しました: {len(self.df)}件")
        print(f"データ期間: {self.df['日付'].min()} - {self.df['日付'].max()}")
        
        # データを保存
        output_path = Path("sales_data.csv")
        self.df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"データを {output_path} に保存しました")
    
    def load_data(self, data_path: str) -> None:
        """データの読み込み"""
        print(f"データを読み込み中: {data_path}")
        self.df = pd.read_csv(data_path, encoding='utf-8')
        self.df['日付'] = pd.to_datetime(self.df['日付'])
        print(f"データを読み込みました: {len(self.df)}件")
    
    def basic_analysis(self) -> Dict[str, Any]:
        """基本分析の実行"""
        if self.df is None:
            raise ValueError("データが読み込まれていません")
        
        print("=== 基本分析 ===")
        
        results = {}
        
        # 1. 基本統計
        results['基本統計'] = {
            '総売上金額': self.df['売上金額'].sum(),
            '平均売上金額': self.df['売上金額'].mean(),
            '取引件数': len(self.df),
            'ユニーク顧客数': self.df['顧客ID'].nunique(),
            '商品カテゴリ数': self.df['商品カテゴリ'].nunique(),
            '対象期間': f"{self.df['日付'].min()} - {self.df['日付'].max()}"
        }
        
        # 2. カテゴリ別分析
        category_analysis = self.df.groupby('商品カテゴリ').agg({
            '売上金額': ['sum', 'mean', 'count'],
            '数量': 'sum',
            '顧客ID': 'nunique'
        }).round(2)
        
        category_analysis.columns = ['総売上', '平均売上', '取引数', '総数量', 'ユニーク顧客数']
        results['カテゴリ別分析'] = category_analysis
        
        # 3. 地域別分析
        regional_analysis = self.df.groupby('地域').agg({
            '売上金額': 'sum',
            '顧客ID': 'nunique'
        }).round(2)
        
        regional_analysis.columns = ['総売上', 'ユニーク顧客数']
        results['地域別分析'] = regional_analysis
        
        # 4. 顧客セグメント分析
        customer_analysis = self.df.groupby(['年齢層', '性別', '会員レベル']).agg({
            '売上金額': ['sum', 'mean'],
            '顧客ID': 'nunique'
        }).round(2)
        
        customer_analysis.columns = ['総売上', '平均売上', 'ユニーク顧客数']
        results['顧客セグメント分析'] = customer_analysis
        
        # 結果を表示
        print(f"総売上金額: {results['基本統計']['総売上金額']:,.0f}円")
        print(f"平均売上金額: {results['基本統計']['平均売上金額']:,.0f}円")
        print(f"取引件数: {results['基本統計']['取引件数']:,}件")
        print(f"ユニーク顧客数: {results['基本統計']['ユニーク顧客数']:,}人")
        
        print("\nカテゴリ別売上（上位5位）:")
        top_categories = results['カテゴリ別分析'].sort_values('総売上', ascending=False).head()
        for category, row in top_categories.iterrows():
            print(f"  {category}: {row['総売上']:,.0f}円")
        
        self.analysis_results['基本分析'] = results
        return results
    
    def time_series_analysis(self) -> Dict[str, Any]:
        """時系列分析"""
        if self.df is None:
            raise ValueError("データが読み込まれていません")
        
        print("\n=== 時系列分析 ===")
        
        results = {}
        
        # 1. 日別売上推移
        daily_sales = self.df.groupby('日付')['売上金額'].sum().reset_index()
        daily_sales['移動平均7日'] = daily_sales['売上金額'].rolling(window=7).mean()
        daily_sales['移動平均30日'] = daily_sales['売上金額'].rolling(window=30).mean()
        
        results['日別売上'] = daily_sales
        
        # 2. 月別売上推移
        monthly_sales = self.df.groupby(['年', '月']).agg({
            '売上金額': 'sum',
            '顧客ID': 'nunique'
        }).reset_index()
        
        monthly_sales['年月'] = monthly_sales['年'].astype(str) + '-' + monthly_sales['月'].astype(str).str.zfill(2)
        results['月別売上'] = monthly_sales
        
        # 3. 曜日別パターン
        weekday_pattern = self.df.groupby('曜日').agg({
            '売上金額': ['sum', 'mean'],
            '顧客ID': 'nunique'
        }).round(2)
        
        weekday_pattern.columns = ['総売上', '平均売上', 'ユニーク顧客数']
        results['曜日別パターン'] = weekday_pattern
        
        # 4. 季節性分析
        seasonal_analysis = self.df.groupby('月').agg({
            '売上金額': ['sum', 'mean'],
            '顧客ID': 'nunique'
        }).round(2)
        
        seasonal_analysis.columns = ['総売上', '平均売上', 'ユニーク顧客数']
        results['季節性分析'] = seasonal_analysis
        
        # 結果を表示
        print("曜日別売上（降順）:")
        weekday_sorted = results['曜日別パターン'].sort_values('総売上', ascending=False)
        for day, row in weekday_sorted.iterrows():
            print(f"  {day}: {row['総売上']:,.0f}円")
        
        print("\n月別売上（降順）:")
        monthly_sorted = results['季節性分析'].sort_values('総売上', ascending=False).head(6)
        for month, row in monthly_sorted.iterrows():
            print(f"  {month}月: {row['総売上']:,.0f}円")
        
        self.analysis_results['時系列分析'] = results
        return results
    
    def customer_segmentation(self) -> Dict[str, Any]:
        """顧客セグメンテーション"""
        if self.df is None:
            raise ValueError("データが読み込まれていません")
        
        print("\n=== 顧客セグメンテーション ===")
        
        results = {}
        
        # 1. 顧客別購買行動分析
        customer_behavior = self.df.groupby('顧客ID').agg({
            '売上金額': ['sum', 'mean', 'count'],
            '日付': ['min', 'max'],
            '商品カテゴリ': lambda x: len(x.unique())
        }).round(2)
        
        customer_behavior.columns = ['総購入金額', '平均購入金額', '購入回数', '初回購入日', '最終購入日', '購入カテゴリ数']
        
        # 購入頻度の計算
        customer_behavior['購入期間'] = (customer_behavior['最終購入日'] - customer_behavior['初回購入日']).dt.days
        customer_behavior['月間購入頻度'] = customer_behavior['購入回数'] / (customer_behavior['購入期間'] / 30 + 1)
        
        # 2. RFM分析（簡易版）
        reference_date = self.df['日付'].max()
        rfm_analysis = self.df.groupby('顧客ID').agg({
            '日付': lambda x: (reference_date - x.max()).days,  # Recency
            '売上金額': ['count', 'sum']  # Frequency, Monetary
        }).round(2)
        
        rfm_analysis.columns = ['Recency', 'Frequency', 'Monetary']
        
        # RFMスコアの計算
        rfm_analysis['R_Score'] = pd.qcut(rfm_analysis['Recency'], 5, labels=[5,4,3,2,1])
        rfm_analysis['F_Score'] = pd.qcut(rfm_analysis['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        rfm_analysis['M_Score'] = pd.qcut(rfm_analysis['Monetary'], 5, labels=[1,2,3,4,5])
        
        # 3. 顧客セグメント分類
        def segment_customers(row):
            if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
                return 'Champions'
            elif row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] >= 3:
                return 'Loyal Customers'
            elif row['R_Score'] >= 3 and row['F_Score'] >= 2:
                return 'Potential Loyalists'
            elif row['R_Score'] >= 4 and row['F_Score'] <= 2:
                return 'New Customers'
            elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
                return 'At Risk'
            else:
                return 'Others'
        
        rfm_analysis['顧客セグメント'] = rfm_analysis.apply(segment_customers, axis=1)
        
        # セグメント別統計
        segment_stats = rfm_analysis.groupby('顧客セグメント').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2)
        
        segment_count = rfm_analysis['顧客セグメント'].value_counts()
        
        results['顧客行動分析'] = customer_behavior
        results['RFM分析'] = rfm_analysis
        results['セグメント統計'] = segment_stats
        results['セグメント構成'] = segment_count
        
        # 結果を表示
        print("顧客セグメント構成:")
        for segment, count in segment_count.items():
            percentage = (count / len(rfm_analysis)) * 100
            print(f"  {segment}: {count}人 ({percentage:.1f}%)")
        
        print("\n上位顧客（購入金額順）:")
        top_customers = customer_behavior.sort_values('総購入金額', ascending=False).head(10)
        for customer_id, row in top_customers.iterrows():
            print(f"  顧客ID {customer_id}: {row['総購入金額']:,.0f}円 ({row['購入回数']:.0f}回)")
        
        self.analysis_results['顧客セグメンテーション'] = results
        return results
    
    def create_visualizations(self) -> None:
        """可視化の作成"""
        if self.df is None:
            raise ValueError("データが読み込まれていません")
        
        print("\n=== 可視化の作成 ===")
        
        # 図のサイズ設定
        plt.figure(figsize=(16, 12))
        
        # 1. カテゴリ別売上
        plt.subplot(2, 3, 1)
        category_sales = self.df.groupby('商品カテゴリ')['売上金額'].sum().sort_values(ascending=False)
        category_sales.plot(kind='bar')
        plt.title('カテゴリ別売上')
        plt.xlabel('商品カテゴリ')
        plt.ylabel('売上金額')
        plt.xticks(rotation=45)
        
        # 2. 月別売上推移
        plt.subplot(2, 3, 2)
        monthly_sales = self.df.groupby('月')['売上金額'].sum()
        monthly_sales.plot(kind='line', marker='o')
        plt.title('月別売上推移')
        plt.xlabel('月')
        plt.ylabel('売上金額')
        
        # 3. 曜日別売上
        plt.subplot(2, 3, 3)
        weekday_sales = self.df.groupby('曜日')['売上金額'].sum()
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_sales = weekday_sales.reindex(weekday_order)
        weekday_sales.plot(kind='bar')
        plt.title('曜日別売上')
        plt.xlabel('曜日')
        plt.ylabel('売上金額')
        plt.xticks(rotation=45)
        
        # 4. 地域別売上
        plt.subplot(2, 3, 4)
        regional_sales = self.df.groupby('地域')['売上金額'].sum()
        regional_sales.plot(kind='pie', autopct='%1.1f%%')
        plt.title('地域別売上構成')
        plt.ylabel('')
        
        # 5. 年齢層別売上
        plt.subplot(2, 3, 5)
        age_sales = self.df.groupby('年齢層')['売上金額'].sum()
        age_sales.plot(kind='bar')
        plt.title('年齢層別売上')
        plt.xlabel('年齢層')
        plt.ylabel('売上金額')
        
        # 6. 売上分布
        plt.subplot(2, 3, 6)
        self.df['売上金額'].hist(bins=30, alpha=0.7)
        plt.title('売上金額分布')
        plt.xlabel('売上金額')
        plt.ylabel('頻度')
        
        plt.tight_layout()
        plt.savefig('sales_analysis_charts.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("可視化を sales_analysis_charts.png に保存しました")
    
    def generate_report(self) -> None:
        """分析レポートの生成"""
        print("\n=== 分析レポートの生成 ===")
        
        if self.df is None:
            raise ValueError("データが読み込まれていません")
        
        if not self.analysis_results:
            print("分析結果がありません。先に分析を実行してください。")
            return
        
        # レポートの作成
        report = {
            'レポート作成日': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'データ期間': f"{self.df['日付'].min()} - {self.df['日付'].max()}",
            '分析結果': {}
        }
        
        # 基本分析結果
        if '基本分析' in self.analysis_results:
            basic_stats = self.analysis_results['基本分析']['基本統計']
            report['分析結果']['基本統計'] = {
                '総売上金額': f"{basic_stats['総売上金額']:,.0f}円",
                '平均売上金額': f"{basic_stats['平均売上金額']:,.0f}円",
                '取引件数': f"{basic_stats['取引件数']:,}件",
                'ユニーク顧客数': f"{basic_stats['ユニーク顧客数']:,}人"
            }
        
        # 顧客セグメンテーション結果
        if '顧客セグメンテーション' in self.analysis_results:
            segment_count = self.analysis_results['顧客セグメンテーション']['セグメント構成']
            report['分析結果']['顧客セグメント'] = {}
            for segment, count in segment_count.items():
                percentage = (count / segment_count.sum()) * 100
                report['分析結果']['顧客セグメント'][segment] = f"{count}人 ({percentage:.1f}%)"
        
        # JSONレポートの保存
        report_path = Path("sales_analysis_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"分析レポートを {report_path} に保存しました")
        
        # 簡易HTMLレポートの作成
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>売上分析レポート</title>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>売上分析レポート</h1>
            <p>レポート作成日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>データ期間: {self.df['日付'].min()} - {self.df['日付'].max()}</p>
            
            <h2>基本統計</h2>
            <ul>
                <li>総売上金額: {self.analysis_results['基本分析']['基本統計']['総売上金額']:,.0f}円</li>
                <li>平均売上金額: {self.analysis_results['基本分析']['基本統計']['平均売上金額']:,.0f}円</li>
                <li>取引件数: {self.analysis_results['基本分析']['基本統計']['取引件数']:,}件</li>
                <li>ユニーク顧客数: {self.analysis_results['基本分析']['基本統計']['ユニーク顧客数']:,}人</li>
            </ul>
            
            <h2>分析チャート</h2>
            <img src="sales_analysis_charts.png" alt="売上分析チャート" style="max-width: 100%;">
            
            <p>詳細な分析結果は sales_analysis_report.json をご参照ください。</p>
        </body>
        </html>
        """
        
        html_path = Path("sales_analysis_report.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTMLレポートを {html_path} に保存しました")


def main():
    """メイン実行関数"""
    print("=== 実践的データ分析プロジェクト ===\n")
    
    # 分析器の初期化
    analyzer = SalesAnalyzer()
    
    # 基本分析
    analyzer.basic_analysis()
    
    # 時系列分析
    analyzer.time_series_analysis()
    
    # 顧客セグメンテーション
    analyzer.customer_segmentation()
    
    # 可視化
    analyzer.create_visualizations()
    
    # レポート生成
    analyzer.generate_report()
    
    print("\n=== 分析完了 ===")
    print("生成されたファイル:")
    print("- sales_data.csv: 生成されたサンプルデータ")
    print("- sales_analysis_charts.png: 可視化グラフ")
    print("- sales_analysis_report.json: JSON形式レポート")
    print("- sales_analysis_report.html: HTML形式レポート")


if __name__ == "__main__":
    main()
