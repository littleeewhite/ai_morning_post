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
        你是一名资深的 AI 算法专家与技术布道师。请阅读以下原始资讯和 YouTube 视频字幕，为我整理一份具有深度技术视角的“极客晨报”。

        之前的总结过于简短，现在我需要你彻底深入细节，挖掘出新闻和视频背后的【技术原理】、【架构设计】或【代码逻辑】。

        挑选要求：
        从图文资讯中挑选 2 条最具技术硬核度的内容，从视频字幕中挑选 1 条含金量最高的教程。

        排版与内容深度规范（严格遵循以下结构）：

        ▰▰▰▰▰▰ ☕️ 极客深度晨报 ▰▰▰▰▰▰

        📰 核心资讯 (深度拆解)
        ━━━━━━━━━━━━━━━━━━━━━━
        ❶ [替换为极简标题]
          ↳ 📝 原理剖析: 
             - [深入细节1：这项技术/模型的底层架构或算法核心逻辑是什么？约 60-80 字]
             - [深入细节2：关键数据表现、优化了什么性能或带来了何种范式转变？约 60-80 字]
          ↳ 🛠️ 落地指南: [给出具体的 Python 开发、数据分析或智能体搭建场景下的应用建议。约 60 字]
          ↳ 🔗 链接: [保留原文链接]

        (❷ 格式同上...)

        ▶️ YouTube 硬核精讲
        ━━━━━━━━━━━━━━━━━━━━━━
        ❸ [替换为视频标题]
          ↳ 🎬 核心脉络: [用一段话总结这段视频推导的完整逻辑链。约 80-100 字]
          ↳ 🧠 干货提炼: 
             - [硬核点1：具体的数学推导、框架设计或代码实现要点。约 60 字]
             - [硬核点2：实战避坑指南或博主给出的核心最佳实践。约 60 字]
          ↳ 🔗 链接: [保留视频链接]

        ━━━━━━━━━━━━━━━━━━━━━━
        🤖 深入思考，拒绝浮于表面

        多媒体原始数据池：
        {raw_text}
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