"""
generate_preview_image.py

Generates a high-resolution preview image (assets/preview.png) representing
the complete Linux terminal GitHub profile README layout.
"""

import os
# pyrefly: ignore [missing-import]
from PIL import Image, ImageDraw, ImageFont

def render_preview_png():
    print("[+] Rendering preview screenshot assets/preview.png...")
    width = 1000
    height = 1100
    bg_color = (13, 17, 23)  # #0d1117 GitHub Dark / Terminal Black
    card_bg = (22, 27, 34)   # #161b22
    border_color = (48, 54, 61) # #30363d
    text_white = (240, 246, 252)
    text_gray = (139, 148, 158)
    text_blue = (88, 166, 255)
    text_green = (57, 211, 83)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Attempt to load monospace font
    font_family = "consola.ttf"
    try:
        font_prompt = ImageFont.truetype(font_family, 15)
        font_header = ImageFont.truetype(font_family, 13)
        font_body = ImageFont.truetype(font_family, 12)
        font_large = ImageFont.truetype(font_family, 18)
    except IOError:
        font_prompt = font_header = font_body = font_large = ImageFont.load_default()

    # Draw Section 1: Prompt 1
    y = 30
    draw.text((50, y), "ragunthan@github:~$ ./contributions.sh", fill=text_blue, font=font_prompt)
    
    # Draw Heatmap Card Box
    y += 35
    heatmap_w = 900
    heatmap_h = 220
    draw.rounded_rectangle([50, y, 50 + heatmap_w, y + heatmap_h], radius=8, fill=card_bg, outline=border_color, width=2)
    
    # Terminal dots on heatmap header
    draw.ellipse([65, y + 12, 75, y + 22], fill=(255, 95, 86))
    draw.ellipse([82, y + 12, 92, y + 22], fill=(255, 189, 46))
    draw.ellipse([99, y + 12, 109, y + 22], fill=(27, 201, 63))
    draw.text((400, y + 10), "ragunthan@github: ~/contributions-heatmap", fill=text_gray, font=font_header)
    
    # Heatmap stats row inside preview
    draw.text((80, y + 45), "6", fill=text_green, font=font_large)
    draw.text((80, y + 68), "YEARLY CONTRIBUTIONS", fill=text_gray, font=font_body)

    draw.text((300, y + 45), "2 Days", fill=text_green, font=font_large)
    draw.text((300, y + 68), "CURRENT STREAK", fill=text_gray, font=font_body)

    draw.text((520, y + 45), "2 Days", fill=text_green, font=font_large)
    draw.text((520, y + 68), "LONGEST STREAK", fill=text_gray, font=font_body)

    draw.text((740, y + 45), "3 Commits", fill=text_green, font=font_large)
    draw.text((740, y + 68), "BEST DAY", fill=text_gray, font=font_body)

    # Grid squares simulation in preview
    grid_start_x = 80
    grid_start_y = y + 105
    for c in range(52):
        for r in range(7):
            gx = grid_start_x + c * 15
            gy = grid_start_y + r * 15
            color = (22, 27, 34)
            if (c * 7 + r) % 13 == 0:
                color = (38, 166, 65)
            elif (c * 7 + r) % 7 == 0:
                color = (14, 68, 41)
            elif (c * 7 + r) % 19 == 0:
                color = (57, 211, 83)
            draw.rounded_rectangle([gx, gy, gx + 11, gy + 11], radius=2, fill=color)

    # Draw Section 2: Prompt 2
    y += heatmap_h + 40
    draw.text((50, y), "ragunthan@github:~$ whoami", fill=text_blue, font=font_prompt)

    # Two columns: ASCII Portrait & Neofetch Card
    y += 35
    col_w = 435
    col_h = 600
    
    # Left Column: ASCII Portrait
    left_x = 50
    draw.rounded_rectangle([left_x, y, left_x + col_w, y + col_h], radius=8, fill=card_bg, outline=border_color, width=2)
    draw.ellipse([left_x + 15, y + 12, left_x + 25, y + 22], fill=(255, 95, 86))
    draw.ellipse([left_x + 32, y + 12, left_x + 42, y + 22], fill=(255, 189, 46))
    draw.ellipse([left_x + 49, y + 12, left_x + 59, y + 22], fill=(27, 201, 63))
    draw.text((left_x + 140, y + 10), "ragunthan@github: ~/ascii-portrait", fill=text_gray, font=font_header)

    # Insert prepped image or ASCII text simulation into left box
    if os.path.exists("data/source-prepped.png"):
        ascii_img = Image.open("data/source-prepped.png").convert("RGB").resize((380, 520))
        img.paste(ascii_img, (left_x + 27, y + 50))

    # Right Column: Neofetch Info Card
    right_x = 515
    draw.rounded_rectangle([right_x, y, right_x + col_w, y + col_h], radius=8, fill=card_bg, outline=border_color, width=2)
    draw.ellipse([right_x + 15, y + 12, right_x + 25, y + 22], fill=(255, 95, 86))
    draw.ellipse([right_x + 32, y + 12, right_x + 42, y + 22], fill=(255, 189, 46))
    draw.ellipse([right_x + 49, y + 12, right_x + 59, y + 22], fill=(27, 201, 63))
    draw.text((right_x + 140, y + 10), "ragunthan@github: ~/neofetch", fill=text_gray, font=font_header)

    # Info card text items
    info_items = [
        ("ragunthan@github", ""),
        ("----------------------------------", ""),
        ("Name", "Ragunthan P R"),
        ("Role", "Computer Science Engineering Student"),
        ("Focus", "AI, Cloud, DevOps, Full Stack, Cyber Security"),
        ("Languages", "Python, Java, C, JavaScript, SQL"),
        ("Frameworks", "React, Node.js, Express, Tailwind CSS"),
        ("Tools", "Git, GitHub, Docker, Linux, VS Code"),
        ("Current Project", "AI Powered GitHub Automation"),
        ("Learning", "AWS, Kubernetes, CI/CD, Machine Learning"),
    ]

    iy = y + 50
    for key, val in info_items:
        if val == "":
            if "ragunthan" in key:
                draw.text((right_x + 25, iy), key, fill=text_blue, font=font_prompt)
            else:
                draw.text((right_x + 25, iy), key, fill=border_color, font=font_body)
        else:
            draw.text((right_x + 25, iy), f"{key}:", fill=text_gray, font=font_body)
            draw.text((right_x + 160, iy), val, fill=text_white, font=font_body)
        iy += 38

    os.makedirs("assets", exist_ok=True)
    out_path = "assets/preview.png"
    img.save(out_path, "PNG")
    print(f"[OK] Saved preview image to {out_path}")

if __name__ == "__main__":
    render_preview_png()
