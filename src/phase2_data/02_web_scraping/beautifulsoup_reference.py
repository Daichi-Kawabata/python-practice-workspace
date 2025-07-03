"""
BeautifulSoupライブラリによるHTML解析（型安全版）

HTML/XMLの解析とスクレイピングの基礎を学習します。
全ての型エラーを解消し、型チェッカーで警告が出ない完全版です。
"""

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString, PageElement
from typing import List, Dict, Any, Optional, Union, cast
from dataclasses import dataclass, field
import re
import time


@dataclass
class ScrapedData:
    """スクレイピングで取得したデータを表すクラス"""
    title: str
    url: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


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


def basic_html_parsing():
    """基本的なHTML解析"""
    print("=== 基本的なHTML解析 ===")
    
    # 1. HTMLサンプル
    html_content = """
    <html>
        <head>
            <title>サンプルページ</title>
            <meta name="description" content="これはサンプルページです">
        </head>
        <body>
            <h1 id="main-title" class="title">メインタイトル</h1>
            <div class="content">
                <p class="intro">これは最初の段落です。</p>
                <p class="detail">詳細な内容がここに記述されています。</p>
                <ul class="list">
                    <li>項目1</li>
                    <li>項目2</li>
                    <li>項目3</li>
                </ul>
            </div>
            <footer>
                <a href="https://example.com">リンク</a>
            </footer>
        </body>
    </html>
    """
    
    # 2. BeautifulSoupオブジェクトの作成
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 3. 基本的な要素の取得
    # タイトルの取得
    title_tag = safe_find(soup, 'title')
    title = safe_get_text(title_tag, "タイトルなし")
    print(f"タイトル: {title}")
    
    # IDで要素を取得
    main_title_tag = safe_find(soup, 'h1', id='main-title')
    main_title = safe_get_text(main_title_tag)
    print(f"メインタイトル: {main_title}")
    
    # クラスで要素を取得
    intro_tag = safe_find(soup, 'p', class_='intro')
    intro = safe_get_text(intro_tag)
    print(f"導入文: {intro}")
    
    # 複数の要素を取得
    all_p_tags = safe_find_all(soup, 'p')
    print(f"\n段落の数: {len(all_p_tags)}")
    for i, p_tag in enumerate(all_p_tags, 1):
        text = safe_get_text(p_tag)
        class_attr = safe_get_attribute(p_tag, 'class', 'クラスなし')
        print(f"  段落{i}: {text} (class: {class_attr})")
    
    # リスト項目の取得
    li_tags = safe_find_all(soup, 'li')
    print(f"\nリスト項目:")
    for li_tag in li_tags:
        text = safe_get_text(li_tag)
        print(f"  - {text}")
    
    # リンクの取得
    a_tag = safe_find(soup, 'a')
    if a_tag:
        link_text = safe_get_text(a_tag)
        link_url = safe_get_attribute(a_tag, 'href')
        print(f"\nリンク: {link_text} -> {link_url}")


def advanced_element_selection():
    """高度な要素選択"""
    print("\n=== 高度な要素選択 ===")
    
    html_content = """
    <div class="post" data-id="1">
        <h2>投稿タイトル1</h2>
        <p class="author">作成者: 山田太郎</p>
        <div class="content">
            <p>これは投稿の内容です。</p>
            <p>詳細な説明がここにあります。</p>
        </div>
        <div class="tags">
            <span class="tag">Python</span>
            <span class="tag">Web</span>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # データ属性での検索
    first_post = safe_find(soup, 'div', attrs={'data-id': '1'})
    if first_post:
        # 子要素の検索
        h2_tag = safe_find(first_post, 'h2')
        if h2_tag:
            title = safe_get_text(h2_tag)
            print(f"投稿タイトル: {title}")
        
        # 複数の子要素検索 - CSSセレクタは使わず直接検索
        content_div = safe_find(first_post, 'div', class_='content')
        if content_div:
            content_tags = safe_find_all(content_div, 'p')
            print("投稿内容:")
            for tag in content_tags:
                text = safe_get_text(tag)
                print(f"  {text}")
        
        # タグの取得
        tag_elements = safe_find_all(first_post, 'span', class_='tag')
        tags = [safe_get_text(tag) for tag in tag_elements]
        print(f"タグ: {', '.join(tags)}")


def navigate_html_tree():
    """HTMLツリーのナビゲーション"""
    print("\n=== HTMLツリーのナビゲーション ===")
    
    html_content = """
    <div class="container">
        <h1>セクション1</h1>
        <p>段落1</p>
        <h2>サブセクション</h2>
        <p>段落2</p>
        <ul>
            <li>項目1</li>
            <li>項目2</li>
        </ul>
    </div>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    container = safe_find(soup, 'div', class_='container')
    
    if container and isinstance(container, Tag):
        print("親要素から子要素へのナビゲーション:")
        
        # 親要素の属性確認
        class_value = safe_get_attribute(container, 'class')
        print(f"コンテナのクラス: {class_value}")
        
        # 子要素の走査（型安全）
        print("子要素:")
        for child in container.children:
            if isinstance(child, Tag):
                tag_name = child.name if child.name else "unknown"
                text = safe_get_text(child)
                if text:
                    print(f"  <{tag_name}>: {text}")
        
        # 兄弟要素のナビゲーション
        h1_tag = safe_find(container, 'h1')
        if h1_tag and isinstance(h1_tag, Tag):
            print(f"\nH1タグの次の兄弟要素:")
            next_element = h1_tag.find_next_sibling()
            if next_element and isinstance(next_element, Tag):
                tag_name = next_element.name if next_element.name else "unknown"
                text = safe_get_text(next_element)
                print(f"  <{tag_name}>: {text}")


