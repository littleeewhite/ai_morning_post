import feedparser
import requests
import time
from datetime import datetime


def fetch_ai_news():
    print("🛡️ 开启【2025+ 纪元】资讯过滤模式...")

    # 设定基准：必须是 2025 年之后，且距今不超过 30 天
    MIN_YEAR = 2025
    MAX_DAYS = 30
    now_ts = time.time()

    rss_sources = {
        "🏛️ 权威发布": [
            'https://export.arxiv.org/rss/cs.AI',
            'https://www.infoq.cn/feed',
            'https://openai.com/news/rss/',
            'https://anthropic.com/news/rss',  # 增加 Claude 官方源
        ],
        "👨‍💻 极客实践": [
            'https://hnrss.org/newest?q=AI',
            'https://www.theverge.com/ai-artificial-intelligence/rss/index.xml',
            'https://techcrunch.com/category/artificial-intelligence/feed/'
        ]
    }

    news_items = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

    for category, urls in rss_sources.items():
        for url in urls:
            try:
                print(f"📡 扫描: {url}")
                response = requests.get(url, headers=headers, timeout=12)
                if response.status_code == 200:
                    feed = feedparser.parse(response.text)

                    for entry in feed.entries:
                        # 提取时间戳
                        pub_struct = entry.get('published_parsed') or entry.get('updated_parsed')

                        if pub_struct:
                            # 1. 第一道防线：年份硬拦截
                            if pub_struct.tm_year < MIN_YEAR:
                                continue  # 2024 及以前的内容直接扔掉

                            # 2. 第二道防线：30天保鲜期
                            entry_ts = time.mktime(pub_struct)
                            if (now_ts - entry_ts) > (MAX_DAYS * 24 * 3600):
                                continue
                        else:
                            # 如果源没有提供时间，为了安全起见，我们也跳过它
                            continue

                        news_items.append({
                            'category': category,
                            'title': entry.title,
                            'link': entry.link,
                            'summary': entry.get('summary', '')[:300],
                            'pub_date': time.strftime('%Y-%m-%d', pub_struct)
                        })

                        if len([i for i in news_items if i['category'] == category]) >= 6:
                            break
            except Exception as e:
                print(f"⚠️ 跳过源 {url}: {e}")

    print(f"✅ 过滤完成！已锁定 {len(news_items)} 条 2025-2026 年间的核心资讯。")
    return news_items