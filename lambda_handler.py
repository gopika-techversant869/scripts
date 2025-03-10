








def lambda_handler(event, context):
    """ AWS Lambda Entry Point """
    bucket_name = event["bucket"]
    image_key = event["key"]

    resizer = OpenCVImageResizer()
    processor = ImageProcessor(resizer)
    
    result = processor.process(bucket_name, image_key)
    return result