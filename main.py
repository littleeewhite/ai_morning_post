from crawler import fetch_ai_news
from youtube_tracker import fetch_youtube_videos  # 引入新模块
from llm_processor import summarize_news
from notifier import push_to_iphone


def run_agent():
    print("=== 开始执行 AI 晨报定时任务 ===")

    # 1. 采集图文资讯
    text_news = fetch_ai_news()

    # 2. 采集 YouTube 视频字幕
    video_news = fetch_youtube_videos()

    # 合并所有数据
    all_raw_data = text_news + video_news
    print(f"共抓取到 {len(all_raw_data)} 条多媒体素材，准备移交 DeepSeek...")

    # 3. 生成摘要
    daily_summary = summarize_news(all_raw_data)

    # 4. 推送消息
    push_to_iphone(daily_summary)

    print("=== 任务执行完毕 ===")

if __name__ == "__main__":
    run_agent()