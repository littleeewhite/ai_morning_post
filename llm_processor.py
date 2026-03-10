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
        你现在是一位大厂资深 AI 工程师，正在带一个 Python 基础不错、想转行 AI 的新人。
        请根据以下原始资料，按照固定 UI 结构输出一份【极客深度晨报】。

        ⚠️ 核心任务优先级：
        第一优先级：整理 10 个 AI 黑话科普（放在最前面）。
        第二优先级：总结 2 条深度资讯和 1 条视频干货。

        排版规范（严格遵守）：

        ▰▰▰▰▰▰ ☕️ 导师的 AI 晨报 ▰▰▰▰▰▰

        📖 导师开小灶：今日 AI 黑话 (新手村必背)
        ━━━━━━━━━━━━━━━━━━━━━━
        (请随机挑选 10 个 AI/数据分析领域的硬核词汇，采用“一句话解释 + 极简类比”模式)
        1. **[词汇1]**: [一句话解释]。👉 **类比**：[生活化类比]
        ... (直到第10个)

        📰 圈内大事件 (大白话解读)
        ━━━━━━━━━━━━━━━━━━━━━━
        ❶ [标题]
          ↳ 🤔 啥意思：[深度拆解...]
          ↳ 💡 怎么用：[实战建议...]
          ↳ 🔗 传送门: [链接]

        (❷ 格式同上...)

        ▶️ 必看硬核视频 (帮你画重点)
        ━━━━━━━━━━━━━━━━━━━━━━
        ❸ [标题]
          ↳ 🎬 核心脉络: [逻辑总结...]
          ↳ 🧠 课代表笔记: [干货点...]
          ↳ 🔗 传送门: [链接]

        ━━━━━━━━━━━━━━━━━━━━━━
        🤖 每天进步一点点，转行不掉队！

        【待处理原始素材】：
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