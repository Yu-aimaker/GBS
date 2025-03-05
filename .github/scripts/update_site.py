#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob
from datetime import datetime
from bs4 import BeautifulSoup

# 設定
ARTICLES_DIR = 'articles'
CATEGORIES_DIR = 'categories'
SITEMAP_PATH = 'sitemap.xml'
INDEX_PATH = 'index.html'
BASE_URL = 'https://yu-aimaker.github.io/GBS'

# カテゴリとHTMLファイルのマッピング
CATEGORY_MAPPING = {
    '本': 'books.html',
    '自動車・バイク': 'automotive.html',
    'ベビー・キッズ': 'baby-kids.html',
    'ビューティー': 'beauty.html',
    'ドラッグストア': 'drugstore.html',
    'DVD・CD': 'dvd.html', 
    '家電・カメラ': 'electronics.html',
    'ファッション': 'fashion.html',
    '食品・飲料': 'food-beverage.html',
    'ゲーム': 'games.html',
    'ギフト': 'gift.html',
    'ホーム・キッチン': 'home-kitchen.html',
    '産業・研究開発用品': 'industrial.html',
    'パソコン・オフィス用品': 'pc-office.html',
    'ペット': 'pet.html',
    'スポーツ・アウトドア': 'sports-outdoor.html',
    'おもちゃ・ホビー': 'toys-hobby.html',
    '時計・アクセサリー': 'watch-accessories.html',
    '自己紹介': 'other.html',
    'お知らせ': 'other.html',
    '未分類': 'other.html'
}

# その他カテゴリ用のデフォルトファイル
DEFAULT_CATEGORY_FILE = 'other.html'

def get_new_articles():
    """Git履歴から新しい記事を検出する"""
    # すべての記事ファイルを取得
    articles = glob.glob(f'{ARTICLES_DIR}/*.html')
    
    # 新しい記事と見なす（実際のユースケースでは、Gitの履歴を使って新規ファイルを特定できる）
    # ここでは簡易的にすべての記事を処理対象とする
    return articles

