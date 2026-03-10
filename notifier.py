import requests
import os
import time


def push_to_iphone(content):
    print("--- [Debug] 正在启动安全切片推送 ---")
    bark_url_base = os.environ.get("BARK_URL", "").rstrip('/')

    # 缩小每段长度到 800，确保万无一失
    limit = 800
    lines = content.split('\n')
    chunks = []
    current_chunk = ""

    for line in lines:
        # 如果单行太长（虽然罕见），强制截断
        if len(line) > limit:
            line = line[:limit]

        if len(current_chunk) + len(line) < limit:
            current_chunk += line + "\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())

    print(f"--- [Debug] 准备分 {len(chunks)} 条推送给 Bark ---")

    for i, chunk in enumerate(chunks):
        # 增加随机 group 后缀，防止 iOS 自动折叠掉后面的消息
        payload = {
            "title": f"☕️ AI 导师晨报 ({i + 1}/{len(chunks)})",
            "body": chunk,
            "group": f"AI_Morning_{int(time.time())}",  # 动态组名
            "icon": "https://cdn-icons-png.flaticon.com/512/2083/2083213.png",
            "sound": "minuet",
            "isArchive": 1,
            "level": "active"
        }

        try:
            # 这里的 URL 拼接一定要干净
            res = requests.post(bark_url_base, json=payload, timeout=15)
            print(f"🚀 第 {i + 1} 段状态: {res.status_code}")
        except Exception as e:
            print(f"❌ 推送异常: {e}")

        time.sleep(1.5)