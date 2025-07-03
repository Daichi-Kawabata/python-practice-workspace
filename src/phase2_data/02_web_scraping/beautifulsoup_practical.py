"""
BeautifulSoupライブラリによるHTML解析（実践的な例・型安全版）

実際に動作するHTML解析のサンプルコードです。
型エラーを全て解消した安全なバージョンです。
"""

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString, PageElement
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import time


@dataclass
class Article:
    """記事情報を表すクラス"""
    title: str
    url: str
    description: Optional[str] = None


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


def parse_simple_html():
    """シンプルなHTML解析の例"""
    print("=== シンプルなHTML解析 ===")
    
    html = """
    <html>
        <head><title>テストページ</title></head>
        <body>
            <h1>メインタイトル</h1>
            <p class="intro">紹介文です</p>
            <ul>
                <li>項目1</li>
                <li>項目2</li>
                <li>項目3</li>
            </ul>
        </body>
    </html>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # タイトルを取得
    title_tag = safe_find(soup, 'title')
    title = safe_get_text(title_tag)
    print(f"タイトル: {title}")
    
    # メインタイトルを取得
    h1_tag = safe_find(soup, 'h1')
    h1_text = safe_get_text(h1_tag)
    print(f"メインタイトル: {h1_text}")
    
    # 紹介文を取得
    intro_tag = safe_find(soup, 'p', class_='intro')
    intro_text = safe_get_text(intro_tag)
    print(f"紹介文: {intro_text}")
    
    # リスト項目を取得
    li_tags = safe_find_all(soup, 'li')
    print("リスト項目:")
    for i, li_tag in enumerate(li_tags, 1):
        li_text = safe_get_text(li_tag)
        print(f"  {i}. {li_text}")


def extract_table_data():
    """テーブルデータの抽出"""
    print("\n=== テーブルデータの抽出 ===")
    
    html = """
    <table>
        <thead>
            <tr>
                <th>名前</th>
                <th>年齢</th>
                <th>職業</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>田中太郎</td>
                <td>30</td>
                <td>エンジニア</td>
            </tr>
            <tr>
                <td>佐藤花子</td>
                <td>25</td>
                <td>デザイナー</td>
            </tr>
        </tbody>
    </table>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    table = safe_find(soup, 'table')
    
    if not table:
        print("テーブルが見つかりません")
        return
    
    # ヘッダーを取得
    headers = []
    thead = safe_find(table, 'thead')
    if thead:
        th_tags = safe_find_all(thead, 'th')
        headers = [safe_get_text(th) for th in th_tags]
    
    print(f"ヘッダー: {headers}")
    
    # データ行を取得
    tbody = safe_find(table, 'tbody')
    if tbody:
        tr_tags = safe_find_all(tbody, 'tr')
        for row_num, row in enumerate(tr_tags, 1):
            td_tags = safe_find_all(row, 'td')
            cells = [safe_get_text(td) for td in td_tags]
            print(f"行{row_num}: {cells}")


def extract_links_and_images():
    """リンクと画像の抽出"""
    print("\n=== リンクと画像の抽出 ===")
    
    html = """
    <div>
        <a href="https://example.com" target="_blank">外部リンク</a>
        <a href="/internal">内部リンク</a>
        <img src="image1.jpg" alt="画像1" width="100" height="100">
        <img src="image2.png" alt="画像2">
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # リンクを抽出
    links = safe_find_all(soup, 'a')
    print("リンク:")
    for link in links:
        href = safe_get_attribute(link, 'href')
        text = safe_get_text(link)
        target = safe_get_attribute(link, 'target')
        target_text = f" (新しいタブ)" if target == "_blank" else ""
        print(f"  {text}: {href}{target_text}")
    
    # 画像を抽出
    images = safe_find_all(soup, 'img')
    print("\n画像:")
    for img in images:
        src = safe_get_attribute(img, 'src')
        alt = safe_get_attribute(img, 'alt')
        width = safe_get_attribute(img, 'width')
        height = safe_get_attribute(img, 'height')
        size_info = f" ({width}x{height})" if width and height else ""
        print(f"  {alt}: {src}{size_info}")


def scrape_test_webpage():
    """テスト用のWebページをスクレイピング"""
    print("\n=== テスト用Webページのスクレイピング ===")
    
    try:
        # HTTPbinのHTML表示ページ
        url = "https://httpbin.org/html"
        print(f"URL: {url} にアクセス中...")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        print(f"ステータスコード: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # タイトルを取得
        title_tag = safe_find(soup, 'title')
        title = safe_get_text(title_tag)
        print(f"ページタイトル: {title}")
        
        # 見出しを取得
        headings = safe_find_all(soup, 'h1') + safe_find_all(soup, 'h2') + safe_find_all(soup, 'h3')
        if headings:
            print("見出し:")
            for heading in headings:
                heading_text = safe_get_text(heading)
                tag_name = heading.name if hasattr(heading, 'name') and heading.name else "unknown"
                print(f"  {tag_name}: {heading_text}")
        
        # リンクを取得
        links = safe_find_all(soup, 'a')
        if links and len(links) > 0:
            print("リンク:")
            for link in links[:3]:  # 最初の3つのみ表示
                href = safe_get_attribute(link, 'href')
                text = safe_get_text(link)
                if href:
                    print(f"  {text}: {href}")
        
    except requests.RequestException as e:
        print(f"HTTPエラー: {e}")
    except Exception as e:
        print(f"解析エラー: {e}")


def parse_complex_structure():
    """複雑な構造のHTML解析"""
    print("\n=== 複雑な構造のHTML解析 ===")
    
    html = """
    <div class="container">
        <header>
            <h1>ニュースサイト</h1>
        </header>
        <main>
            <article class="news-item" data-id="1">
                <h2>ニュース1</h2>
                <p class="meta">
                    <span class="author">記者A</span>
                    <span class="date">2024-01-15</span>
                </p>
                <p class="content">ニュースの内容です。</p>
            </article>
            <article class="news-item" data-id="2">
                <h2>ニュース2</h2>
                <p class="meta">
                    <span class="author">記者B</span>
                    <span class="date">2024-01-14</span>
                </p>
                <p class="content">別のニュースです。</p>
            </article>
        </main>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # サイトタイトル
    site_title_tag = safe_find(soup, 'header h1')
    site_title = safe_get_text(site_title_tag)
    print(f"サイトタイトル: {site_title}")
    
    # ニュース記事を抽出
    articles = safe_find_all(soup, 'article', class_='news-item')
    print(f"\nニュース記事数: {len(articles)}")
    
    for article in articles:
        article_id = safe_get_attribute(article, 'data-id')
        
        # タイトル
        title_tag = safe_find(article, 'h2')
        title = safe_get_text(title_tag)
        
        # 著者
        author_tag = safe_find(article, 'span', class_='author')
        author = safe_get_text(author_tag)
        
        # 日付
        date_tag = safe_find(article, 'span', class_='date')
        date = safe_get_text(date_tag)
        
        # 内容
        content_tag = safe_find(article, 'p', class_='content')
        content = safe_get_text(content_tag)
        
        print(f"\n記事ID: {article_id}")
        print(f"タイトル: {title}")
        print(f"著者: {author}")
        print(f"日付: {date}")
        print(f"内容: {content}")


def main():
    """メイン関数"""
    print("BeautifulSoup実践的HTML解析のデモンストレーション")
    print("=" * 50)
    
    try:
        parse_simple_html()
        extract_table_data()
        extract_links_and_images()
        scrape_test_webpage()
        parse_complex_structure()
        
        print("\n" + "=" * 50)
        print("全てのデモンストレーションが完了しました！")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