def extract_article_info(article_path):
    """記事ファイルからメタデータを抽出する"""
    with open(article_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    
    # 基本情報を抽出
    article_id = os.path.basename(article_path).split('-')[0]
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else "無題の記事"
    
    # カテゴリを抽出
    category = "未分類"  # デフォルト値
    section_meta = soup.find('meta', attrs={'property': 'article:section'})
    if section_meta and section_meta.get('content'):
        category = section_meta.get('content')
    
    # 公開日を取得
    published_date = datetime.now().strftime('%Y-%m-%d')
    date_meta = soup.find('meta', attrs={'property': 'article:published_time'})
    if date_meta and date_meta.get('content'):
        try:
            date_str = date_meta.get('content')
            published_date = date_str.split('T')[0]
        except:
            pass
    
    # 記事の概要を取得
    description = ""
    desc_meta = soup.find('meta', attrs={'name': 'description'})
    if desc_meta and desc_meta.get('content'):
        description = desc_meta.get('content')
    
    # イメージパスを取得
    image_path = ""
    image_meta = soup.find('meta', attrs={'property': 'og:image'})
    if image_meta and image_meta.get('content'):
        image_path = image_meta.get('content').replace(f"{BASE_URL}/", "")
    
    # 記事の最初の段落（要約用）
    excerpt = description
    
    return {
        'id': article_id,
        'path': article_path,
        'title': title,
        'category': category,
        'date': published_date,
        'description': description,
        'excerpt': excerpt,
        'image': image_path,
        'url': f'{article_path}'
    }

def update_index_html(articles):
    """index.htmlの最新記事リストを更新する"""
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    
    # 最新の投稿セクションを探す
    posts_grid = soup.find('div', class_='posts-grid')
    if posts_grid:
        # 既存の記事アイテムをクリア
        posts_grid.clear()
        
        # 記事を新しい順に並べ替え
        sorted_articles = sorted(articles, key=lambda x: x['id'], reverse=True)
        
        # 各記事のHTMLを作成して追加
        for article in sorted_articles:
            # 画像パスを調整する
            image_path = article['image']
            
            # BASE_URLを取り除く（もしあれば）
            if BASE_URL in image_path:
                image_path = image_path.replace(f"{BASE_URL}/", "")
            
            # 記事ページからの相対パス（../assets/...）をホームページからの相対パス（assets/...）に修正
            if image_path.startswith('../'):
                image_path = image_path[3:]  # '../'を取り除く
            elif image_path.startswith('assets/'):
                # すでに正しい形式なのでそのまま
                pass
            else:
                # それ以外のケースでは、ルートからの相対パスとして扱う
                image_path = image_path
            
            # 記事リンクのHTMLを作成
            article_html = f"""
                <a href="{article['url']}" class="post-preview">
                    <div class="post-layout">
                        <img src="{image_path}" alt="{article['title']}のアイコン画像" class="post-image" width="800" height="200" loading="lazy">
                        <div class="post-content">
                            <h3>{article['title']}</h3>
                            <p class="post-meta">投稿日: {article['date']}</p>
                            <p>{article['excerpt']}</p>
                            <span class="read-more">続きを読む</span>
                        </div>
                    </div>
                </a>
            """
            # 作成したHTMLをパース
            article_soup = BeautifulSoup(article_html, 'lxml')
            # 記事リストに追加
            posts_grid.append(article_soup)
    
    # JSONLDデータも更新
    itemlist_script = soup.find('script', string=re.compile(r'@type": "ItemList"'))
    if itemlist_script:
        # 新しいJSONLDデータを作成
        jsonld_items = []
        
        for i, article in enumerate(sorted_articles, 1):
            rel_url = article['url'].replace(ARTICLES_DIR + '/', '')
            image_url = article['image']
            # タイトルから不要な部分を削除
            title = article['title'].split('|')[0].strip() if '|' in article['title'] else article['title']
            
            item = {
                "@type": "ListItem",
                "position": i,
                "url": f"{BASE_URL}/{article['url']}",
                "name": title,
                "description": article['excerpt'],
                "image": f"{BASE_URL}/{image_url}"
            }
            jsonld_items.append(item)
        
        # JSONLDデータを文字列化（簡易的な実装）
        jsonld_str = '{\n'
        jsonld_str += '  "@context": "https://schema.org",\n'
        jsonld_str += '  "@type": "ItemList",\n'
        jsonld_str += '  "itemListElement": [\n'
        
        for i, item in enumerate(jsonld_items):
            jsonld_str += '    {\n'
            jsonld_str += f'      "@type": "ListItem",\n'
            jsonld_str += f'      "position": {item["position"]},\n'
            jsonld_str += f'      "url": "{item["url"]}",\n'
            jsonld_str += f'      "name": "{item["name"]}",\n'
            jsonld_str += f'      "description": "{item["description"]}",\n'
            jsonld_str += f'      "image": "{item["image"]}"\n'
            jsonld_str += '    }' + (',' if i < len(jsonld_items) - 1 else '') + '\n'
        
        jsonld_str += '  ]\n'
        jsonld_str += '}\n'
        
        # 既存のスクリプトタグを新しいJSONLDで置き換え
        new_script = soup.new_tag('script')
        new_script['type'] = 'application/ld+json'
        new_script.string = jsonld_str
        itemlist_script.replace_with(new_script)
    
    # 更新したHTMLを保存
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"✅ index.htmlを{len(articles)}件の記事で更新しました")

