import sys
from PIL import Image

def create_favicons(source_image, output_dir):
    try:
        img = Image.open(source_image)
        # Ensure image is RGBA for transparency (though the reference has a black background)
        img = img.convert("RGBA")
        
        # Save standard PNGs
        img.resize((16, 16), Image.Resampling.LANCZOS).save(f"{output_dir}/favicon-16x16.png", "PNG")
        img.resize((32, 32), Image.Resampling.LANCZOS).save(f"{output_dir}/favicon-32x32.png", "PNG")
        img.resize((180, 180), Image.Resampling.LANCZOS).save(f"{output_dir}/apple-touch-icon.png", "PNG")
        img.resize((192, 192), Image.Resampling.LANCZOS).save(f"{output_dir}/android-chrome-192x192.png", "PNG")
        img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{output_dir}/android-chrome-512x512.png", "PNG")
        
        # Create ICO file containing multiple sizes
        icon_sizes = [(16, 16), (32, 32), (48, 48)]
        img.save(f"{output_dir}/favicon.ico", format="ICO", sizes=icon_sizes)
        print("Favicons generated successfully.")
    except Exception as e:
        print(f"Error generating favicons: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <source_image> <output_dir>")
        sys.exit(1)
    create_favicons(sys.argv[1], sys.argv[2])
