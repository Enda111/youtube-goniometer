"""
Icon creation script for YouTube Goniometer.

This script generates custom icons for the application, including Windows ICO format
and various PNG sizes for different use cases.
"""

from typing import List, Union
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_goniometer_icon() -> Image.Image:
    """Create a simple goniometer icon for the YouTube Goniometer app."""
    
    # Create a 256x256 image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dark background circle
    margin = 20
    circle_bbox = [margin, margin, size - margin, size - margin]
    draw.ellipse(circle_bbox, fill=(30, 35, 45, 255), outline=(80, 90, 110, 255), width=4)
    
    # Draw goniometer grid lines
    center = size // 2
    radius = (size - margin * 2) // 2 - 10
    
    # Vertical and horizontal lines
    line_color = (100, 120, 140, 200)
    draw.line([center, margin + 10, center, size - margin - 10], fill=line_color, width=2)
    draw.line([margin + 10, center, size - margin - 10, center], fill=line_color, width=2)
    
    # Diagonal lines for mono/stereo indicators
    diag_offset = int(radius * 0.7)
    draw.line([center - diag_offset, center - diag_offset, center + diag_offset, center + diag_offset], 
              fill=line_color, width=1)
    draw.line([center - diag_offset, center + diag_offset, center + diag_offset, center - diag_offset], 
              fill=line_color, width=1)
    
    # Draw some sample goniometer pattern (L/R correlation)
    pattern_color = (100, 200, 255, 255)  # Bright blue
    
    # Create a simple stereo pattern
    for angle in range(0, 360, 5):
        rad = np.radians(angle)
        # Simulate stereo audio pattern
        r = radius * 0.6 * (0.7 + 0.3 * np.sin(angle * 0.1))
        x = int(center + r * np.cos(rad))
        y = int(center + r * np.sin(rad))
        draw.ellipse([x-2, y-2, x+2, y+2], fill=pattern_color)
    
    # Add YouTube play button symbol
    play_size = 40
    play_x = center - play_size // 3
    play_y = center - play_size // 2
    
    # Triangle for play button
    play_color = (255, 80, 80, 255)  # YouTube red
    play_points = [
        (play_x, play_y),
        (play_x, play_y + play_size),
        (play_x + int(play_size * 0.8), play_y + play_size // 2)
    ]
    draw.polygon(play_points, fill=play_color)
    
    # Add small "G" for Goniometer in corner
    font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]
    try:
        # Try to use a font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 24)
    except (OSError, IOError):
        font = ImageFont.load_default()
    
    text_color = (200, 220, 240, 255)
    draw.text((size - 40, 10), "G", fill=text_color, font=font)
    
    return img

def create_icon_files() -> None:
    """Create icon files in multiple formats and sizes."""
    
    # Create the base icon
    icon_img = create_goniometer_icon()
    
    # Save as PNG (high quality)
    icon_img.save('icon.png', 'PNG')
    print("Created: icon.png (256x256)")
    
    # Create ICO file with multiple sizes
    sizes: List[int] = [16, 32, 48, 64, 128, 256]
    ico_images: List[Image.Image] = []
    
    for size in sizes:
        resized = icon_img.resize((size, size), Image.Resampling.LANCZOS)
        ico_images.append(resized)
    
    # Save as ICO file
    ico_images[0].save('icon.ico', format='ICO', sizes=[(img.width, img.height) for img in ico_images])
    print("Created: icon.ico (multiple sizes)")
    
    # Create smaller PNG versions
    for size in [32, 64, 128]:
        resized = icon_img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f'icon_{size}.png', 'PNG')
        print(f"Created: icon_{size}.png")

if __name__ == "__main__":
    try:
        create_icon_files()
        print("\n✅ Icon files created successfully!")
        print("\nTo use with PyInstaller:")
        print("pyinstaller --onefile --windowed --icon=icon.ico --name='YouTube-Goniometer' app.py")
        
    except ImportError as e:
        print(f"❌ Missing required library: {e}")
        print("\nInstall Pillow (PIL) with:")
        print("pip install Pillow")
        
    except (OSError, IOError, ValueError) as e:
        print(f"❌ Error creating icon: {e}")