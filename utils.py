import urllib.request
from botocore.exceptions import ClientError
import boto3
import os


def upload_s3(local_file_path, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")

    try:
        s3.upload_file(local_file_path, bucket_name, s3_key)
    except ClientError as e:
        print(f"failed uploading to s3 {e}")
        return False
    return True


def get_safe_value_from_dict(data, key):
    if key in data:
        return data[key]
    else:
        return None


def download(url: str, filename: str, folder: str):
    filepath = f'{folder}/{filename}'
    print(f"downloading: {url}")
    filepath, headers = urllib.request.urlretrieve(url, filename=filepath)
    print("download file location: ", filepath)
    return filepath
