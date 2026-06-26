import urllib.parse

# Define the new high-fidelity cartoon pineapple leaf SVG
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <g stroke="#1e3a00" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">
    <!-- Bottom-most row (pointing out and slightly down) -->
    <path d="M16 25 C11 26 5 24 3 20 C3 16 7 16 11 18 C13 19 15 21 16 23" fill="#15803d" />
    <path d="M16 25 C21 26 27 24 29 20 C29 16 25 16 21 18 C19 19 17 21 16 23" fill="#15803d" />
    
    <!-- Middle row (pointing out and up) -->
    <path d="M16 21 C10 21 6 18 4 13 C5 10 9 10 12 12 C14 13 15 15 16 17" fill="#16a34a" />
    <path d="M16 21 C22 21 26 18 28 13 C27 10 23 10 20 12 C18 13 17 15 16 17" fill="#16a34a" />
    
    <!-- Upper row (pointing mostly up) -->
    <path d="M16 17 C11 17 8 13 6 8 C8 5 11 5 13 7 C15 8 16 10 16 12" fill="#4ade80" />
    <path d="M16 17 C21 17 24 13 26 8 C24 5 21 5 19 7 C17 8 16 10 16 12" fill="#4ade80" />
    
    <!-- Top-most center leaf (vertical) -->
    <path d="M16 14 C13 14 13 7 16 2 C19 7 19 14 16 14" fill="#a3e635" />
  </g>
  <!-- Highlights for a shiny cartoon look -->
  <g fill="none" stroke-linecap="round">
    <!-- Light green highlights on upper leaves -->
    <path d="M8 8 C10 7 11 7 12 7" stroke="#bef264" stroke-width="0.8" />
    <path d="M24 8 C22 7 21 7 20 7" stroke="#bef264" stroke-width="0.8" />
    <!-- Yellow center highlight -->
    <path d="M16 10 C15.5 8 15.5 5 16 3.5" stroke="#fef08a" stroke-width="0.8" />
  </g>
</svg>"""

# Encode SVG content for CSS
encoded_svg = urllib.parse.quote(svg_content)
svg_data_uri = f'data:image/svg+xml,{encoded_svg}'

# Open and modify css.css
css_path = "/Users/lap/Code/css/css.css"
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Locate the background-image rule for the pineapple leaves and replace it
# Look for the block under `/* Add pineapple leaves on top of 6+ months members' avatars ... */`
import re

# We will search for the background-image URL inside the ::after pseudo-element of the pineapple leaves section
pattern = r'(#author-photo::after\s*\{[^}]*background-image:\s*url\(")([^"]*)("\)[^}]*\})'
matches = re.findall(pattern, css_content)
print(f"Found {len(matches)} background-image slots in ::after")

# Replace in css_content
new_css_content = re.sub(
    r'(#author-photo::after\s*\{[^}]*background-image:\s*url\(")([^"]*)("\)[^}]*\})',
    r'\g<1>' + svg_data_uri + r'\g<3>',
    css_content
)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(new_css_content)

print("css.css updated successfully!")

# Also check braces to make sure it's valid
from check_braces import check_braces
check_braces(css_path)
