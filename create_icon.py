"""
Icon creation script for YouTube Goniometer.

This script generates custom icons for the application, including Windows ICO format
and various PNG sizes for different use cases.
"""

from typing import List, Tuple
from PIL import Image, ImageDraw
import numpy as np

def create_goniometer_icon() -> Image.Image:
    """Create a high-resolution braided circular G icon made of intertwined lines and dots."""
    
    # Create a high-resolution 512x512 image with transparent background
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dark background circle with subtle gradient
    margin = 40
    circle_bbox = [margin, margin, size - margin, size - margin]
    draw.ellipse(circle_bbox, fill=(15, 18, 25, 255), outline=(40, 50, 65, 255), width=6)
    
    # Enhanced goniometer colors for braided effect
    gonio_colors = [
        (0, 255, 0, 220),      # Bright green
        (20, 235, 20, 200),    # Slightly dimmer
        (40, 215, 40, 180),    # Medium
        (0, 200, 50, 160),     # Darker green
        (0, 180, 80, 140),     # Even darker
    ]
    
    center_x, center_y = size // 2, size // 2
    
    # Create a circular G - much larger and more prominent
    g_radius = 160  # Much larger for high resolution
    
    def fill_with_gonio_texture(region_points: List[Tuple[int, int]]) -> None:
        """Fill a region with goniometer-style dots and small lines."""
        if not region_points:
            return
            
        # Find bounding box
        min_x = min(p[0] for p in region_points)
        max_x = max(p[0] for p in region_points)
        min_y = min(p[1] for p in region_points)
        max_y = max(p[1] for p in region_points)
        
        # Fill with goniometer texture
        for _ in range(300):  # Many texture elements
            x = np.random.randint(min_x, max_x)
            y = np.random.randint(min_y, max_y)
            
            # Check if point is inside the region (simple approximation)
            if (min_x <= x <= max_x and min_y <= y <= max_y):
                # Random texture element
                if np.random.random() < 0.7:  # Dots
                    dot_size = np.random.randint(1, 4)
                    alpha = np.random.randint(120, 255)
                    color_idx = int(np.random.randint(0, len(gonio_colors)))
                    base_color = gonio_colors[color_idx]
                    color = (base_color[0], base_color[1], base_color[2], alpha)
                    draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size], fill=color)
                else:  # Small lines
                    length = np.random.randint(3, 8)
                    angle = np.random.uniform(0, 2 * np.pi)
                    x2 = int(x + length * np.cos(angle))
                    y2 = int(y + length * np.sin(angle))
                    alpha = np.random.randint(100, 200)
                    color_idx = int(np.random.randint(0, len(gonio_colors)))
                    base_color = gonio_colors[color_idx]
                    color = (base_color[0], base_color[1], base_color[2], alpha)
                    draw.line([x, y, x2, y2], fill=color, width=2)
    
    def create_bold_g() -> None:
        """Create a bold, clear G shape filled with goniometer texture."""
        
        # Simple, bold G dimensions
        stroke_width = 45  # Thick strokes for clarity
        
        # G parameters - centered and large
        g_left = center_x - 100
        g_right = center_x + 80
        g_top = center_y - 110
        g_bottom = center_y + 110
        g_mid_bar_y = center_y + 25
        g_mid_bar_right = center_x + 30
        
        # 1. Draw the main C-shape outline first (thick green border)
        
        # Top horizontal line
        draw.rectangle([g_left, g_top, g_right - 30, g_top + stroke_width], 
                      fill=(0, 255, 0, 200))
        
        # Left vertical line
        draw.rectangle([g_left, g_top, g_left + stroke_width, g_bottom], 
                      fill=(0, 255, 0, 200))
        
        # Bottom horizontal line  
        draw.rectangle([g_left, g_bottom - stroke_width, g_right - 30, g_bottom], 
                      fill=(0, 255, 0, 200))
        
        # Middle horizontal bar (G's distinguishing feature)
        draw.rectangle([g_mid_bar_right - 20, g_mid_bar_y - stroke_width//2, 
                       g_right - 15, g_mid_bar_y + stroke_width//2], 
                      fill=(0, 255, 0, 200))
        
        # Right vertical line (from middle bar down)
        draw.rectangle([g_right - 45, g_mid_bar_y - stroke_width//2, 
                       g_right - 15, g_bottom - stroke_width], 
                      fill=(0, 255, 0, 200))
        
        # 2. Fill the strokes with goniometer texture
        
        # Top stroke region
        top_region = [(g_left, g_top), (g_right - 30, g_top), 
                     (g_right - 30, g_top + stroke_width), (g_left, g_top + stroke_width)]
        fill_with_gonio_texture(top_region)
        
        # Left stroke region  
        left_region = [(g_left, g_top), (g_left + stroke_width, g_top),
                      (g_left + stroke_width, g_bottom), (g_left, g_bottom)]
        fill_with_gonio_texture(left_region)
        
        # Bottom stroke region
        bottom_region = [(g_left, g_bottom - stroke_width), (g_right - 30, g_bottom - stroke_width),
                        (g_right - 30, g_bottom), (g_left, g_bottom)]
        fill_with_gonio_texture(bottom_region)
        
        # Middle bar region
        mid_region = [(g_mid_bar_right - 20, g_mid_bar_y - stroke_width//2),
                     (g_right - 15, g_mid_bar_y - stroke_width//2),
                     (g_right - 15, g_mid_bar_y + stroke_width//2),
                     (g_mid_bar_right - 20, g_mid_bar_y + stroke_width//2)]
        fill_with_gonio_texture(mid_region)
        
        # Right vertical region
        right_region = [(g_right - 45, g_mid_bar_y - stroke_width//2),
                       (g_right - 15, g_mid_bar_y - stroke_width//2),
                       (g_right - 15, g_bottom - stroke_width),
                       (g_right - 45, g_bottom - stroke_width)]
        fill_with_gonio_texture(right_region)
        
        # 3. Add some curved corners for a more polished look
        corner_radius = 15
        
        # Round the outer corners slightly
        for corner_x, corner_y in [(g_left, g_top), (g_left, g_bottom), 
                                  (g_right - 30, g_top)]:
            for angle in np.linspace(0, np.pi/2, 10):
                x = int(corner_x + corner_radius * np.cos(angle))
                y = int(corner_y + corner_radius * np.sin(angle))
                dot_size = 3
                draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size], 
                           fill=(0, 255, 0, 150))
    
    # Create the bold, clear G
    create_bold_g()
    
    # Add subtle crosshairs in background (like goniometer display)
    crosshair_color = (60, 80, 60, 100)
    draw.line([center_x, margin + 15, center_x, size - margin - 15], fill=crosshair_color, width=1)
    draw.line([margin + 15, center_y, size - margin - 15, center_y], fill=crosshair_color, width=1)
    
    # Add some final decorative accent dots around the entire design
    for _ in range(30):
        # Random dots in the overall icon area
        x = np.random.randint(50, size - 50)
        y = np.random.randint(50, size - 50)
        
        # Only add dots outside the main G area to avoid clutter
        distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        if distance_from_center > g_radius + 30:
            dot_size = np.random.randint(1, 3)
            alpha = np.random.randint(40, 100)
            color = (0, 255, 0, alpha)
            draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size], fill=color)
    
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