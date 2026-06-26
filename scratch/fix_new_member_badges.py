import shutil
from check_braces import check_braces

source_file = "/Users/lap/Code/css/css.css"
backup_file = "/Users/lap/Code/css/css_backup_temp_new_member.css"

# Step 1: Make a backup of the original file
shutil.copy2(source_file, backup_file)
print(f"Created backup at: {backup_file}")

with open(source_file, "r", encoding="utf-8") as f:
    content = f.read()

# Locate the default member badge content swap block (around lines 2003-2029)
# We will add :not([alt*="Hội viên mới" i]):not([alt*="New member" i]):not([aria-label*="Hội viên mới" i]):not([aria-label*="New member" i])
# to all selectors in that group to ensure new member badges are never replaced by the 1-month pineapple icon.

old_default_swap = """    yt-live-chat-text-message-renderer[author-type="member"] yt-live-chat-author-chip #chat-badges img,
    yt-live-chat-text-message-renderer[author-type="member"] yt-live-chat-author-chip #author-badges img,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]) yt-live-chat-author-chip #chat-badges img,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]) yt-live-chat-author-chip #author-badges img,
    :is(yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer) :is(yt-live-chat-author-badge-renderer, #chat-badges, #author-badges) img,
    :is(yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer) img[class*="badge"],
    :is(yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer) img[id*="badge"],
    yt-live-chat-paid-message-renderer yt-live-chat-author-badge-renderer[type="member"] img,
    yt-live-chat-paid-message-renderer :is(yt-live-chat-author-badge-renderer, #chat-badges, #author-badges) img:not([src*="moderator"]):not([alt*="moderator"]):not([alt*="quản trị viên"]),
    yt-live-chat-paid-message-renderer img[class*="badge"]:not([src*="moderator"]):not([alt*="moderator"]):not([alt*="quản trị viên"]) {"""

new_default_swap = """    yt-live-chat-text-message-renderer[author-type="member"] yt-live-chat-author-chip #chat-badges img:not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    yt-live-chat-text-message-renderer[author-type="member"] yt-live-chat-author-chip #author-badges img:not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]) yt-live-chat-author-chip #chat-badges img:not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]) yt-live-chat-author-chip #author-badges img:not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    :is(yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer) :is(yt-live-chat-author-badge-renderer, #chat-badges, #author-badges) img:not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    :is(yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer) img[class*="badge"]:not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    :is(yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer) img[id*="badge"]:not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    yt-live-chat-paid-message-renderer yt-live-chat-author-badge-renderer[type="member"] img:not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    yt-live-chat-paid-message-renderer :is(yt-live-chat-author-badge-renderer, #chat-badges, #author-badges) img:not([src*="moderator"]):not([alt*="moderator"]):not([alt*="quản trị viên"]):not([alt*="Hội viên mới" i]):not([alt*="New member" i]),
    yt-live-chat-paid-message-renderer img[class*="badge"]:not([src*="moderator"]):not([alt*="moderator"]):not([alt*="quản trị viên"]):not([alt*="Hội viên mới" i]):not([alt*="New member" i]) {"""

# Replace old default swap
if old_default_swap in content:
    content = content.replace(old_default_swap, new_default_swap)
    print("Replaced default swap selector successfully!")
else:
    print("Warning: old_default_swap not found exactly!")

