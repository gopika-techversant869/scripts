import sys
import cv2
import os
import boto3
import logging
import numpy as np
from abc import ABC, abstractmethod
from io import BytesIO



s3 = boto3.client("s3")

class IImageResizer(ABC):
    """
    This as the Abstract Interface for Image resizing
    """

    @abstractmethod
    def load_image(self, image_path):
        pass

    @abstractmethod
    def resize_image(self, img):
        pass

    @abstractmethod
    def save_images(self, resized_images, image_path):
        pass

class OpenCVImageResizer(IImageResizer):
    """
    This as the concrete implementation of abstract interface mentioned above
    """

    def __init__(self, sizes=None):
        self.sizes = sizes or {
            "large": (1024, 1024),
            "medium": (512, 512),
            "thumbnail": (128, 128),
        }

    def load_image(self, bucket_name,image_name):
        # img = cv2.imread(image_path)
        # if img is None:
        #     raise ValueError("Failed to load image. Please check the file path.")
        # return img
        response = s3.get_object(Bucket=bucket_name, Key=image_name)
        image_data = response["Body"].read()
        image_array = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Failed to load image from S3.")

        return img


    def resize_image(self, img):
        # return {name: cv2.resize(img, size, interpolation=cv2.INTER_CUBIC) for name, size in self.sizes.items()}
        for name,size in self.sizes.items():
            image_dict = {name:cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)}
            return image_dict


    def save_images(self, resized_images, bucket_name,image_name):
        # filename = os.path.splitext(image_name)
        # for size_name, img in resized_images.items():
        #     output_path = f"{filename}_{size_name}.jpg"
        #     new_key = f"{filename}_{size_name}.jpg"
        #     buffer_bytes = BytesIO(buffer)
        #     s3.put_object(Bucket=bucket_name, Key=new_key, Body=buffer_bytes.getvalue(), ContentType="image/jpeg")

        #     print(f"Image saved to S3: s3://{bucket_name}/{new_key}")
        #     cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, 90])
        #     print(f"Image saved: {output_path}")
        filename, ext = os.path.splitext(image_name) 
        logging.info("file_name extracted :",filename)
        for size_name, img in resized_images.items():
            status, buffer = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
            logging.info("status and buffer:",status,buffer)
            buffer_bytes = BytesIO(buffer)
            new_key = f"{filename}_{size_name}.jpg"
            s3.put_object(Bucket=bucket_name, Key=new_key, Body=buffer_bytes.getvalue(), ContentType="image/jpeg")

            print(f"Image saved to S3: s3://{bucket_name}/{new_key}")


class ImageProcessor:
    """
    This is the high level class which is strictly follows the IImageResizer interface.
    """
    def __init__(self, resizer: IImageResizer):  
        self.resizer = resizer

    def process(self, bucket_name,image_name):
        try:
            # img = self.resizer.load_image(image_path)
            # resized_images = self.resizer.resize_image(img)
            # self.resizer.save_images(resized_images, image_path)
            img = self.resizer.load_image(bucket_name, image_name)
            resized_images = self.resizer.resize_image(img)
            self.resizer.save_images(resized_images, bucket_name, image_name)
            return {"message": "Images processed and saved to S3"}
        except Exception as e:
            print(f" Error: {e}")



