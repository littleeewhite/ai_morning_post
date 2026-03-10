from crawler import fetch_ai_news
from youtube_tracker import fetch_youtube_videos  # 引入新模块
from llm_processor import summarize_news
from notifier import push_to_iphone


def run_agent():
    print("=== 开始执行 AI 晨报定时任务 ===")

    # 1. 采集数据
    text_news = fetch_ai_news()
    video_news = fetch_youtube_videos()
    all_raw_data = text_news + video_news
    print(f"共抓取到 {len(all_raw_data)} 条多媒体素材，准备移交 DeepSeek...")

    # 2. 生成摘要 (这里会调用 llm_processor.py)
    daily_summary = summarize_news(all_raw_data)

    # --- 重点：检查下面这两行有没有写！ ---
    if daily_summary:
        # 3. 推送消息 (必须调用这个函数，否则 DeepSeek 生成完就直接丢掉了)
        push_to_iphone(daily_summary)
    else:
        print("❌ 错误：DeepSeek 返回内容为空，无法推送")
    # ------------------------------------

    print("=== 任务执行完毕 ===")

if __name__ == "__main__":
    run_agent()