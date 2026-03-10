import feedparser
import requests


def fetch_ai_news():
    print("正在拉取分层技术资讯...")

    # 采用分层结构，让大模型知道信息的权重
    rss_sources = {
        "【权威发布与深度专栏】": [
            'https://export.arxiv.org/rss/cs.AI',  # ArXiv AI 论文官方源
            'https://medium.com/feed/towards-data-science',  # TDS 权威数据科学专栏
            'https://www.infoq.cn/feed'  # InfoQ 架构与前沿资讯
        ],
        "【社区讨论与博主实践】": [
            'https://www.reddit.com/r/MachineLearning/top/.rss?t=day',  # Reddit ML 社区每日最热
            'https://hnrss.org/newest?q=AI',  # Hacker News AI 频道
            'https://feed.cnblogs.com/blog/sitehome/rss'  # 博客园国内开发者实践
        ]
    }

    news_items = []

    # 模拟真实浏览器，防止被 Reddit 和 Medium 拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for category, urls in rss_sources.items():
        for url in urls:
            try:
                print(f"📡 正在拉取 [{category}] 源: {url}")
                response = requests.get(url, headers=headers, timeout=12)

                if response.status_code == 200:
                    feed = feedparser.parse(response.text)

                    # 权威信息提取前 3 条，博主讨论提取前 2 条
                    limit = 3 if "权威" in category else 2

                    for entry in feed.entries[:limit]:
                        news_items.append({
                            'category': category,
                            'title': entry.title,
                            'link': entry.link,
                            # Medium 等源的摘要包含大量 HTML 标签，只取前200字符
                            'summary': entry.get('summary', '')[:200]
                        })
                else:
                    print(f"⚠️ 状态码 {response.status_code}: 无法访问 {url}")

            except requests.exceptions.Timeout:
                print(f"⚠️ 请求超时: {url}")
            except Exception as e:
                print(f"❌ 抓取异常 {url}: {e}")

    return news_items