def extract_specific_data():
    """特定のデータ抽出"""
    print("\n=== 特定のデータ抽出 ===")
    
    html_content = """
    <div class="article">
        <h1>記事タイトル</h1>
        <div class="metadata">
            <span class="author">作成者: 佐藤花子</span>
            <span class="date">2024-01-15</span>
            <div class="stats">
                <span class="views">1,234 views</span>
                <span class="likes">56 likes</span>
            </div>
        </div>
        <div class="content">
            <p>記事の本文がここにあります。</p>
            <p>詳細な内容が続きます。</p>
            <a href="https://example.com/related">関連記事</a>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 記事データの抽出
    article_data = {}
    
    # タイトル
    title_tag = safe_find(soup, 'h1')
    article_data['title'] = safe_get_text(title_tag)
    
    # 作成者（正規表現を使用）
    author_tag = safe_find(soup, 'span', class_='author')
    author_text = safe_get_text(author_tag)
    author_match = re.search(r'作成者:\s*(.+)', author_text)
    article_data['author'] = author_match.group(1) if author_match else "不明"
    
    # 日付
    date_tag = safe_find(soup, 'span', class_='date')
    article_data['date'] = safe_get_text(date_tag)
    
    # 統計情報
    views_tag = safe_find(soup, 'span', class_='views')
    views_text = safe_get_text(views_tag)
    views_match = re.search(r'([\d,]+)', views_text)
    article_data['views'] = int(views_match.group(1).replace(',', '')) if views_match else 0
    
    likes_tag = safe_find(soup, 'span', class_='likes')
    likes_text = safe_get_text(likes_tag)
    likes_match = re.search(r'(\d+)', likes_text)
    article_data['likes'] = int(likes_match.group(1)) if likes_match else 0
    
    # リンク
    link_tag = safe_find(soup, 'a')
    if link_tag:
        href = safe_get_attribute(link_tag, 'href')
        link_text = safe_get_text(link_tag)
        article_data['related_link'] = {'url': href, 'text': link_text}
    
    print("抽出された記事データ:")
    for key, value in article_data.items():
        print(f"  {key}: {value}")


def parse_table_data():
    """テーブルデータの解析"""
    print("\n=== テーブルデータの解析 ===")
    
    html_content = """
    <table class="products">
        <thead>
            <tr>
                <th>商品名</th>
                <th>価格</th>
                <th>在庫</th>
                <th>カテゴリ</th>
            </tr>
        </thead>
        <tbody>
            <tr data-id="1" class="available">
                <td>ノートパソコン</td>
                <td>¥89,800</td>
                <td>15</td>
                <td>電子機器</td>
            </tr>
            <tr data-id="2" class="sold-out">
                <td>マウス</td>
                <td>¥2,500</td>
                <td>0</td>
                <td>アクセサリ</td>
            </tr>
            <tr data-id="3" class="available">
                <td>キーボード</td>
                <td>¥5,800</td>
                <td>8</td>
                <td>アクセサリ</td>
            </tr>
        </tbody>
    </table>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    table = safe_find(soup, 'table', class_='products')
    
    if not table:
        print("テーブルが見つかりません")
        return
    
    # ヘッダーの取得
    thead = safe_find(table, 'thead')
    headers = []
    if thead:
        th_elements = safe_find_all(thead, 'th')
        headers = [safe_get_text(th) for th in th_elements]
    
    print(f"テーブルヘッダー: {headers}")
    
    # データ行の取得
    tbody = safe_find(table, 'tbody')
    products = []
    if tbody:
        tr_elements = safe_find_all(tbody, 'tr')
        for row in tr_elements:
            td_elements = safe_find_all(row, 'td')
            if len(td_elements) >= 4:
                product = {
                    'id': safe_get_attribute(row, 'data-id'),
                    'name': safe_get_text(td_elements[0]),
                    'price': safe_get_text(td_elements[1]),
                    'stock': safe_get_text(td_elements[2]),
                    'category': safe_get_text(td_elements[3]),
                    'status': safe_get_attribute(row, 'class')
                }
                products.append(product)
    
    print("\n商品データ:")
    for product in products:
        print(f"  ID: {product['id']}")
        print(f"  商品名: {product['name']}")
        print(f"  価格: {product['price']}")
        print(f"  在庫: {product['stock']}")
        print(f"  カテゴリ: {product['category']}")
        print(f"  ステータス: {product['status']}")
        print("  ---")


