"""
Icon creation script for YouTube Goniometer.

This script generates custom icons for the application, including Windows ICO format
and various PNG sizes for different use cases.
"""

from typing import List, Tuple
from PIL import Image, ImageDraw
import numpy as np

def create_goniometer_icon() -> Image.Image:
    """Create a ultra-high-resolution 2048x2048 woven G icon with authentic braided gaps."""
    
    # Create a ultra-high-resolution 2048x2048 image with transparent background
    size = 2048
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
    
    # Create a circular G - scaled up for ultra-high resolution
    g_radius = 640  # Much larger for 2048x2048 resolution
    
    def fill_with_woven_texture(region_points: List[Tuple[int, int]], strand_direction: str = "mixed") -> None:
        """Fill a region with authentic woven texture that has gaps between strands."""
        if not region_points:
            return
            
        # Find bounding box
        min_x = min(p[0] for p in region_points)
        max_x = max(p[0] for p in region_points)
        min_y = min(p[1] for p in region_points)
        max_y = max(p[1] for p in region_points)
        
        # Create woven strands with gaps - scaled for 2048x2048
        strand_width = 12  # Width of individual strands
        gap_width = 8      # Gap between strands
        total_width = strand_width + gap_width
        
        # Draw horizontal strands
        if strand_direction in ["horizontal", "mixed"]:
            y = min_y
            while y < max_y:
                # Create slightly wavy horizontal strands
                for x in range(min_x, max_x, 4):  # High resolution sampling
                    wave_offset = int(6 * np.sin(x * 0.02 + y * 0.01))  # Weaving pattern
                    strand_y = y + wave_offset
                    
                    # Only draw if within strand area (not in gap)
                    strand_phase = (strand_y % total_width)
                    if strand_phase < strand_width:
                        # Add texture elements to the strand
                        if np.random.random() < 0.4:  # Less dense for more realistic weave
                            if np.random.random() < 0.6:  # Dots
                                dot_size = np.random.randint(2, 8)
                                alpha = np.random.randint(140, 255)
                                color_idx = int(np.random.randint(0, len(gonio_colors)))
                                base_color = gonio_colors[color_idx]
                                color = (base_color[0], base_color[1], base_color[2], alpha)
                                draw.ellipse([x - dot_size, strand_y - dot_size, 
                                            x + dot_size, strand_y + dot_size], fill=color)
                            else:  # Short horizontal lines
                                length = np.random.randint(8, 20)
                                thickness = np.random.randint(2, 6)
                                alpha = np.random.randint(120, 200)
                                color_idx = int(np.random.randint(0, len(gonio_colors)))
                                base_color = gonio_colors[color_idx]
                                color = (base_color[0], base_color[1], base_color[2], alpha)
                                draw.line([x, strand_y, x + length, strand_y], 
                                        fill=color, width=thickness)
                y += 6  # Move to next row
        
        # Draw vertical strands (interweaving)
        if strand_direction in ["vertical", "mixed"]:
            x = min_x
            while x < max_x:
                # Create slightly wavy vertical strands
                for y in range(min_y, max_y, 4):  # High resolution sampling
                    wave_offset = int(8 * np.sin(y * 0.018 + x * 0.012))  # Different weave pattern
                    strand_x = x + wave_offset
                    
                    # Only draw if within strand area and interweaving properly
                    strand_phase = (strand_x % total_width)
                    weave_phase = (y // (total_width // 2)) % 2  # Over/under pattern
                    
                    if strand_phase < strand_width:
                        # Interweaving logic - some areas hidden behind horizontal strands
                        horizontal_strand_phase = (y % total_width)
                        if horizontal_strand_phase >= strand_width or weave_phase == 1:
                            # Add texture elements to visible vertical strand
                            if np.random.random() < 0.35:  # Slightly less dense
                                if np.random.random() < 0.5:  # Dots
                                    dot_size = np.random.randint(2, 7)
                                    alpha = np.random.randint(130, 240)
                                    color_idx = int(np.random.randint(0, len(gonio_colors)))
                                    base_color = gonio_colors[color_idx]
                                    color = (base_color[0], base_color[1], base_color[2], alpha)
                                    draw.ellipse([strand_x - dot_size, y - dot_size, 
                                                strand_x + dot_size, y + dot_size], fill=color)
                                else:  # Short vertical lines
                                    length = np.random.randint(6, 16)
                                    thickness = np.random.randint(2, 5)
                                    alpha = np.random.randint(110, 190)
                                    color_idx = int(np.random.randint(0, len(gonio_colors)))
                                    base_color = gonio_colors[color_idx]
                                    color = (base_color[0], base_color[1], base_color[2], alpha)
                                    draw.line([strand_x, y, strand_x, y + length], 
                                            fill=color, width=thickness)
                x += 7  # Move to next column
    
    def create_bold_g() -> None:
        """Create a bold, clear G shape filled with goniometer texture."""
        
        # Simple, bold G dimensions - scaled for 2048x2048
        stroke_width = 180  # Much thicker strokes for ultra-high resolution
        
        # G parameters - centered and large, scaled 4x for 2048x2048
        g_left = center_x - 400
        g_right = center_x + 320
        g_top = center_y - 440
        g_bottom = center_y + 440
        g_mid_bar_y = center_y + 100
        g_mid_bar_right = center_x + 120
        
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
        
        # Top stroke region - horizontal weave
        top_region = [(g_left, g_top), (g_right - 30, g_top), 
                     (g_right - 30, g_top + stroke_width), (g_left, g_top + stroke_width)]
        fill_with_woven_texture(top_region, "horizontal")
        
        # Left stroke region - vertical weave  
        left_region = [(g_left, g_top), (g_left + stroke_width, g_top),
                      (g_left + stroke_width, g_bottom), (g_left, g_bottom)]
        fill_with_woven_texture(left_region, "vertical")
        
        # Bottom stroke region - horizontal weave
        bottom_region = [(g_left, g_bottom - stroke_width), (g_right - 30, g_bottom - stroke_width),
                        (g_right - 30, g_bottom), (g_left, g_bottom)]
        fill_with_woven_texture(bottom_region, "horizontal")
        
        # Middle bar region - horizontal weave
        mid_region = [(g_mid_bar_right - 20, g_mid_bar_y - stroke_width//2),
                     (g_right - 15, g_mid_bar_y - stroke_width//2),
                     (g_right - 15, g_mid_bar_y + stroke_width//2),
                     (g_mid_bar_right - 20, g_mid_bar_y + stroke_width//2)]
        fill_with_woven_texture(mid_region, "horizontal")
        
        # Right vertical region - vertical weave
        right_region = [(g_right - 45, g_mid_bar_y - stroke_width//2),
                       (g_right - 15, g_mid_bar_y - stroke_width//2),
                       (g_right - 15, g_bottom - stroke_width),
                       (g_right - 45, g_bottom - stroke_width)]
        fill_with_woven_texture(right_region, "vertical")
        
        # 3. Add some curved corners for a more polished look - scaled for 2048x2048
        corner_radius = 60
        
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
    
    # Add some final decorative accent dots around the entire design - scaled for 2048x2048
    for _ in range(120):  # More dots for higher resolution
        # Random dots in the overall icon area
        x = np.random.randint(200, size - 200)
        y = np.random.randint(200, size - 200)
        
        # Only add dots outside the main G area to avoid clutter
        distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        if distance_from_center > g_radius + 120:
            dot_size = np.random.randint(4, 12)  # Larger dots for 2048x2048
            alpha = np.random.randint(40, 100)
            color = (0, 255, 0, alpha)
            draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size], fill=color)
    
    return img

def create_icon_files() -> None:
    """Create icon files in multiple formats and sizes."""
    
    # Create the base icon
    icon_img = create_goniometer_icon()
    
    # Save as ultra-high resolution PNG (2048x2048)
    icon_img.save('icon.png', 'PNG')
    print(f"Created: icon.png ({icon_img.width}x{icon_img.height})")
    
    # Create ICO file with multiple sizes including high-res
    sizes: List[int] = [16, 32, 48, 64, 128, 256, 512]
    ico_images: List[Image.Image] = []
    
    for size in sizes:
        resized = icon_img.resize((size, size), Image.Resampling.LANCZOS)
        ico_images.append(resized)
    
    # Save as ICO file
    ico_images[0].save('icon.ico', format='ICO', sizes=[(img.width, img.height) for img in ico_images])
    print("Created: icon.ico (multiple sizes including 512x512)")
    
    # Create various PNG versions for different uses
    for size in [32, 64, 128, 256, 512, 1024]:
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