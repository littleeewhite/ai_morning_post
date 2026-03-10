import feedparser
from youtube_transcript_api import YouTubeTranscriptApi
import re


def fetch_youtube_videos():
    print("🎬 正在巡视顶级 AI YouTube 频道...")

    # YouTube 频道的专属 RSS 订阅源 (通过 Channel ID 拼接)
    youtube_channels = {
        "Andrej Karpathy": "https://www.youtube.com/feeds/videos.xml?channel_id=UCRVWBOpuFrKz9rEqsBHEBMA",
        "AI Explained": "https://www.youtube.com/feeds/videos.xml?channel_id=UCNJ1Ymd5yFaUPp68MbJQzWA",
        "StatQuest": "https://www.youtube.com/feeds/videos.xml?channel_id=UCtYLUTtgS3k1Fg4y5tAhLbw"
    }

    video_items = []

    for channel_name, rss_url in youtube_channels.items():
        try:
            feed = feedparser.parse(rss_url)
            # 每个频道只检查最新的一期视频
            if feed.entries:
                latest_video = feed.entries[0]
                video_url = latest_video.link
                title = latest_video.title

                # 从 URL 中正则提取 Video ID
                video_id_match = re.search(r"v=([a-zA-Z0-9_-]+)", video_url)
                if not video_id_match:
                    continue

                video_id = video_id_match.group(1)

                # 尝试获取视频字幕 (优先获取英文，会自动被大模型翻译成中文总结)
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh-Hans'])
                    # 将字幕片段拼接成完整长文本，截取前 15000 个字符（防止爆 token）
                    full_transcript = " ".join([t['text'] for t in transcript_list])[:15000]

                    video_items.append({
                        'category': "▶️ 视频精讲 (YouTube)",
                        'title': f"[{channel_name}] {title}",
                        'link': video_url,
                        'summary': full_transcript  # 这里存的是完整的字幕！
                    })
                    print(f"✅ 成功提取字幕: {title}")
                except Exception as e:
                    print(f"⚠️ 无法获取字幕，跳过视频 [{title}]: {e}")

        except Exception as e:
            print(f"❌ 解析频道 {channel_name} 失败: {e}")

    return video_items