# Now locate the old new member badge rules (lines 2087-2129) and replace them with a complete hide rule.
old_hide_block = """    /* New member badge hide left side absolute */

    yt-live-chat-text-message-renderer[author-type="member"]:has(img[alt="Hội viên mới"]) yt-live-chat-author-chip #chat-badges,
    yt-live-chat-text-message-renderer[author-type="member"]:has(img[alt="New member"]) yt-live-chat-author-chip #chat-badges,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(img[alt="Hội viên mới"]) yt-live-chat-author-chip #chat-badges,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(img[alt="New member"]) yt-live-chat-author-chip #chat-badges,
    yt-live-chat-text-message-renderer[author-type="member"]:has(yt-live-chat-author-badge-renderer[aria-label*="Hội viên mới"]) yt-live-chat-author-chip #chat-badges,
    yt-live-chat-text-message-renderer[author-type="member"]:has(yt-live-chat-author-badge-renderer[aria-label*="New member"]) yt-live-chat-author-chip #chat-badges,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(yt-live-chat-author-badge-renderer[aria-label*="Hội viên mới"]) yt-live-chat-author-chip #chat-badges,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(yt-live-chat-author-badge-renderer[aria-label*="New member"]) yt-live-chat-author-chip #chat-badges {
        display: none !important;
    }

    yt-live-chat-text-message-renderer[author-type="member"]:has(img[alt="Hội viên mới"]) yt-live-chat-author-chip #author-badges,
    yt-live-chat-text-message-renderer[author-type="member"]:has(img[alt="New member"]) yt-live-chat-author-chip #author-badges,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(img[alt="Hội viên mới"]) yt-live-chat-author-chip #author-badges,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(img[alt="New member"]) yt-live-chat-author-chip #author-badges,
    yt-live-chat-text-message-renderer[author-type="member"]:has(yt-live-chat-author-badge-renderer[aria-label*="Hội viên mới"]) yt-live-chat-author-chip #author-badges,
    yt-live-chat-text-message-renderer[author-type="member"]:has(yt-live-chat-author-badge-renderer[aria-label*="New member"]) yt-live-chat-author-chip #author-badges,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(yt-live-chat-author-badge-renderer[aria-label*="Hội viên mới"]) yt-live-chat-author-chip #author-badges,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(yt-live-chat-author-badge-renderer[aria-label*="New member"]) yt-live-chat-author-chip #author-badges {
        position: static !important;
        left: auto !important;
        top: auto !important;
        margin-left: 4px !important;
        transform: none !important;
        opacity: 1 !important;
        display: inline-flex !important;
    }

    yt-live-chat-text-message-renderer[author-type="member"]:has(img[alt="Hội viên mới"]) yt-live-chat-author-chip #author-badges img,
    yt-live-chat-text-message-renderer[author-type="member"]:has(img[alt="New member"]) yt-live-chat-author-chip #author-badges img,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(img[alt="Hội viên mới"]) yt-live-chat-author-chip #author-badges img,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(img[alt="New member"]) yt-live-chat-author-chip #author-badges img,
    yt-live-chat-text-message-renderer[author-type="member"]:has(yt-live-chat-author-badge-renderer[aria-label*="Hội viên mới"]) yt-live-chat-author-chip #author-badges img,
    yt-live-chat-text-message-renderer[author-type="member"]:has(yt-live-chat-author-badge-renderer[aria-label*="New member"]) yt-live-chat-author-chip #author-badges img,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(yt-live-chat-author-badge-renderer[aria-label*="Hội viên mới"]) yt-live-chat-author-chip #author-badges img,
    yt-live-chat-text-message-renderer[author-type="moderator"]:has(yt-live-chat-author-badge-renderer[type="member"]):has(yt-live-chat-author-badge-renderer[aria-label*="New member"]) yt-live-chat-author-chip #author-badges img {
        width: 32px !important;
        height: 32px !important;
        filter: none !important;
        opacity: 1 !important;
    }"""

new_hide_block = """    /* Hide badge container completely for New Members across all renderers (chats, welcome cards, milestone banners, etc) */
    :is(yt-live-chat-text-message-renderer, yt-live-chat-paid-message-renderer, yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer):has(img:is([alt*="Hội viên mới" i], [alt*="New member" i]), yt-live-chat-author-badge-renderer:is([aria-label*="Hội viên mới" i], [aria-label*="New member" i])) :is(yt-live-chat-author-badge-renderer, #chat-badges, #author-badges) {
        display: none !important;
    }"""

if old_hide_block in content:
    content = content.replace(old_hide_block, new_hide_block)
    print("Replaced old hide block successfully!")
else:
    # If indentation is slightly different, let's look for a fuzzy match
    print("Warning: old_hide_block not found exactly!")

# Save to a check file first
temp_file = "/Users/lap/Code/css/css_temp_check.css"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(content)

# Run check_braces on the temp file
if check_braces(temp_file):
    print("Verification passed! Writing back to css.css...")
    shutil.copy2(temp_file, source_file)
    print("Update successful!")
else:
    print("Verification failed! Restoring backup...")
    shutil.copy2(backup_file, source_file)
