"""
実践的なWebスクレイピング課題（型安全版）

このファイルには、学習した内容を組み合わせた実践的な課題が含まれています。
各課題を通じて、requests + BeautifulSoup + データ処理の総合的なスキルを身につけます。
型エラーを全て解消した安全なバージョンです。
"""

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString, PageElement
import csv
import json
import time
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import re


@dataclass
class NewsArticle:
    """ニュース記事を表すクラス"""
    title: str
    url: str
    published_date: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class Product:
    """商品情報を表すクラス"""
    name: str
    price: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    availability: Optional[str] = None
    url: Optional[str] = None


def safe_get_text(element: Optional[Union[Tag, NavigableString, PageElement]], default: str = "") -> str:
    """要素からテキストを安全に取得する"""
    if element is None:
        return default
    if isinstance(element, Tag):
        return element.get_text().strip()
    elif isinstance(element, NavigableString):
        return str(element).strip()
    else:
        return default


def safe_get_attribute(element: Optional[Union[Tag, NavigableString, PageElement]], 
                      attr: str, default: str = "") -> str:
    """要素から属性値を安全に取得する"""
    if element is None or not isinstance(element, Tag):
        return default
    value = element.get(attr)
    if value is None:
        return default
    if isinstance(value, list):
        return " ".join(str(v) for v in value)
    return str(value)


def safe_find(element: Union[Tag, BeautifulSoup], selector: str, **kwargs) -> Optional[Tag]:
    """要素から子要素を安全に検索する"""
    if not isinstance(element, (Tag, BeautifulSoup)):
        return None
    result = element.find(selector, **kwargs)
    return result if isinstance(result, Tag) else None


def safe_find_all(element: Union[Tag, BeautifulSoup], selector: str, **kwargs) -> List[Tag]:
    """要素から複数の子要素を安全に検索する"""
    if not isinstance(element, (Tag, BeautifulSoup)):
        return []
    results = element.find_all(selector, **kwargs)
    return [r for r in results if isinstance(r, Tag)]


