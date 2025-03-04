import sys
from PIL import Image

# Define size presets
SIZES = {
    "large": (1024, 1024),
    "medium": (512, 512),
    "thumbnail": (128, 128),
}

def resize_image(image_path):
    """Resizes an image into multiple sizes and saves them."""
    
    try:
        # Open the image
        img = Image.open(image_path)

        # Convert to RGB (important for saving as JPEG)
        img = img.convert("RGB")

        # Get filename without extension
        filename = image_path.rsplit(".", 1)[0]

        for size_name, size in SIZES.items():
            # Resize using high-quality downscaling
            resized_img = img.resize(size, Image.LANCZOS)
            
            # Save image with optimized compression
            output_path = f"{filename}_{size_name}.jpg"
            resized_img.save(output_path, "JPEG", quality=90, optimize=True)

            print(f"✔ Image saved: {output_path}")

    except Exception as e:
        print(f" Error: {e}")

# Command-line execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(" Usage: python script.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]  # Get image path from command-line argument
    resize_image(image_path)




