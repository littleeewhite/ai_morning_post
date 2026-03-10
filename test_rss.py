import requests
import feedparser


def test_fetch():
    # 我们用“博客园”的官方 RSS 作为测试，这个源在国内访问极快，且几乎没有反爬限制
    test_url = 'https://feed.cnblogs.com/blog/sitehome/rss'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print(f"🚀 开始测试请求: {test_url}")

    try:
        # 1. 测试网络请求
        response = requests.get(test_url, headers=headers, timeout=10)
        print(f"✅ HTTP 状态码: {response.status_code}")

        # 打印返回内容的前 100 个字符，看看是不是正常的 XML
        print(f"📦 返回内容片段: {response.text[:100]}...\n")

        if response.status_code == 200:
            # 2. 测试 XML 解析
            feed = feedparser.parse(response.text)
            entries_count = len(feed.entries)
            print(f"📊 feedparser 成功解析出 {entries_count} 篇文章")

            if entries_count > 0:
                print(f"📰 第一篇文章标题: {feed.entries[0].title}")
                print(f"🔗 第一篇文章链接: {feed.entries[0].link}")
            else:
                print("❌ 警告：状态码是 200，但 feedparser 没有解析出任何文章！可能对方返回的不是标准 RSS/Atom 格式。")

    except requests.exceptions.Timeout:
        print("❌ 错误：请求超时！请检查你的网络环境，或者是否需要开启/关闭系统代理。")
    except Exception as e:
        print(f"❌ 发生未知异常: {e}")


if __name__ == "__main__":
    test_fetch()