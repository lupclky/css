import base64
import re
from check_braces import check_braces

# Step 1: Read and base64-encode the leaves image
image_path = "/Users/lap/Code/css/scratch/badges/leaves_only.png"
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

png_data_uri = f"data:image/png;base64,{encoded_string}"
print(f"Base64 Data URI length: {len(png_data_uri)}")

# Step 2: Open css.css and perform replacements
css_path = "/Users/lap/Code/css/css.css"
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Let's find the `#author-photo::after` block for the pineapple leaves
# We want to replace:
# 1. background-image: url(...)
# 2. width: 22px !important;
# 3. height: 22px !important;
# 4. top: -17px !important;

target_block = """    :is(yt-live-chat-text-message-renderer, yt-live-chat-paid-message-renderer, yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer):not([author-type="owner"]):not(:has(yt-live-chat-author-badge-renderer[type="owner"])):has(img:is([alt*="6 month" i], [alt*="6 tháng" i], [alt*="7 month" i], [alt*="7 tháng" i], [alt*="8 month" i], [alt*="8 tháng" i], [alt*="9 month" i], [alt*="9 tháng" i], [alt*="10 month" i], [alt*="10 tháng" i], [alt*="11 month" i], [alt*="11 tháng" i], [alt*="12 month" i], [alt*="12 tháng" i], [alt*="24 month" i], [alt*="24 tháng" i], [alt*="36 month" i], [alt*="36 tháng" i], [alt*="48 month" i], [alt*="48 tháng" i], [alt*="year" i], [alt*="năm" i])) #author-photo::after {"""

# Let's find where Y starts after this block in css.css.
# We will view/locate the block precisely in the file.
# Let's write a python search-and-replace for the exact CSS rule.

# The original block in css.css Y=4092 is:
#     :is(yt-live-chat-text-message-renderer, yt-live-chat-paid-message-renderer, yt-live-chat-membership-item-renderer, ytd-sponsorships-live-chat-gift-purchase-announcement-renderer, ytd-sponsorships-live-chat-gift-redemption-announcement-renderer):not([author-type="owner"]):not(:has(yt-live-chat-author-badge-renderer[type="owner"])):has(img:is([alt*="6 month" i], [alt*="6 tháng" i], [alt*="7 month" i], [alt*="7 tháng" i], [alt*="8 month" i], [alt*="8 tháng" i], [alt*="9 month" i], [alt*="9 tháng" i], [alt*="10 month" i], [alt*="10 tháng" i], [alt*="11 month" i], [alt*="11 tháng" i], [alt*="12 month" i], [alt*="12 tháng" i], [alt*="24 month" i], [alt*="24 tháng" i], [alt*="36 month" i], [alt*="36 tháng" i], [alt*="48 month" i], [alt*="48 tháng" i], [alt*="year" i], [alt*="năm" i])) #author-photo::after {
#         content: "" !important;
#         position: absolute !important;
#         top: -17px !important;
#         left: 50% !important;
#         transform: translateX(-50%) translateZ(10px) !important;
#         width: 22px !important;
#         height: 22px !important;
#         background-image: url(...) !important;
#         background-size: contain !important;
#         background-repeat: no-repeat !important;
#         background-position: center bottom !important;
#         z-index: 99999 !important;
#         pointer-events: none !important;
#         filter: drop-shadow(1px 2px 2px rgba(0, 0, 0, 0.45)) !important;
#     }