def update_category_pages(articles):
    """カテゴリページの記事リストを更新する"""
    # ファイルごとに記事をグループ化
    file_articles = {}
    
    # 各記事をカテゴリファイルにマッピング
    for article in articles:
        category_name = article['category']
        # カテゴリに対応するHTMLファイルを取得
        if category_name in CATEGORY_MAPPING:
            category_file = CATEGORY_MAPPING[category_name]
        else:
            category_file = DEFAULT_CATEGORY_FILE
        
        # ファイル別に記事を整理
        if category_file not in file_articles:
            file_articles[category_file] = []
        file_articles[category_file].append(article)
    
    # 各カテゴリファイルを更新
    for category_file, mapped_articles in file_articles.items():
        category_path = os.path.join(CATEGORIES_DIR, category_file)
        
        # カテゴリページが存在するか確認
        if not os.path.exists(category_path):
            print(f"⚠️ カテゴリページが見つかりません: {category_path}, other.htmlを使用します")
            category_file = DEFAULT_CATEGORY_FILE
            category_path = os.path.join(CATEGORIES_DIR, DEFAULT_CATEGORY_FILE)
            
            # other.htmlに記事を追加
            if category_file not in file_articles:
                file_articles[category_file] = []
            file_articles[category_file].extend(mapped_articles)
            continue
        
        # カテゴリページを読み込む
        with open(category_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'lxml')
        
        # 記事リストセクションを探す
        articles_list = soup.find('div', class_='articles-list')
        if articles_list:
            # 既存の記事をクリア
            articles_list.clear()
            
            # 記事を新しい順に並べ替え
            sorted_articles = sorted(mapped_articles, key=lambda x: x['id'], reverse=True)
            
            # 各記事のHTMLを作成して追加
            for article in sorted_articles:
                # 記事のHTMLを作成
                article_html = f"""
                    <article class="article-item">
                        <h3 class="article-title">{article['title'].split('|')[0].strip()}</h3>
                        <div class="article-meta">投稿日: {article['date']}</div>
                        <p class="article-excerpt">{article['description']}</p>
                        <a href="../{article['url']}" class="read-more">続きを読む</a>
                    </article>
                """
                # 作成したHTMLをパース
                article_soup = BeautifulSoup(article_html, 'lxml')
                # 記事リストに追加
                articles_list.append(article_soup)
        
        # 更新したカテゴリページを保存
        with open(category_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"✅ カテゴリページを更新しました: {category_path} ({len(mapped_articles)}件の記事)")

def update_sitemap(articles):
    """サイトマップを更新する"""
    with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'xml')
    
    # 既存の記事URLを取得
    existing_urls = {}
    for url_tag in soup.find_all('url'):
        loc_tag = url_tag.find('loc')
        if loc_tag and "/articles/" in loc_tag.text:
            existing_urls[loc_tag.text] = url_tag
    
    # 新しい記事を追加
    for article in articles:
        article_url = f"{BASE_URL}/{article['url']}"
        
        # すでに存在する場合はスキップ
        if article_url in existing_urls:
            continue
        
        # 新しいURLエントリを作成
        new_url = soup.new_tag('url')
        
        # locタグを作成
        loc = soup.new_tag('loc')
        loc.string = article_url
        new_url.append(loc)
        
        # lastmodタグを作成
        lastmod = soup.new_tag('lastmod')
        lastmod.string = article['date']
        new_url.append(lastmod)
        
        # changefreqタグを作成
        changefreq = soup.new_tag('changefreq')
        changefreq.string = 'monthly'
        new_url.append(changefreq)
        
        # priorityタグを作成
        priority = soup.new_tag('priority')
        priority.string = '0.9'
        new_url.append(priority)
        
        # 画像情報があれば追加
        if article['image']:
            image = soup.new_tag('image:image', prefix='image')
            
            image_loc = soup.new_tag('image:loc', prefix='image')
            image_loc.string = f"{BASE_URL}/{article['image']}"
            image.append(image_loc)
            
            image_title = soup.new_tag('image:title', prefix='image')
            image_title.string = f"{article['title']}のアイコン画像"
            image.append(image_title)
            
            new_url.append(image)
        
        # サイトマップに追加
        soup.urlset.append(new_url)
    
    # 更新したサイトマップを保存
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"✅ sitemap.xmlを更新しました")

def main():
    """メイン処理"""
    print("🚀 サイト更新スクリプトを実行します...")
    
    # 新しい記事を取得
    article_files = get_new_articles()
    print(f"📝 処理対象の記事: {len(article_files)}件")
    
    # 記事情報を抽出
    articles = []
    for article_file in article_files:
        article_info = extract_article_info(article_file)
        articles.append(article_info)
        print(f"⚙️ 記事を解析: {article_info['title']} (カテゴリ: {article_info['category']})")
    
    # 各種ページを更新
    update_index_html(articles)
    update_category_pages(articles)
    update_sitemap(articles)
    
    print("✨ サイト更新が完了しました！")

if __name__ == "__main__":
    main() 