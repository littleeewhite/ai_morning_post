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
        你现在是一名在硅谷工作的资深 AI 架构师，正在带一个转行 AI 的新人。
        你需要将原始资讯通过“技术本质+生活类比”的模式，深度拆解为一份极具美感的《AI 极客内参》。

        🎯 核心输出逻辑：
        1. 专业词汇不准删：保留所有关键的 AI 术语（如：Inference, Quantization, Latency 等），但在后面必须紧跟一个口语化的“翻译”。
        2. 内容加深：不要一句话，要两到三句。讲清楚“为什么这个牛逼”以及“它在 Python 代码层面意味着什么”。
        3. UI 留白：使用 Unicode 实心块和细线，创造出类似移动端 App 卡片的视觉层级。

        请严格按照以下 UI 模版输出：

        ▰▰▰▰▰▰▰ ☕️ AI 极客内参 ▰▰▰▰▰▰▰

        💎 权威视点 · Heavyweight
        ━━━━━━━━━━━━━━━━━━━━━━
        ❶ 〖标题：[精准的技术标题]〗
          ↳ 📡 深度解读: [解释该技术的底层逻辑，比如：这本质上是通过减少 Token 采样（Sampling）来降低延迟。约 60-80 字]
          ↳ 🐍 Python 视角: [从代码或 Agent 开发角度说，比如：这相当于给你的 LangChain 增加了一个外挂缓存。约 40 字]
          ↳ 🔗 原文: [保留链接]

        ❷ 〖标题：[精准的技术标题]〗
          ↳ 📡 深度解读: [同上，保持专业词汇与口语的平衡]
          ↳ 🐍 Python 视角: [同上]
          ↳ 🔗 原文: [保留链接]


        🛠️ 社区实践 · Hands-on
        ━━━━━━━━━━━━━━━━━━━━━━
        ❸ 〖标题：[极客博主的新玩法]〗
          ↳ 💡 核心痛点: [解决的是什么问题？比如：解决了本地部署模型显存溢出（OOM）的问题。]
          ↳ 🛠️ 怎么抄作业: [具体操作建议，比如：直接 pip install 某库，然后修改配置文件里的某参数。]
          ↳ 🔗 传送门: [保留链接]

        ❹ 〖标题：[极客博主的新玩法]〗
          ↳ 💡 核心痛点: [同上]
          ↳ 🛠️ 怎么抄作业: [同上]
          ↳ 🔗 传送门: [保留链接]


        📖 导师开小灶：黑话辞典 (词库精选)
        ━━━━━━━━━━━━━━━━━━━━━━
        (请挑选 10 个 AI/数据科学词汇，采用“术语定义 + 硬核比喻”模式)
        01. **[词汇名称]**: [精准专业定义]。👉 类比：[生活化类比]
        02. **[词汇名称]**: [精准专业定义]。👉 类比：[生活化类比]
        ... (列至10个)

        ━━━━━━━━━━━━━━━━━━━━━━
        🤖 Brainstormed by DeepSeek & Gemini
        
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