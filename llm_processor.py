from openai import OpenAI
import os


def summarize_news(news_items):
    print("正在唤醒 DeepSeek 大脑进行信息提纯...")

    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )

    if not news_items:
        return "今日暂未抓取到有效资讯，请检查网络或 RSS 节点状态。"

    # 将格式化的数据喂给大模型
    # === 替换原有的 raw_text 生成逻辑 ===
    raw_text = "\n\n".join([
        f"来源级别: {item['category']}\n标题: {item['title']}\n链接: {item['link']}\n片段: {item['summary']}"
        for item in news_items
    ])

    # === 稍微调整 prompt 中的格式要求 ===
    prompt = f"""
        你现在是一位极具亲和力的大厂资深 AI 工程师。你正在带一个刚入门、准备转行 AI 领域（已有 Python 基础）的新人。
        请阅读以下原始资讯和 YouTube 视频字幕，为他整理一份“每天早上的技术闲聊晨报”。

        挑选要求：
        从图文资讯中挑选 2 条最值得关注的内容，从视频字幕中挑选 1 条含金量最高的教程。

        语言风格极其重要（绝对指令）：
        1. 极度口语化：像聊天一样自然！多用“大白话”、“打比方”。绝对不要机械地罗列参数和生硬的学术名词。
        2. 场景化代入：把高深的技术点，映射到他熟悉的 Python 编程逻辑或日常生活中。

        排版与内容规范（严格遵循以下结构）：

        ▰▰▰▰▰▰ ☕️ 导师的 AI 晨报 ▰▰▰▰▰▰

        📰 圈内大事件 (大白话解读)
        ━━━━━━━━━━━━━━━━━━━━━━
        ❶ [替换为带点悬念或趣味的一句话标题]
          ↳ 🤔 啥意思啊：[用极其通俗的语言，结合生活类比或基础编程概念，讲明白这个技术或新闻的核心。约 80 字]
          ↳ 💡 怎么用它：[用师兄带新人的口吻，告诉他如果想练手或者写进简历，可以怎么结合 Python 去用。约 60 字]
          ↳ 🔗 传送门: [保留原文链接]

        (❷ 格式同上...)

        ▶️ 必看硬核视频 (帮你画重点)
        ━━━━━━━━━━━━━━━━━━━━━━
        ❸ [替换为接地气的视频标题]
          ↳ 🎬 核心脉络: [像朋友给你安利电影一样，总结这期视频最精彩的推导逻辑或踩坑经验。约 100 字]
          ↳ 🧠 课代表笔记: 
             - [干货1：具体到某个代码逻辑或好用的工具，大白话解释。约 60 字]
             - [干货2：新手最容易犯的错，或者最值得抄的
        """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个严谨的技术观察员，专注于 AI 技术的工程落地。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"大模型生成摘要失败: {e}"