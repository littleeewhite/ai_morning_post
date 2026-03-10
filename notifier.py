import requests
import os
import time


def push_to_iphone(content):
    print("--- [Debug] 修正推送路径中... ---")

    # 这里的 BARK_URL 应该是 https://api.day.app/你的Key (末尾不带斜杠)
    bark_url_base = os.environ.get("BARK_URL", "").rstrip('/')
    if not bark_url_base:
        print("❌ 未配置 BARK_URL")
        return

    # 切片逻辑保持不变 (1000字符安全块)
    lines = content.split('\n')
    chunks = []
    current_chunk = ""
    for line in lines:
        if len(current_chunk) + len(line) < 1000:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
    chunks.append(current_chunk.strip())

    print(f"--- [Debug] 准备分 {len(chunks)} 段发送 ---")

    for index, chunk in enumerate(chunks):
        # 核心修复：直接使用 base URL。Bark 会自动识别 POST 里的 JSON
        # 如果你之前收到了 "push" 字样，说明服务器把 URL 里的 /push 当成了内容
        url = bark_url_base

        payload = {
            "title": f"☕️ AI 极客内参 ({index + 1}/{len(chunks)})",
            "body": chunk,
            "group": "AI_Daily",
            "icon": "https://cdn-icons-png.flaticon.com/512/2083/2083213.png",
            "sound": "minuet",
            "isArchive": 1
        }

        try:
            # 使用 json=payload 会自动设置 Content-Type 为 application/json
            response = requests.post(url, json=payload, timeout=15)

            if response.status_code == 200:
                print(f"🚀 第 {index + 1} 段发送成功")
            else:
                # 如果还是不行，打印出完整的返回信息排查
                print(f"❌ 失败码: {response.status_code}, 返回: {response.text}")
        except Exception as e:
            print(f"❌ 推送异常: {e}")

        time.sleep(1.5)