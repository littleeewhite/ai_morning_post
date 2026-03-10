from openai import OpenAI
import os
import time
import random

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
    tech_topics = ["计算机视觉", "自然语言处理", "模型压缩", "数据工程", "强化学习", "多模态", "Agent 编排",
                   "向量数据库"]
    random_focus = random.choice(tech_topics)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    # === 稍微调整 prompt 中的格式要求 ===
    prompt = f"""
        (基准时间: {time.strftime('%Y-%m-%d')} | 随机种子: {current_time})

        你现在是一名硅谷资深 AI 架构师。请为转行新人制作一份《AI 极客内参》。

        🎯 核心输出逻辑：
        1. 专业词汇不准删：保留所有关键的 AI 术语（如：Inference, Quantization, Latency 等），但在后面必须紧跟一个口语化的“翻译”。
        2. 内容加深：讲清楚技术本质，以及“对于想从事 AI 行业的技术人才有什么好处和应用”。
        3. UI 留白：使用 Unicode 实心块和细线，严禁使用任何 Markdown 符号（如 **、##）。

        🚨 核心红线：
        - 严禁总结任何发生在 2025 年之前的事件。
        - 【𝐀𝐈 𝐉𝐚𝐫𝐠𝐨𝐧】板块必须不多不少正好输出 10 个词汇，严禁只写 2 个！

        请严格按此模版输出（不要多说废话）：

        ▰▰▰▰▰▰▰ ☕️ 𝐀𝐈 导师晨报 ▰▰▰▰▰▰▰

        ■ 𝐓𝐨𝐝𝐚𝐲'𝐬 𝐇𝐢𝐠𝐡𝐥𝐢𝐠𝐡𝐭𝐬 (深度资讯)

        💎 权威视点 · Heavyweight
        ━━━━━━━━━━━━━━━━━━━━━━
        ❶ 〖标题：[精准的技术标题]〗
          ↳ 🕒 发布: [日期]
          ↳ 📡 深度解读: [约 80 字，必须包含底层逻辑和专业术语]
          ↳ 🐍 落地建议: [对转行人才的价值与应用场景，约 50 字]
          ↳ 🔗 原文: [链接]

        ❷ 〖标题：[精准的技术标题]〗
          ↳ [格式同上，必须是 2025-2026 年的资讯]


        🛠️ 社区实践 · Hands-on
        ━━━━━━━━━━━━━━━━━━━━━━
        ❸ 〖标题：[博主新玩法]〗
          ↳ 🕒 发布: [日期]
          ↳ 💡 核心痛点: [解决了什么实际问题？]
          ↳ 🛠️ 怎么抄作业: [具体操作建议]
          ↳ 🔗 传送门: [链接]

        ❹ 〖标题：[博主新玩法]〗
          ↳ [格式同上]


        ■ 𝐀𝐈 𝐉𝐚𝐫𝐠𝐨𝐧 (今日必背 · 𝟏𝟎 𝐖𝐨𝐫𝐝𝐬)
        ━━━━━━━━━━━━━━━━━━━━━━
        ⚠️ 导师警告：请从 {random_focus} 领域挑选 10 个硬核词汇，填满下方 10 个空位：

        01. 〖单词〗: [定义]。👉 类比：[比喻]
        02. 〖单词〗: [定义]。👉 类比：[比喻]
        03. 〖单词〗: [定义]。👉 类比：[比喻]
        04. 〖单词〗: [定义]。👉 类比：[比喻]
        05. 〖单词〗: [定义]。👉 类比：[比喻]
        06. 〖单词〗: [定义]。👉 类比：[比喻]
        07. 〖单词〗: [定义]。👉 类比：[比喻]
        08. 〖单词〗: [定义]。👉 类比：[比喻]
        09. 〖单词〗: [定义]。👉 类比：[比喻]
        10. 〖单词〗: [定义]。👉 类比：[比喻]

        ━━━━━━━━━━━━━━━━━━━━━━
        🤖 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝 𝐛𝐲 𝐃𝐞𝐞𝐩𝐒𝐞𝐞𝐤-𝐕𝟑 & 𝐆𝐞𝐦𝐢𝐧𝐢
        """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个严谨的技术观察员，专注于 AI 技术的工程落地。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=3000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"大模型生成摘要失败: {e}"