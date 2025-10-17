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
    
    def draw_curved_gonio_trace(points: List[tuple], density: int = 4, line_width: int = 3) -> None:
        """Draw a curved goniometer trace made of many overlapping small lines."""
        if len(points) < 2:
            return
            
        # Create smooth curve through points using interpolation
        smooth_points = []
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            # Add intermediate points for smoothness
            for t in np.linspace(0, 1, density):
                # Add slight curve variation for organic goniometer look
                curve_offset = np.sin(t * np.pi) * 3
                x = int(x1 + t * (x2 - x1) + np.random.uniform(-curve_offset, curve_offset))
                y = int(y1 + t * (y2 - y1) + np.random.uniform(-curve_offset, curve_offset))
                smooth_points.append((x, y))
        
        # Draw overlapping short line segments
        for i in range(len(smooth_points) - 1):
            x1, y1 = smooth_points[i]
            x2, y2 = smooth_points[i + 1]
            
            # Vary line properties for authentic goniometer look
            intensity = 0.7 + 0.3 * np.sin(i * 0.2)
            alpha = int(120 + 80 * intensity)
            thickness = line_width + int(np.sin(i * 0.15) * 1.5)
            
            # Multiple overlapping lines for thickness and glow
            for offset in range(-thickness//2, thickness//2 + 1):
                for brightness in [0.6, 0.8, 1.0]:
                    line_alpha = int(alpha * brightness)
                    color = (0, 255, 0, line_alpha)
                    
                    # Draw slightly offset lines for thickness
                    draw.line([x1 + offset, y1, x2 + offset, y2], fill=color, width=1)
                    if offset != 0:  # Add perpendicular offset too
                        draw.line([x1, y1 + offset, x2, y2 + offset], fill=color, width=1)
    
    # Create curved "G" shape with flowing goniometer traces
    
    # Top curve - more stylized arc
    top_points = []
    for t in np.linspace(0, 1, 12):
        # Create curved top with gentle arc
        x = start_x + t * (g_width - 30)
        curve_height = 15 * np.sin(t * np.pi * 0.7)  # Gentle downward curve
        y = start_y - curve_height
        top_points.append((int(x), int(y)))
    draw_curved_gonio_trace(top_points, density=6, line_width=4)
    
    # Left curve - flowing S-curve
    left_points = []
    for t in np.linspace(0, 1, 20):
        # Create flowing left edge with S-curve
        curve_offset = 12 * np.sin(t * np.pi * 1.5) * (1 - t * 0.3)
        x = start_x + curve_offset
        y = start_y + t * g_height
        left_points.append((int(x), int(y)))
    draw_curved_gonio_trace(left_points, density=5, line_width=5)
    
    # Bottom curve - elegant arc
    bottom_points = []
    for t in np.linspace(0, 1, 10):
        x = start_x + 5 + t * (g_width - 35)
        curve_height = 12 * np.sin(t * np.pi * 0.8)  # Gentle upward curve
        y = start_y + g_height + curve_height
        bottom_points.append((int(x), int(y)))
    draw_curved_gonio_trace(bottom_points, density=6, line_width=4)
    
    # Middle bar - curved with tapering
    mid_y = start_y + g_height // 2 + 8
    middle_points = []
    for t in np.linspace(0, 1, 8):
        curve_variation = 6 * np.sin(t * np.pi)
        x = start_x + g_width // 2 + t * (g_width // 2 - 20)
        y = mid_y + curve_variation * (0.5 - abs(t - 0.5))  # Curve up in middle
        middle_points.append((int(x), int(y)))
    draw_curved_gonio_trace(middle_points, density=5, line_width=4)
    
    # Right vertical - curved with slight bow
    right_points = []
    right_start_y = mid_y - 5
    for t in np.linspace(0, 1, 12):
        curve_bow = 8 * np.sin(t * np.pi) * 0.7  # Slight outward bow
        x = start_x + g_width - 22 + curve_bow
        y = right_start_y + t * (start_y + g_height - right_start_y + 5)
        right_points.append((int(x), int(y)))
    draw_curved_gonio_trace(right_points, density=5, line_width=4)
    
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