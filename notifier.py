import requests
import os
import time


def push_to_iphone(content):
    print("准备推送到 iPhone...")

    bark_url_base = os.environ.get("BARK_URL", "").rstrip('/')
    if not bark_url_base:
        print("未配置 BARK_URL 环境变量！")
        return

    url = f"{bark_url_base}/"

    # 苹果 APNs 和 Nginx 都有严格的大小限制。
    # 我们按每 800 个字符进行智能分块（安全余量，绝对不会触发 413 报错）
    chunk_size = 800
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    print(f"内容总长度为 {len(content)} 字符，已自动切分为 {len(chunks)} 条推送。")

    for index, chunk in enumerate(chunks):
        # 如果被拆分了，在标题动态加上页码进度指示
        title_suffix = f" (第{index + 1}/{len(chunks)}页)" if len(chunks) > 1 else ""

        payload = {
            "title": f"☕️ 极客深度晨报{title_suffix}",
            "body": chunk,
            "group": "AI Learning",
            "icon": "https://cdn-icons-png.flaticon.com/512/2083/2083213.png",
            "sound": "minuet",
            "isArchive": 1,
            "level": "timeSensitive"
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"🚀 第 {index + 1} 页已成功推送！")
            else:
                print(f"推送失败，状态码: {response.status_code}, 返回: {response.text[:100]}")
        except Exception as e:
            print("推送请求发生异常:", e)

        # 增加 1.5 秒的线程休眠，防止并发请求过快导致到达手机的顺序错乱
        if len(chunks) > 1:
            time.sleep(1.5)