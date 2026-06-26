import shutil
from check_braces import check_braces

source_file = "/Users/lap/Code/css/css.css"
backup_file = "/Users/lap/Code/css/css_backup_temp_leaves.css"

# Step 1: Make a backup of the original file
shutil.copy2(source_file, backup_file)
print(f"Created backup at: {backup_file}")

with open(source_file, "r", encoding="utf-8") as f:
    content = f.read()

# Define replacement strings
old_6m_selector = 'img[alt*="6 month" i], img[alt*="6 tháng" i], img[alt*="7 month" i], img[alt*="7 tháng" i], img[alt*="8 month" i], img[alt*="8 tháng" i], img[alt*="9 month" i], img[alt*="9 tháng" i], img[alt*="10 month" i], img[alt*="10 tháng" i], img[alt*="11 month" i], img[alt*="11 tháng" i], img[alt*="year" i], img[alt*="năm" i]'

new_6m_selector = 'img:is([alt*="6 month" i], [alt*="6 tháng" i], [alt*="7 month" i], [alt*="7 tháng" i], [alt*="8 month" i], [alt*="8 tháng" i], [alt*="9 month" i], [alt*="9 tháng" i], [alt*="10 month" i], [alt*="10 tháng" i], [alt*="11 month" i], [alt*="11 tháng" i], [alt*="12 month" i], [alt*="12 tháng" i], [alt*="24 month" i], [alt*="24 tháng" i], [alt*="36 month" i], [alt*="36 tháng" i], [alt*="48 month" i], [alt*="48 tháng" i], [alt*="year" i], [alt*="năm" i])'

old_t5_animation = 'img[alt*="1 year" i], img[alt*="1 năm" i], img[alt*="12 month" i], img[alt*="12 tháng" i], img[alt*="13 month" i], img[alt*="13 tháng" i], img[alt*="23 month" i], img[alt*="23 tháng" i], img[alt*="2 year" i], img[alt*="2 năm" i], img[alt*="3 year" i], img[alt*="3 năm" i], img[alt*="4 year" i], img[alt*="4 năm" i]'

new_t5_animation = 'img:is([alt*="1 year" i], [alt*="1 năm" i], [alt*="12 month" i], [alt*="12 tháng" i], [alt*="13 month" i], [alt*="13 tháng" i], [alt*="23 month" i], [alt*="23 tháng" i], [alt*="24 month" i], [alt*="24 tháng" i], [alt*="36 month" i], [alt*="36 tháng" i], [alt*="48 month" i], [alt*="48 tháng" i], [alt*="2 year" i], [alt*="2 năm" i], [alt*="3 year" i], [alt*="3 năm" i], [alt*="4 year" i], [alt*="4 năm" i])'

# Count occurrences before replacing
occ_6m = content.count(old_6m_selector)
occ_t5 = content.count(old_t5_animation)

print(f"Found {occ_6m} occurrences of the 6+ months selector list.")
print(f"Found {occ_t5} occurrences of the Tier 5 animation selector list.")

# Perform replacements
content = content.replace(old_6m_selector, new_6m_selector)
content = content.replace(old_t5_animation, new_t5_animation)

# Adjust Pineapple leaves top offset slightly for a better visual look (e.g., top: -17px instead of top: -15px)
old_leaves_top = 'top: -15px !important;'
new_leaves_top = 'top: -17px !important;'
leaves_top_occ = content.count(old_leaves_top)
print(f"Found {leaves_top_occ} occurrences of leaves top offset style.")
content = content.replace(old_leaves_top, new_leaves_top)

# Save changes temporarily to check
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
