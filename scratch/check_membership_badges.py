import re

html_path = "/Users/lap/Code/css/scratch/youtube_live_chat_popout.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all img tags
img_tags = re.findall(r'<img[^>]+>', content)
print("--- ALL BADGE/MEMBER IMAGES ---")
for img in img_tags:
    alt_match = re.search(r'alt="([^"]*)"', img)
    src_match = re.search(r'src="([^"]*)"', img)
    alt = alt_match.group(1) if alt_match else ""
    src = src_match.group(1) if src_match else ""
    if any(k in alt.lower() or k in src.lower() for k in ["member", "hội viên", "month", "tháng", "year", "năm", "badge"]):
        print(f"Alt: {alt} | Src: {src[:60]}...")

# Find all yt-live-chat-author-badge-renderer tags
badge_tags = re.findall(r'<yt-live-chat-author-badge-renderer[^>]+>', content)
print("\n--- ALL AUTHOR BADGE RENDERERS ---")
for badge in badge_tags:
    label_match = re.search(r'aria-label="([^"]*)"', badge)
    type_match = re.search(r'type="([^"]*)"', badge)
    label = label_match.group(1) if label_match else ""
    b_type = type_match.group(1) if type_match else ""
    print(f"Type: {b_type} | Aria-Label: {label}")
