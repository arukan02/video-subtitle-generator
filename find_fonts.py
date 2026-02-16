"""
Find available fonts on your Windows system
This will help you choose the right font paths
"""

import os
from pathlib import Path

print("Searching for fonts on your system...\n")

# Windows fonts directory
fonts_dir = Path("C:/Windows/Fonts")

if fonts_dir.exists():
    print(f"✓ Found fonts directory: {fonts_dir}\n")
    
    # Get all font files
    font_files = []
    for ext in ['*.ttf', '*.ttc', '*.otf']:
        font_files.extend(fonts_dir.glob(ext))
    
    print(f"Found {len(font_files)} font files\n")
    print("=" * 60)
    
    # Show fonts that might be useful
    print("\n📝 ENGLISH FONTS (good for English subtitles):")
    print("-" * 60)
    english_fonts = [
        'arial', 'times', 'calibri', 'verdana', 'tahoma', 
        'georgia', 'comic', 'courier', 'consola'
    ]
    for font_file in sorted(font_files):
        name_lower = font_file.name.lower()
        if any(ef in name_lower for ef in english_fonts):
            print(f"  {font_file}")
    
    print("\n🇯🇵 JAPANESE FONTS (good for Japanese subtitles):")
    print("-" * 60)
    japanese_fonts = [
        'gothic', 'mincho', 'meiryo', 'msgothic', 'msmincho', 
        'yugothic', 'yumin', 'noto'
    ]
    for font_file in sorted(font_files):
        name_lower = font_file.name.lower()
        if any(jf in name_lower for jf in japanese_fonts):
            print(f"  {font_file}")
    
    print("\n🇰🇷 KOREAN FONTS (good for Korean subtitles):")
    print("-" * 60)
    korean_fonts = ['malgun', 'batang', 'dotum', 'gulim', 'nanum']
    for font_file in sorted(font_files):
        name_lower = font_file.name.lower()
        if any(kf in name_lower for kf in korean_fonts):
            print(f"  {font_file}")
    
    print("\n" + "=" * 60)
    print("\n💡 HOW TO USE THESE FONTS:")
    print("-" * 60)
    print("In your code, use the full path like this:")
    print("  font='C:/Windows/Fonts/arial.ttf'")
    print("  font='C:/Windows/Fonts/msgothic.ttc'")
    print("\nMake sure to copy the EXACT filename from above!")
    
else:
    print("✗ Could not find Windows fonts directory")
    print("Your fonts might be in a different location.")
    print("\nTry checking:")
    print("  - C:/Windows/Fonts")
    print("  - C:/Program Files/Common Files/Microsoft Shared/Fonts")

print("\n" + "=" * 60)
