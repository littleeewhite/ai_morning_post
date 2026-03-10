import requests
import os
import time


def push_to_iphone(content):
    # ...获取 URL 的代码不变...

    # 调大分块大小，减少碎片化
    chunk_size = 2000
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    for index, chunk in enumerate(chunks):
        title = f"☕️ AI 导师晨报 ({index + 1}/{len(chunks)})"
        payload = {
            "title": title,
            "body": chunk,
            "group": "AI_Learning",
            "icon": "https://cdn-icons-png.flaticon.com/512/2083/2083213.png",
            "sound": "minuet",
            "isArchive": 1,
            "level": "active"  # 确保消息能立刻唤醒屏幕
        }
        # ...请求代码不变...
        time.sleep(1)  # 缩短等待时间