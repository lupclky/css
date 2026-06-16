import os
from PIL import Image
import colorsys

badge_dir = "/Users/lap/Code/css/scratch/badges"

for filename in sorted(os.listdir(badge_dir)):
    if not filename.endswith(".png"):
        continue
    
    img_path = os.path.join(badge_dir, filename)
    img = Image.open(img_path).convert("RGBA")
    
    hues = []
    sats = []
    vals = []
    
    for x in range(img.width):
        for y in range(img.height):
            r, g, b, a = img.getpixel((x, y))
            if a > 50:  # non-transparent pixel
                # ignore white/black/gray (low saturation)
                h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                if s > 0.15 and v > 0.15:
                    hues.append(h * 360)
                    sats.append(s)
                    vals.append(v)
                    
    if hues:
        avg_hue = sum(hues) / len(hues)
        avg_sat = sum(sats) / len(sats)
        avg_val = sum(vals) / len(vals)
        
        # Classify color based on hue
        color_name = "unknown"
        if avg_hue < 15 or avg_hue > 345:
            color_name = "red"
        elif 15 <= avg_hue < 45:
            color_name = "orange/brown"
        elif 45 <= avg_hue < 75:
            color_name = "yellow"
        elif 75 <= avg_hue < 165:
            color_name = "green"
        elif 165 <= avg_hue < 255:
            color_name = "cyan/blue"
        elif 255 <= avg_hue < 315:
            color_name = "purple/violet"
        elif 315 <= avg_hue <= 345:
            color_name = "pink/magenta"
            
        print(f"{filename}: Hue={avg_hue:.1f} ({color_name}), Sat={avg_sat:.2f}, Val={avg_val:.2f}")
    else:
        print(f"{filename}: No colored pixels found")
