import sys
import cv2

# Define size presets
SIZES = {
    "large": (1024, 1024),
    "medium": (512, 512),
    "thumbnail": (128, 128),
}

def resize_image(image_path):
    """Resizes an image into multiple sizes and saves them using OpenCV."""
    
    try:
        # Read image using OpenCV
        img = cv2.imread(image_path)

        if img is None:
            raise ValueError("Failed to load image. Please check the file path.")

        # Get filename without extension
        filename = image_path.rsplit(".", 1)[0]

        for size_name, size in SIZES.items():
            # Resize using high-quality interpolation
            resized_img = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)

            # Save image with optimized compression
            output_path = f"{filename}_{size_name}.jpg"
            cv2.imwrite(output_path, resized_img, [cv2.IMWRITE_JPEG_QUALITY, 90])

            print(f"Image saved: {output_path}")

    except Exception as e:
        print(f"Error: {e}")

# Command-line execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(" Usage: python script.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]  # Get image path from command-line argument
    resize_image(image_path)
