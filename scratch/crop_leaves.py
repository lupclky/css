from PIL import Image

img_path = "/Users/lap/Code/css/scratch/badges/tier2_2_5m.png"
img = Image.open(img_path).convert("RGBA")
width, height = img.size

# Leaves are from Y=0 to Y=17
leaves_bottom_y = 17

# Find bounding box for non-transparent pixels in Y=0 to Y=17
min_x = width
max_x = 0
min_y = height
max_y = 0

for y in range(leaves_bottom_y + 1):
    for x in range(width):
        r, g, b, a = img.getpixel((x, y))
        if a > 0:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

print(f"Bounding box: X: {min_x} to {max_x}, Y: {min_y} to {max_y}")

# Crop the leaves
cropped_img = img.crop((min_x, min_y, max_x + 1, max_y + 1))
cropped_path = "/Users/lap/Code/css/scratch/badges/leaves_only.png"
cropped_img.save(cropped_path)
print(f"Saved cropped leaves to: {cropped_path}")
