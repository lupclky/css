import re
import os

file_path = '/Users/lap/Code/css/css3.css'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove standard CSS comments /* ... */
# Non-greedy match, DOTALL to match newlines
content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

# Remove encoded XML comments in data URIs %3C!-- ... --%3E
# Case insensitive for hex codes just in case, though usually uppercase
content = re.sub(r'%3C!--.*?--%3E', '', content, flags=re.IGNORECASE)

# Remove literal XML comments <!-- ... --> just in case
content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Comments removed.")
