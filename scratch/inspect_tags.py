import re
with open("/Users/lap/Code/css/scratch/youtube_live_chat_popout.html", "r", encoding="utf-8") as f:
    content = f.read()

print("HTML Length:", len(content))
print("First 500 chars:", content[:500])

# Find tags starting with yt-
tags = re.findall(r'<([a-zA-Z0-9\-]+)', content)
yt_tags = sorted(list(set([t for t in tags if t.startswith('yt-') or t.startswith('ytd-')])))
print("Found YT tags:", yt_tags)

# Check if there are any messages
messages = re.findall(r'<yt-live-chat-text-message-renderer', content)
print("Text message count:", len(messages))
paid_messages = re.findall(r'<yt-live-chat-paid-message-renderer', content)
print("Paid message count:", len(paid_messages))
membership_messages = re.findall(r'<yt-live-chat-membership-item-renderer', content)
print("Membership message count:", len(membership_messages))