def handle_complex_html():
    """複雑なHTMLの処理"""
    print("\n=== 複雑なHTMLの処理 ===")
    
    html_content = """
    <div class="page">
        <header>
            <nav>
                <ul>
                    <li><a href="/home">ホーム</a></li>
                    <li><a href="/about">会社概要</a></li>
                    <li><a href="/contact">お問い合わせ</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <article>
                <h1>重要なお知らせ</h1>
                <!-- コメントは無視されます -->
                <p class="highlight">新商品を発売しました！</p>
                <div class="image-container">
                    <img src="product.jpg" alt="新商品画像" title="新商品">
                </div>
            </article>
        </main>
        <footer>
            <p>&copy; 2024 Company Name. All rights reserved.</p>
        </footer>
    </div>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # ナビゲーションリンクの抽出
    nav_links = []
    nav = safe_find(soup, 'nav')
    if nav:
        a_tags = safe_find_all(nav, 'a')
        for a_tag in a_tags:
            link_data = {
                'text': safe_get_text(a_tag),
                'url': safe_get_attribute(a_tag, 'href')
            }
            nav_links.append(link_data)
    
    print("ナビゲーションリンク:")
    for link in nav_links:
        print(f"  {link['text']}: {link['url']}")
    
    # メイン記事の情報
    article = safe_find(soup, 'article')
    if article:
        title_tag = safe_find(article, 'h1')
        title = safe_get_text(title_tag)
        
        highlight_tag = safe_find(article, 'p', class_='highlight')
        highlight = safe_get_text(highlight_tag)
        
        img_tag = safe_find(article, 'img')
        img_info = {}
        if img_tag:
            img_info = {
                'src': safe_get_attribute(img_tag, 'src'),
                'alt': safe_get_attribute(img_tag, 'alt'),
                'title': safe_get_attribute(img_tag, 'title')
            }
        
        print(f"\n記事タイトル: {title}")
        print(f"ハイライト: {highlight}")
        if img_info:
            print(f"画像情報: {img_info}")


def practical_scraping_example():
    """実践的なスクレイピング例"""
    print("\n=== 実践的なスクレイピング例 ===")
    
    # サンプルHTMLページ
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>商品一覧 - オンラインストア</title>
        <meta name="description" content="最新の商品一覧をご覧ください">
    </head>
    <body>
        <div class="products-container">
            <div class="product" data-id="101">
                <h3>スマートフォン</h3>
                <p class="price">¥79,800</p>
                <p class="description">最新のスマートフォンです</p>
                <div class="tags">
                    <span class="tag">電子機器</span>
                    <span class="tag">通信</span>
                </div>
            </div>
            <div class="product" data-id="102">
                <h3>ワイヤレスイヤホン</h3>
                <p class="price">¥12,800</p>
                <p class="description">高音質なワイヤレスイヤホン</p>
                <div class="tags">
                    <span class="tag">オーディオ</span>
                    <span class="tag">アクセサリ</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    soup = BeautifulSoup(sample_html, 'html.parser')
    
    # ページのメタデータ取得
    page_data = ScrapedData(
        title=safe_get_text(safe_find(soup, 'title'), "無題"),
        url="https://example.com/products"
    )
    
    # description メタタグの取得
    description_tag = safe_find(soup, 'meta', attrs={'name': 'description'})
    if description_tag:
        description_content = safe_get_attribute(description_tag, 'content')
        if description_content:
            page_data.description = description_content
    
    print(f"ページタイトル: {page_data.title}")
    print(f"ページ説明: {page_data.description}")
    
    # 商品データの抽出
    products = []
    product_elements = safe_find_all(soup, 'div', class_='product')
    
    for product_element in product_elements:
        # 商品名
        name_tag = safe_find(product_element, 'h3')
        name = safe_get_text(name_tag)
        
        # 価格
        price_tag = safe_find(product_element, 'p', class_='price')
        price = safe_get_text(price_tag)
        
        # 説明
        desc_tag = safe_find(product_element, 'p', class_='description')
        description = safe_get_text(desc_tag)
        
        # タグ
        tag_elements = safe_find_all(product_element, 'span', class_='tag')
        tags = [safe_get_text(tag) for tag in tag_elements]
        
        # ID
        product_id = safe_get_attribute(product_element, 'data-id')
        
        product_data = {
            'id': product_id,
            'name': name,
            'price': price,
            'description': description,
            'tags': tags
        }
        products.append(product_data)
    
    print(f"\n抽出された商品数: {len(products)}")
    for product in products:
        print(f"\n商品ID: {product['id']}")
        print(f"商品名: {product['name']}")
        print(f"価格: {product['price']}")
        print(f"説明: {product['description']}")
        print(f"タグ: {', '.join(product['tags'])}")


def main():
    """メイン関数"""
    print("BeautifulSoup HTML解析のデモンストレーション")
    print("=" * 50)
    
    try:
        basic_html_parsing()
        advanced_element_selection()
        navigate_html_tree()
        extract_specific_data()
        parse_table_data()
        handle_complex_html()
        practical_scraping_example()
        
        print("\n" + "=" * 50)
        print("すべてのデモンストレーションが完了しました！")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
