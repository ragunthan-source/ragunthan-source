"""
generate_starter_photo.py

Generates a high-contrast developer portrait for data/input_photo.png.
"""

# pyrefly: ignore [missing-import]
from PIL import Image, ImageDraw
import os

def create_portrait():
    width, height = 400, 500
    img = Image.new("RGBA", (width, height), (240, 240, 245, 255))
    draw = ImageDraw.Draw(img)

    # Draw shoulders / body
    draw.ellipse([50, 280, 350, 550], fill=(25, 30, 40, 255))
    
    # Hoodie collar
    draw.polygon([(150, 300), (200, 380), (250, 300)], fill=(15, 18, 25, 255))
    
    # Neck
    draw.rectangle([160, 230, 240, 310], fill=(220, 180, 150, 255))
    
    # Face outline
    draw.ellipse([110, 80, 290, 280], fill=(235, 195, 165, 255))
    
    # Hair
    draw.ellipse([95, 50, 305, 180], fill=(30, 25, 20, 255))
    draw.polygon([(95, 140), (120, 210), (140, 150)], fill=(30, 25, 20, 255))
    draw.polygon([(305, 140), (280, 210), (260, 150)], fill=(30, 25, 20, 255))
    
    # Glasses
    draw.rounded_rectangle([130, 145, 185, 185], radius=5, outline=(20, 20, 20, 255), width=6)
    draw.rounded_rectangle([215, 145, 270, 185], radius=5, outline=(20, 20, 20, 255), width=6)
    draw.line([(185, 162), (215, 162)], fill=(20, 20, 20, 255), width=5)
    
    # Eyes
    draw.ellipse([148, 158, 168, 172], fill=(40, 30, 20, 255))
    draw.ellipse([233, 158, 253, 172], fill=(40, 30, 20, 255))
    
    # Nose & Smile
    draw.line([(200, 175), (195, 205), (205, 205)], fill=(190, 145, 125, 255), width=4)
    draw.arc([155, 200, 245, 250], start=20, end=160, fill=(30, 25, 20, 255), width=5)

    os.makedirs("data", exist_ok=True)
    output_path = "data/input_photo.png"
    img.save(output_path, "PNG")
    print(f"[OK] Created starter portrait at {output_path}")

if __name__ == "__main__":
    create_portrait()
