import boto3
import cv2
import os
import numpy as np
from io import BytesIO
from abc import ABC, abstractmethod

s3 = boto3.client("s3")

class IImageResizer(ABC):
    """ Abstract Interface for Image Resizing """

    @abstractmethod
    def load_image(self, bucket_name, image_key):
        pass

    @abstractmethod
    def resize_image(self, img):
        pass

    @abstractmethod
    def save_images(self, resized_images, bucket_name, original_key):
        pass


class OpenCVImageResizer(IImageResizer):
    """ Concrete implementation using OpenCV """

    def __init__(self, sizes=None):
        self.sizes = sizes or {
            "large": (1024, 1024),
            "medium": (512, 512),
            "thumbnail": (128, 128),
        }

    def load_image(self, bucket_name, image_key):
        """ Load image from S3 into memory """
        response = s3.get_object(Bucket=bucket_name, Key=image_key)
        image_data = response["Body"].read()
        
        # Convert image bytes to OpenCV format
        image_array = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Failed to load image from S3.")

        return img

    def resize_image(self, img):
        """ Resize image to different sizes """
        return {
            name: cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
            for name, size in self.sizes.items()
        }

    def save_images(self, resized_images, bucket_name, original_key):
        """ Upload resized images back to S3 """
        filename, ext = os.path.splitext(original_key)  # Extract filename
        
        for size_name, img in resized_images.items():
            _, buffer = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
            buffer_bytes = BytesIO(buffer)

            # Upload to S3
            new_key = f"{filename}_{size_name}.jpg"
            s3.put_object(Bucket=bucket_name, Key=new_key, Body=buffer_bytes.getvalue(), ContentType="image/jpeg")

            print(f"Image saved to S3: s3://{bucket_name}/{new_key}")


class ImageProcessor:
    """ High-level class following the IImageResizer interface """

    def __init__(self, resizer: IImageResizer):
        self.resizer = resizer

    def process(self, bucket_name, image_key):
        try:
            img = self.resizer.load_image(bucket_name, image_key)
            resized_images = self.resizer.resize_image(img)
            self.resizer.save_images(resized_images, bucket_name, image_key)
            return {"message": "Images processed and saved to S3"}
        except Exception as e:
            return {"error": str(e)}


def lambda_handler(event, context):
    """ AWS Lambda Entry Point """
    bucket_name = event["bucket"]
    image_key = event["key"]

    resizer = OpenCVImageResizer()
    processor = ImageProcessor(resizer)
    
    result = processor.process(bucket_name, image_key)
    return result
