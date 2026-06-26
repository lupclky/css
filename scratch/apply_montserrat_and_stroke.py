import re
import shutil
from check_braces import check_braces

source_file = "/Users/lap/Code/css/css.css"
backup_file = "/Users/lap/Code/css/css_backup_temp_montserrat.css"

# Make a backup
shutil.copy2(source_file, backup_file)
print(f"Backup created at: {backup_file}")

with open(source_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace Nunito font for author names (we look for selector patterns of author names and replace font-family)
# We can do a search and replace for: font-family: "Nunito", sans-serif !important;
# But wait, there are also some other font-families we might want to change.
# Let's target all font-family definitions that are inside author name chip rules.
# We can replace all exact occurrences of `font-family: "Nunito", sans-serif !important;`
# with `font-family: "Montserrat", sans-serif !important;`
# Let's count them first.
occurrences = content.count('font-family: "Nunito", sans-serif !important;')
print(f"Found {occurrences} occurrences of Nunito font-family to replace.")

content = content.replace('font-family: "Nunito", sans-serif !important;', 'font-family: "Montserrat", sans-serif !important;')

# 2. Increase text stroke from 4.5px to 6px
# We find `-webkit-text-stroke: 4.5px #000000 !important;` and replace with `-webkit-text-stroke: 6px #000000 !important;`
stroke_occurrences = content.count('-webkit-text-stroke: 4.5px #000000 !important;')
print(f"Found {stroke_occurrences} occurrences of text stroke to replace.")

content = content.replace('-webkit-text-stroke: 4.5px #000000 !important;', '-webkit-text-stroke: 6px #000000 !important;')

# Save to temp and verify
temp_file = "/Users/lap/Code/css/css_temp_montserrat.css"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(content)

if check_braces(temp_file):
    shutil.copy2(temp_file, source_file)
    print("Verification passed and css.css updated successfully!")
else:
    print("Verification failed! Restoring backup...")
    shutil.copy2(backup_file, source_file)
