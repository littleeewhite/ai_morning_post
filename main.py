from crawler import fetch_ai_news
from llm_processor import summarize_news
from notifier import push_to_iphone


def run_agent():
    print("=== 开始执行 AI 晨报定时任务 ===")

    # 1. 采集数据
    raw_news = fetch_ai_news()
    print(f"共抓取到 {len(raw_news)} 条原始资讯。")

    # 2. 生成摘要
    daily_summary = summarize_news(raw_news)

    # ... 前面生成摘要的代码 ...



    # 3. 推送消息
    push_to_iphone(daily_summary)

    print("=== 任务执行完毕 ===")


if __name__ == "__main__":
    run_agent()