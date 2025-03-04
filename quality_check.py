from PIL import Image

def check_image_properties(image_path):
    img = Image.open(image_path)
    print(f"Image: {image_path}, Size: {img.size}, Format: {img.format}")

# Example Usage
check_image_properties("/home/gopika/Documents/scripts/istockphoto-1403500817-612x612.jpg")
check_image_properties("/home/gopika/Documents/scripts/istockphoto-1403500817-612x612_large.jpg")
# check_image_properties("output_medium.jpg")
# check_image_properties("output_thumbnail.jpg")
