from io import BytesIO
from pdf2docx import Converter
import json
import boto3
import base64
from botocore.exceptions import ClientError
def handler(event, context):
    s3_client = boto3.client('s3')
    # request_body = event.get("body")
    # convert_from = request_body.get("convert_from","")
    # convert_to = request_body.get("convert_to","")
    # is_base64_encoded = event.get("isBase64Encoded", False)
    # original_filename = request_body.get("original_filename","")
    # if convert_to == "docx" and convert?_from == "pdf":
    
    body = event.get("content", False)
    file_data = base64.b64decode(body) 
    
    original_filename = "sample"
    is_converted, output_file_bytes = convert_pdf2doc(file_data,original_filename)
    s3_client.put_object(
        Body=output_file_bytes,
        Bucket='doc-storage-01',
        Key=f"processed/{original_filename}.docx"
        )
    if is_converted == True:
        file_url = get_presigned_url('doc-storage-01',f"processed/{original_filename}.docx")

        return {
            "status_code":200,
            "message":"file converted successfully",
            "file_url": file_url,
            "expiration":300
        }
    
    return {
        "status_code":500,
        "message":"Error while converting the file"
    }

def convert_pdf2doc(doc_data, original_filename):
    cv = Converter(stream=doc_data)
    output_file_data = BytesIO()
    cv.convert(output_file_data)
    output_file_data.seek(0)
    data = output_file_data.read()
    is_converted = False
    if data:
        is_converted = True
    return is_converted, data
    
    
def get_presigned_url(bucket_name, object_name, expiration=300):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print("Exception: ", e)
        return None

    # The response contains the presigned URL
    return response