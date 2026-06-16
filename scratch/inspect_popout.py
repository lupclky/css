import re

with open("/Users/lap/Code/css/scratch/youtube_live_chat_popout.html", "r", encoding="utf-8") as f:
    content = f.read()

tags = re.findall(r'<([a-zA-Z0-9\-]+)', content)
yt_tags = sorted(list(set([t for t in tags if t.startswith('yt-') or t.startswith('ytd-')])))
print("Found YT tags:", yt_tags)
