from aws_s3_create_bucket import AWSCreateS3Bucket
from aws_s3_copy_file import AWSCopyFile
from aws_s3_upload_file import AWSFileUploader
from aws_s3_delete_file import AWSDeleteFile
from aws_s3_delete_bucket import AWSDeleteBucket
from aws_s3_download_io_file import AWSFileIODownloader
from aws_s3_upload_io_file import AWSFileIOUploader
from aws_s3_download_file import AWSDownloader

import pandas as pd
import io

def create_bucket():
    creator = AWSCreateS3Bucket()
    creator.create('bucket-test-slippl')
create_bucket()

def upload_file():
    uploader = AWSFileUploader()
    for i in range(0, 1010):
        uploader.upload('object-bucket-slippl', '../data/test.txt', f'test_{i}.txt')
#upload_file()

def download_file():
    dwl = AWSDownloader()
    dwl.download('slippl2', 'dataframe.csv', 'daf.csv')
    df = pd.read_csv('daf.csv')
    print('DATAFRAME: \n', df)
#download_file()

def copy_file():
    co = AWSCopyFile()
    co.copy('slippl', 'slippl2', 'txt/file.txt', 'test.txt')
#copy_file()

def delete_file():
    deleter = AWSDeleteFile()
    deleter.delete('slippl2', 'test3.txt')
#delete_file()

def delete_bucket():
    deler = AWSDeleteBucket()
    deler.delete('slippl2')
#delete_bucket()

def download_io_file():
    dow = AWSFileIODownloader()
    data = dow.download('slippl2', 'data.csv')
    print(data)
    df = pd.read_csv(io.BytesIO(data))
    return df
#df = download_io_file()
#print(df)

def upload_io_file(df):
    # pip install openpyxl
    towrite = io.BytesIO()
    df.to_excel(towrite)  # write to BytesIO buffer
    towrite.seek(0) 

    uow = AWSFileIOUploader()
    uow.upload(towrite, 'slippl2', 'dataframe.csv')
#upload_io_file(df)

