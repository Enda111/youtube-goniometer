"""
Icon creation script for YouTube Goniometer.

This script generates custom icons for the application, including Windows ICO format
and various PNG sizes for different use cases.
"""

from typing import List, Union
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_goniometer_icon() -> Image.Image:
    """Create a goniometer-style 'G' icon made of dots and lines."""
    
    # Create a 256x256 image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dark background circle
    margin = 20
    circle_bbox = [margin, margin, size - margin, size - margin]
    draw.ellipse(circle_bbox, fill=(20, 20, 30, 255), outline=(60, 60, 80, 255), width=3)
    
    # Goniometer green color (same as the app)
    gonio_green = (0, 255, 0, 200)
    gonio_green_bright = (0, 255, 0, 255)
    gonio_green_dim = (0, 200, 0, 150)
    
    center_x, center_y = size // 2, size // 2
    
    # Create a "G" shape using goniometer dots and lines
    # G is roughly 120x140 pixels, centered
    g_width = 120
    g_height = 140
    start_x = center_x - g_width // 2
    start_y = center_y - g_height // 2
    
    def draw_gonio_line(x1: int, y1: int, x2: int, y2: int, density: int = 8) -> None:
        """Draw a line made of goniometer-style dots."""
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        num_dots = max(2, int(distance / density))
        
        for i in range(num_dots):
            t = i / (num_dots - 1) if num_dots > 1 else 0
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            
            # Vary dot size and brightness slightly for organic look
            dot_size = 2 + int(np.sin(i * 0.3) * 0.5)
            color = gonio_green if i % 3 == 0 else gonio_green_dim
            draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size], fill=color)
    
    # Draw the "G" shape with goniometer-style dotted lines
    
    # Top horizontal line
    draw_gonio_line(start_x, start_y, start_x + g_width - 20, start_y, 6)
    
    # Left vertical line (full height)
    draw_gonio_line(start_x, start_y, start_x, start_y + g_height, 7)
    
    # Bottom horizontal line
    draw_gonio_line(start_x, start_y + g_height, start_x + g_width - 20, start_y + g_height, 6)
    
    # Middle horizontal line (for the G)
    mid_y = start_y + g_height // 2 + 10
    draw_gonio_line(start_x + g_width // 2, mid_y, start_x + g_width - 20, mid_y, 5)
    
    # Right vertical line (bottom half only)
    draw_gonio_line(start_x + g_width - 20, mid_y, start_x + g_width - 20, start_y + g_height, 6)
    
    # Add some extra goniometer-style scatter points around the G for authenticity
    for _ in range(25):
        # Random points near the G shape
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(g_width * 0.6, g_width * 0.8)
        x = int(center_x + radius * np.cos(angle))
        y = int(center_y + radius * np.sin(angle))
        
        # Only draw if reasonably close to the G shape
        if (start_x - 20 <= x <= start_x + g_width + 20 and 
            start_y - 20 <= y <= start_y + g_height + 20):
            dot_size = np.random.randint(1, 3)
            alpha = np.random.randint(80, 150)
            color = (0, 255, 0, alpha)
            draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size], fill=color)
    
    # Add subtle crosshairs in background (like goniometer display)
    crosshair_color = (60, 80, 60, 100)
    draw.line([center_x, margin + 15, center_x, size - margin - 15], fill=crosshair_color, width=1)
    draw.line([margin + 15, center_y, size - margin - 15, center_y], fill=crosshair_color, width=1)
    
    # Add some bright accent dots at key points
    key_points = [
        (start_x, start_y),  # Top left
        (start_x + g_width - 20, start_y + g_height),  # Bottom right
        (start_x + g_width - 20, mid_y),  # Middle right
    ]
    
    for x, y in key_points:
        draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=gonio_green_bright)
    
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