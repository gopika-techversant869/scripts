import sys
sys.path.append("./PIL")  # Ensure Lambda can find Pillow
import boto3
from abc import ABC, abstractmethod
from io import BytesIO
from PIL import Image

import logging
logging.basicConfig(level=logging.INFO)


s3 = boto3.client("s3")

class IImageResizer(ABC):
    """Abstract Interface for Image resizing"""

    @abstractmethod
    def load_image(self, bucket_name, image_name):
        pass

    @abstractmethod
    def resize_image(self, img):
        pass

    @abstractmethod
    def save_images(self, resized_images, bucket_name, image_name):
        pass

class PillowImageResizer(IImageResizer):
    """Concrete implementation of image resizer using Pillow"""

    def __init__(self, sizes=None):
        self.sizes = sizes or {
            "large": (1024, 1024),
            "medium": (512, 512),
            "thumbnail": (128, 128),
        }
    
    def load_image(self, bucket_name, image_name):
        """Load image from S3 into a PIL Image object"""
        response = s3.get_object(Bucket=bucket_name, Key=image_name)
        image_data = response["Body"].read()
        img = Image.open(BytesIO(image_data)).convert("RGB")  # Convert to RGB

        if img is None:
            raise ValueError("Failed to load image from S3.")

        return img


    def resize_image(self, img):
        """Resize the image using Pillow"""
        resized_images = {}
        for name, size in self.sizes.items():
            resized_images[name] = img.resize(size, Image.LANCZOS)  
        return resized_images

    def save_images(self, resized_images, bucket_name, image_name):
        """Save resized images to S3"""
        filename, ext = image_name.rsplit(".", 1)  
        logging.info(f"Extracted filename: {filename}")

        for size_name, img in resized_images.items():
            buffer_bytes = BytesIO()
            img.save(buffer_bytes, format="JPEG", quality=90)  
            buffer_bytes.seek(0)

            new_key = f"{filename}_{size_name}.jpg"
            s3.put_object(Bucket=bucket_name, Key=new_key, Body=buffer_bytes, ContentType="image/jpeg")

            print(f"Image saved to S3: s3://{bucket_name}/{new_key}")

class ImageProcessor:
    """High-level class following IImageResizer interface"""

    def __init__(self, resizer: IImageResizer):  
        self.resizer = resizer

    def process(self, bucket_name, image_name):
        """Process image: Load, resize, and save to S3"""
        try:
            img = self.resizer.load_image(bucket_name, image_name)
            resized_images = self.resizer.resize_image(img)
            self.resizer.save_images(resized_images, bucket_name, image_name)
            return {"message": "Images processed and saved to S3"}
        except Exception as e:
            logging.error(f"Error: {e}")
            return {"error": str(e)}




def lambda_handler(event, context):
    """ AWS Lambda Entry Point """
    logging.info(f"Received event: {event}")

    bucket_name = event.get("bucket")
    image_key = event.get("key")

    if not bucket_name or not image_key:
        logging.error("Missing 'bucket' or 'key' in request")
        return {"error": "Missing 'bucket' or 'key' in request"}

    logging.info(f"Processing image: s3://{bucket_name}/{image_key}")

    resizer = PillowImageResizer()
    processor = ImageProcessor(resizer)

    result = processor.process(bucket_name, image_key)
    logging.info(f"Processing result: {result}")
    
    return result
