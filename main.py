# main.py
import json
import boto3
import os
import tempfile
from aws_question_agent import graph


def download_from_s3(bucket_name: str, object_key: str) -> str:
    """Download image from S3 and return local file path"""
    s3_client = boto3.client('s3')
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_path = temp_file.name
    temp_file.close()
    
    # Download from S3
    s3_client.download_file(bucket_name, object_key, temp_path)
    return temp_path


def lambda_handler(event, context):
    """AWS Lambda handler for S3 trigger events"""
    try:
        # Parse S3 event
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            
            print(f"Processing image: {object_key} from bucket: {bucket_name}")
            
            # Download image from S3
            local_image_path = download_from_s3(bucket_name, object_key)
            
            try:
                # Process the image using the agent
                input_state = {"file_path": local_image_path}
                graph.invoke(input_state)
            finally:
                # Clean up temporary file
                if os.path.exists(local_image_path):
                    os.unlink(local_image_path)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully processed images')
        }
    
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }