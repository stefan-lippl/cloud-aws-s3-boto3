import boto3
import sys
sys.path.append('../')

REGION_NAME = 'YOUR-REGION'
ACCESS_KEY_ID = 'YOUR-ACCESS-KEY-ID'
SECRET_ACCESS_KEY = 'YOUR-SECRET-ACCESS-KEY'

s3c = boto3.client(
    's3',
    region_name=REGION_NAME, 
    aws_access_key_id=ACCESS_KEY_ID, 
    aws_secret_access_key=SECRET_ACCESS_KEY
)

s3r = boto3.resource(
    's3',
    region_name=REGION_NAME, 
    aws_access_key_id=ACCESS_KEY_ID, 
    aws_secret_access_key=SECRET_ACCESS_KEY
)