# We can replace the inner property lines inside this block.
old_rules = """        top: -17px !important;
        left: 50% !important;
        transform: translateX(-50%) translateZ(10px) !important;
        width: 22px !important;
        height: 22px !important;
        background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2032%2032%22%3E%0A%20%20%3Cg%20stroke%3D%22%231e3a00%22%20stroke-width%3D%221.8%22%20stroke-linejoin%3D%22round%22%20stroke-linecap%3D%22round%22%3E%0A%20%20%20%20%3C%21--%20Bottom-most%20row%20%28pointing%20out%20and%20slightly%20down%29%20--%3E%0A%20%20%20%20%3Cpath%20d%3D%22M16%2025%20C11%2026%205%2024%203%2020%20C3%2016%207%2016%2011%2018%20C13%2019%2015%2021%2016%2023%22%20fill%3D%22%2315803d%22%20/%3E%0A%20%20%20%20%3Cpath%20d%3D%22M16%2025%20C21%2026%2027%2024%2029%2020%20C29%2016%2025%2016%2021%2018%20C19%2019%2017%2021%2016%2023%22%20fill%3D%22%2315803d%22%20/%3E%0A%20%20%20%20%0A%20%20%20%20%3C%21--%20Middle%20row%20%28pointing%20out%20and%20up%29%20--%3E%0A%20%20%20%20%3Cpath%20d%3D%22M16%2021%20C10%2021%206%2018%204%2013%20C5%2010%209%2010%2012%2012%20C14%2013%2015%2015%2016%2017%22%20fill%3D%22%2316a34a%22%20/%3E%0A%20%20%20%20%3Cpath%20d%3D%22M16%2021%20C22%2021%2026%2018%2028%2013%20C27%2010%2023%2010%2020%2012%20C18%2013%2017%2015%2016%2017%22%20fill%3D%22%2316a34a%22%20/%3E%0A%20%20%20%20%0A%20%20%20%20%3C%21--%20Upper%20row%20%28pointing%20mostly%20up%29%20--%3E%0A%20%20%20%20%3Cpath%20d%3D%22M16%2017%20C11%2017%208%2013%206%208%20C8%205%2011%205%2013%207%20C15%208%2016%2010%2016%2012%22%20fill%3D%22%234ade80%22%20/%3E%0A%20%20%20%20%3Cpath%20d%3D%22M16%2017%20C21%2017%2024%2013%2026%208%20C24%205%2021%205%2019%207%20C17%208%2016%2010%2016%2012%22%20fill%3D%22%234ade80%22%20/%3E%0A%20%20%20%20%0A%20%20%20%20%3C%21--%20Top-most%20center%20leaf%20%28vertical%29%20--%3E%0A%20%20%20%20%3Cpath%20d%3D%22M16%2014%20C13%2014%2013%207%2016%202%20C19%207%2019%2014%2016%2014%22%20fill%3D%22%23a3e635%22%20/%3E%0A%20%20%3C/g%3E%0A%20%20%3C%21--%20Highlights%20for%20a%20shiny%20cartoon%20look%20--%3E%0A%20%20%3Cg%20fill%3D%22none%22%20stroke-linecap%3D%22round%22%3E%0A%20%20%20%20%3C%21--%20Light%20green%20highlights%20on%20upper%20leaves%20--%3E%0A%20%20%20%20%3Cpath%20d%3D%22M8%208%20C10%207%2011%207%2012%207%22%20stroke%3D%22%23bef264%22%20stroke-width%3D%220.8%22%20/%3E%0A%20%20%20%20%3Cpath%20d%3D%22M24%208%20C22%207%2021%207%2020%207%22%20stroke%3D%22%23bef264%22%20stroke-width%3D%220.8%22%20/%3E%0A%20%20%20%20%3C%21--%20Yellow%20center%20highlight%20--%3E%0A%20%20%20%20%3Cpath%20d%3D%22M16%2010%20C15.5%208%2015.5%205%2016%203.5%22%20stroke%3D%22%23fef08a%22%20stroke-width%3D%220.8%22%20/%3E%0A%20%20%3C/g%3E%0A%3C/svg%3E") !important;"""

# We'll replace them with the cropped original leaves PNG base64, with width: 24px, height: 14px, top: -12px
new_rules = f"""        top: -12px !important;
        left: 50% !important;
        transform: translateX(-50%) translateZ(10px) !important;
        width: 24px !important;
        height: 14px !important;
        background-image: url("{png_data_uri}") !important;"""

if old_rules in css_content:
    print("Found exact old rules!")
    css_content = css_content.replace(old_rules, new_rules)
else:
    # If indentation is slightly different, let's do a regex replacement
    # Using regex to find background-image and properties under the selector
    print("Exact match not found, running regex replacement...")
    # Matches #author-photo::after block and replaces top, width, height, and background-image
    pattern = r'(#author-photo::after\s*\{[^}]*content:[^;]*;[^}]*position:[^;]*;)([^}]+)'
    
    def repl(m):
        prefix = m.group(1)
        body = m.group(2)
        # Update top, width, height, background-image
        body = re.sub(r'top:\s*-[0-9]+px\s*!important;', 'top: -12px !important;', body)
        body = re.sub(r'width:\s*[0-9]+px\s*!important;', 'width: 24px !important;', body)
        body = re.sub(r'height:\s*[0-9]+px\s*!important;', 'height: 14px !important;', body)
        # Replace background-image URL
        body = re.sub(r'background-image:[^;]+!important;', f'background-image: url("{png_data_uri}") !important;', body)
        return prefix + body

    css_content = re.sub(pattern, repl, css_content)

# Write out to css.css
with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

# Check braces
if check_braces(css_path):
    print("Successfully replaced with base64 original PNG leaves!")
else:
    print("Brace match verification failed!")