def challenge_1_quotes_scraper():
    """
    課題1: 名言サイトのスクレイピング
    
    http://quotes.toscrape.com から名言を取得し、CSVファイルに保存する。
    取得する情報: 名言テキスト、作者名、タグ
    """
    print("=== 課題1: 名言サイトのスクレイピング ===")
    
    base_url = "http://quotes.toscrape.com"
    quotes_data = []
    
    try:
        print("名言を収集中...")
        
        # 最初のページを取得
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 名言を抽出
        quotes = safe_find_all(soup, 'div', class_='quote')
        
        for quote in quotes:
            # テキストを取得
            text_elem = safe_find(quote, 'span', class_='text')
            text = safe_get_text(text_elem)
            
            # 作者を取得
            author_elem = safe_find(quote, 'small', class_='author')
            author = safe_get_text(author_elem)
            
            # タグを取得
            tag_elems = safe_find_all(quote, 'a', class_='tag')
            tags = [safe_get_text(tag) for tag in tag_elems]
            
            quotes_data.append({
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            })
        
        print(f"取得した名言数: {len(quotes_data)}")
        
        # CSVファイルに保存
        output_file = Path("quotes_data.csv")
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['text', 'author', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for quote in quotes_data:
                writer.writerow(quote)
        
        print(f"データを {output_file} に保存しました")
        
        # 最初の3つの名言を表示
        print("\n取得した名言の例:")
        for i, quote in enumerate(quotes_data[:3], 1):
            print(f"{i}. \"{quote['text'][:50]}...\" - {quote['author']}")
            print(f"   タグ: {quote['tags']}")
            print()
    
    except Exception as e:
        print(f"エラー: {e}")
    
    print()


def challenge_2_weather_api():
    """
    課題2: 天気予報APIの活用
    
    OpenWeatherMap API（無料版）を模擬して、
    複数都市の天気情報を取得し、比較レポートを作成する。
    """
    print("=== 課題2: 天気予報APIの活用（模擬データ） ===")
    
    # 実際のAPIキーが必要なため、模擬データで実装例を示す
    cities = ["Tokyo", "Osaka", "Kyoto", "Hiroshima", "Sapporo"]
    
    # 模擬的な天気データ
    mock_weather_data = [
        {"city": "Tokyo", "temperature": 22, "humidity": 65, "description": "曇り"},
        {"city": "Osaka", "temperature": 25, "humidity": 70, "description": "晴れ"},
        {"city": "Kyoto", "temperature": 20, "humidity": 60, "description": "小雨"},
        {"city": "Hiroshima", "temperature": 24, "humidity": 68, "description": "晴れ"},
        {"city": "Sapporo", "temperature": 15, "humidity": 55, "description": "曇り"}
    ]
    
    print("天気情報を取得中...")
    
    # データ処理とレポート作成
    print("\n都市別天気情報:")
    total_temp = 0
    hottest_city = None
    coldest_city = None
    
    for data in mock_weather_data:
        city = data["city"]
        temp = data["temperature"]
        humidity = data["humidity"]
        desc = data["description"]
        
        print(f"{city}: {temp}°C, 湿度{humidity}%, {desc}")
        
        total_temp += temp
        
        if hottest_city is None or temp > hottest_city[1]:
            hottest_city = (city, temp)
        
        if coldest_city is None or temp < coldest_city[1]:
            coldest_city = (city, temp)
    
    # 統計情報
    avg_temp = total_temp / len(mock_weather_data)
    
    print(f"\n統計情報:")
    print(f"平均気温: {avg_temp:.1f}°C")
    if hottest_city:
        print(f"最高気温: {hottest_city[0]}（{hottest_city[1]}°C）")
    if coldest_city:
        print(f"最低気温: {coldest_city[0]}（{coldest_city[1]}°C）")
    
    # JSONファイルに保存
    output_file = Path("weather_report.json")
    report_data = {
        "date": "2024-01-15",  # 模擬日付
        "cities": mock_weather_data,
        "statistics": {
            "average_temperature": round(avg_temp, 1),
            "hottest_city": {"name": hottest_city[0], "temperature": hottest_city[1]} if hottest_city else None,
            "coldest_city": {"name": coldest_city[0], "temperature": coldest_city[1]} if coldest_city else None
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(report_data, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"\nレポートを {output_file} に保存しました")
    
    print()


def challenge_3_news_aggregator():
    """
    課題3: ニュースアグリゲーター
    
    複数のニュースソースから記事情報を取得し、
    カテゴリ別に整理してHTMLレポートを生成する。
    """
    print("=== 課題3: ニュースアグリゲーター（模擬実装） ===")
    
    # HackerNews（実際のサイト）から情報を取得
    try:
        print("HackerNewsから記事を取得中...")
        
        response = requests.get("https://news.ycombinator.com", timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 記事を抽出
        articles = []
        story_links = safe_find_all(soup, 'a', class_='storylink')
        
        for i, link in enumerate(story_links[:10]):  # 最初の10記事のみ
            title = safe_get_text(link)
            url = safe_get_attribute(link, 'href')
            
            # 相対URLを絶対URLに変換
            if url and url.startswith('item?'):
                url = f"https://news.ycombinator.com/{url}"
            
            # URLが空の場合のデフォルト値を設定
            final_url = url if url else "https://news.ycombinator.com"
            
            articles.append(NewsArticle(
                title=title,
                url=final_url,
                category="Tech",
                tags=["technology", "programming"]
            ))
        
        print(f"取得した記事数: {len(articles)}")
        
        # HTMLレポートを生成
        html_content = generate_news_report(articles)
        
        output_file = Path("news_report.html")
        with open(output_file, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)
        
        print(f"HTMLレポートを {output_file} に保存しました")
        
        # 記事の一覧を表示
        print("\n取得した記事の例:")
        for i, article in enumerate(articles[:5], 1):
            print(f"{i}. {article.title}")
            print(f"   URL: {article.url}")
            print()
    
    except Exception as e:
        print(f"エラー: {e}")
    
    print()


def generate_news_report(articles: List[NewsArticle]) -> str:
    """ニュースレポートのHTMLを生成"""
    html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ニュースレポート</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .article { border: 1px solid #ddd; margin: 10px 0; padding: 15px; }
            .title { font-size: 18px; font-weight: bold; margin-bottom: 5px; }
            .url { color: #666; font-size: 12px; }
            .tags { color: #0066cc; font-size: 12px; margin-top: 5px; }
        </style>
    </head>
    <body>
        <h1>ニュースレポート</h1>
        <p>取得記事数: {count}</p>
    """.format(count=len(articles))
    
    for article in articles:
        html += f"""
        <div class="article">
            <div class="title">{article.title}</div>
            <div class="url">URL: <a href="{article.url}" target="_blank">{article.url}</a></div>
            <div class="tags">タグ: {', '.join(article.tags)}</div>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html


def challenge_4_price_monitor():
    """
    課題4: 価格監視システム
    
    商品価格を定期的に監視し、価格変動を記録する。
    （実際の実装では、商品ページのHTMLを解析して価格を抽出）
    """
    print("=== 課題4: 価格監視システム（模擬実装） ===")
    
    # 模擬的な商品データ
    products = [
        {"name": "ノートPC", "price": 98000, "url": "https://example.com/laptop"},
        {"name": "スマートフォン", "price": 85000, "url": "https://example.com/phone"},
        {"name": "タブレット", "price": 65000, "url": "https://example.com/tablet"}
    ]
    
    print("商品価格を監視中...")
    
    # 価格履歴データを模擬
    import random
    price_history = []
    
    for product in products:
        # 価格変動を模擬（±5%の範囲で変動）
        base_price = product["price"]
        variation = random.uniform(-0.05, 0.05)
        current_price = int(base_price * (1 + variation))
        
        price_record = {
            "name": product["name"],
            "current_price": current_price,
            "previous_price": base_price,
            "change": current_price - base_price,
            "change_percent": round((current_price - base_price) / base_price * 100, 2),
            "url": product["url"],
            "timestamp": "2024-01-15 10:00:00"  # 模擬タイムスタンプ
        }
        
        price_history.append(price_record)
    
    # 価格変動レポート
    print("\n価格変動レポート:")
    for record in price_history:
        name = record["name"]
        current = record["current_price"]
        change = record["change"]
        change_pct = record["change_percent"]
        
        status = "↑" if change > 0 else "↓" if change < 0 else "→"
        
        print(f"{name}: ¥{current:,} ({status} {change:+,}円, {change_pct:+.2f}%)")
    
    # CSVファイルに保存
    output_file = Path("price_history.csv")
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'current_price', 'previous_price', 'change', 'change_percent', 'url', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for record in price_history:
            writer.writerow(record)
    
    print(f"\n価格履歴を {output_file} に保存しました")
    
    print()


def challenge_5_data_pipeline():
    """
    課題5: データパイプライン
    
    複数のソースからデータを取得し、変換・統合して最終レポートを作成する。
    """
    print("=== 課題5: データパイプライン ===")
    
    print("1. 複数ソースからデータを収集...")
    
    # データソース1: API（模擬）
    api_data = [
        {"id": 1, "type": "user", "name": "田中太郎", "age": 25},
        {"id": 2, "type": "user", "name": "佐藤花子", "age": 30},
        {"id": 3, "type": "user", "name": "山田次郎", "age": 28}
    ]
    
    # データソース2: CSV（模擬）
    csv_data = [
        {"user_id": 1, "score": 85, "category": "programming"},
        {"user_id": 2, "score": 92, "category": "design"},
        {"user_id": 3, "score": 78, "category": "programming"}
    ]
    
    print("2. データを変換・統合...")
    
    integrated_data = []
    
    # データを統合
    for user in api_data:
        user_id = user["id"]
        
        # 対応するスコアデータを検索
        score_data = next((item for item in csv_data if item["user_id"] == user_id), None)
        
        integrated_record = {
            "id": user_id,
            "name": user["name"],
            "age": user["age"],
            "score": score_data["score"] if score_data else 0,
            "category": score_data["category"] if score_data else "unknown"
        }
        
        integrated_data.append(integrated_record)
    
    print("3. 統計情報を計算...")
    
    # 統計情報
    total_users = len(integrated_data)
    avg_age = sum(record["age"] for record in integrated_data) / total_users
    avg_score = sum(record["score"] for record in integrated_data) / total_users
    
    category_stats = {}
    for record in integrated_data:
        category = record["category"]
        if category not in category_stats:
            category_stats[category] = {"count": 0, "total_score": 0}
        
        category_stats[category]["count"] += 1
        category_stats[category]["total_score"] += record["score"]
    
    # カテゴリごとの平均スコア
    for category, stats in category_stats.items():
        stats["avg_score"] = stats["total_score"] / stats["count"]
    
    print("4. 最終レポートを生成...")
    
    # 最終レポート
    report = {
        "summary": {
            "total_users": total_users,
            "average_age": round(avg_age, 1),
            "average_score": round(avg_score, 1)
        },
        "users": integrated_data,
        "category_statistics": category_stats
    }
    
    # JSONファイルに保存
    output_file = Path("integrated_report.json")
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(report, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"統合レポートを {output_file} に保存しました")
    
    # サマリーを表示
    print("\nレポートサマリー:")
    print(f"総ユーザー数: {report['summary']['total_users']}")
    print(f"平均年齢: {report['summary']['average_age']}歳")
    print(f"平均スコア: {report['summary']['average_score']}点")
    
    print("\nカテゴリ別統計:")
    for category, stats in category_stats.items():
        print(f"{category}: {stats['count']}人, 平均スコア: {stats['avg_score']:.1f}点")
    
    print()


def main():
    """メイン実行関数"""
    print("実践的なWebスクレイピング課題")
    print("=" * 50)
    
    # 各課題を実行
    challenge_1_quotes_scraper()
    challenge_2_weather_api()
    challenge_3_news_aggregator()
    challenge_4_price_monitor()
    challenge_5_data_pipeline()
    
    print("全課題完了！")
    print("\n生成されたファイル:")
    generated_files = [
        "quotes_data.csv",
        "weather_report.json", 
        "news_report.html",
        "price_history.csv",
        "integrated_report.json"
    ]
    
    for filename in generated_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename}")
    
    print("\n次のステップ:")
    print("1. より複雑なWebサイトでのスクレイピング実践")
    print("2. セレニウムを使用した動的コンテンツの処理")
    print("3. データ分析ライブラリ（pandas）との連携")


if __name__ == "__main__":
    main()
