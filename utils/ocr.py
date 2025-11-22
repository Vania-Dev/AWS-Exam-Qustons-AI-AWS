# ocr_utils.py
# This file handles Optical Character Recognition (OCR) to extract text from images
# It processes exam question images and converts them to readable text for analysis

# Import necessary libraries for image processing and OCR
import boto3  # AWS SDK for Python

# Global variable to store the Textract client instance
_textract_client = None

def init_textract_client():
    """
    Initializes the AWS Textract client.
    
    This function creates a Textract client instance that can extract text from images.
    The client is cached globally to avoid recreating it on every OCR operation.
    
    Returns:
        boto3.client: Initialized Textract client instance
    """
    global _textract_client
    # Only initialize the client if it hasn't been created yet
    if _textract_client is None:
        # Create the Textract client using default AWS credentials
        _textract_client = boto3.client('textract')
    return _textract_client



def image_to_text(path: str) -> str:
    """
    Extracts text from an image using AWS Textract.
    
    Args:
        path (str): File path to the image containing text to extract
    
    Returns:
        str: Extracted text from the image, with multiple text blocks joined by newlines
    """
    # Initialize or get the cached Textract client
    client = init_textract_client()
    
    # Read image file as bytes
    with open(path, 'rb') as image_file:
        image_bytes = image_file.read()
    
    # Call Textract to detect text
    response = client.detect_document_text(
        Document={'Bytes': image_bytes}
    )
    
    # Extract text from Textract response
    text_blocks = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text_blocks.append(block['Text'])
    
    # Join all extracted text pieces into a single string
    text = "\n".join([block.strip() for block in text_blocks if block.strip()])
    
    return text