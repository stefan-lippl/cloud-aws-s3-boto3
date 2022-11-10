# AWS S3 with Boto3

<br>

## Requirements

1) Create a virtual env
    ```bash
    conda create -n aws-s3-boto3 python=3.9
    ```

2) To use the AWS package, you have to install the following libraries

    ```bash
    pip install -r requirements.txt
    ```

<br>

***

<br>

## Credentials

You have to insert your credentials (`Access key ID` and `Secret access key` into the file **`aws_config.py`** inside the scripts folder, as well as the notebooks folder. With your credentials you can enable the connection to your personal AWS Account. After this step, you can start using the classes below.


**If you do not have your credentials yet**, login into your *AWS Management Console*, go to *IAM*, select your *user*, navigate to the tab *Security credentials* and hit the button *Create access key*. Then download the csv and insert your credentials into the config file as mentioned.

Go to `aws_config.py` and enter your credentials:
```
REGION_NAME =       'YOUR-REGION'
ACCESS_KEY_ID =     'YOUR-ACCESS-KEY-ID'
SECRET_ACCESS_KEY = 'YOUR-SECRET-ACCESS-KEY'
```

<br>

***

<br>

## Create S3 Bucket
Please note that the S3 bucket name must be unique in the complete AWS environment. This means that the name must also be unique outside your personal network. In addition, no special characters (except hyphen) are allowed in the name.

<br>

**API**
```python
from aws_s3_create_bucket import AWSCreateS3Bucket

creator = AWSCreateS3Bucket()

creator.create(bucket: str, 
               region: str = 'eu-central-1',
               msg: bool = False)

```

**CLI**
```bash
python aws_s3_create_bucket.py \
--bucket <bucket-name> \
--region <region-name> \
--msg <TRUE | FALSE>
```

<br>

***

<br>

## Upload File
Returns TRUE if the upload was successful, otherwise FALSE.

<br>

**API**

```python
from aws_s3_upload_file import AWSFileUploader

uploader = AWSFileUploader()

uploader.upload(bucket: str,
                filename: str,
                object_key: str,
                msg: bool = False)
```

<br>

**CLI**
```bash
python aws_s3_upload_file.py \
--bucket <bucket-name> \
--filename <local-filename-path> \
--object_key <online-filename-path> \
--msg <TRUE | FALSE>
```

<br>

***

<br>

## List S3 Buckets

<br>

**API**
```python
from aws_s3_list_buckets import AWSBucketsLister

lister = AWSBucketsLister()

lister.list_buckets(msg: bool = False)

```

**CLI**
```bash
python aws_s3_list_buckets.py \
--msg <TURE | FALSE>
```

<br>

***

<br>

## List Files (in bucket)
The fact that a bucket can consist of more than one subfolder, the function returns a list with the exact path structure of each file in the bucket: 

["**sub-folder_0**",  "**sub-folder_1**",  "**sub-folder_2**",  "**sub-folder_N**" ,  "**filename.filetype**"]

This is important if you want to download only files from a certain folder, you can filter the response and use the *AWSDownloader* class to download only these files.

<br>

**API**
```python
from aws_s3_list_files import AWSFilesLister

lister = AWSFilesLister()

lister.list_files(bucket: str,
                  msg: bool = False)
```

**CLI**
```bash
python aws_s3_list_files.py \
--bucket <bucket-name> \
--msg <True|False>
```

<br>

***

<br>


## Delete Bucket
Return TRUE if successfull, else FALSE

<br>

**API**
```python
from aws_s3_delete_bucket import AWSDeleteBucket

deleter = AWSDeleteBucket()

deleter.delete(bucket: str,
               msg: bool = False)
```

**CLI**
```bash
python aws_s3_delete_bucket.py \
--bucket <bucket-name>
--msg <TRUE | FALSE>
```

<br>

***

<br>

## Delete File
Return TRUE if successfull, else FALSE

<br>

**API**
```python
from aws_s3_delete_file import AWSDeleteFile

deleter = AWSDeleteFile()

deleter.delete(bucket: str,
               object_key: str,
               msg: bool = False)
```

**CLI**
```bash
python aws_s3_delete_file.py \
--bucket <bucket-name>
--object_key <path-to-object>
--msg <TRUE | FALSE>
```

<br>

***

<br>

## Copy File
Returns True if the action was successful, otherwise False.

<br>

**API**
```python
from aws_s3_copy_file import AWSCopyFile

copier = AWSCopyFile()

copier.copy(bucket_from: str,
            bucket_to: str,
            object_key_from: str,
            object_key_to: str,
            msg: bool = False)
```

**CLI**
```bash
python aws_s3_copy_file.py \
--bucket_from <bucket-name> \
--bucket_to <bucket-name> \
--object_key_from <object_key> \
--object_key_to <object_key> \
--msg <TRUE | FALSE>
```

<br>

***

<br>

## Download File
Returns True if the action was successful, otherwise False.

<br>

**API**
```python
from aws_s3_download_file import AWSDownloader

downloader = AWSDownloader()

downloader.download(bucket: str,
                    object_key: str,
                    filename: str,
                    msg: bool = False)
```

**CLI**
```bash
python aws_s3_download_file.py \
--bucket <bucket-name> \
--object_key <onine-filename> \
--filename <local-filename> \
--msg <TRUE | FALSE>
```


<br>

***

<br>

## Download IO File (BytesIO)
Returns BytesIO file if the download was successful, otherwise False.

<br>

**API**
```python
from aws_s3_download_io_file import AWSFileIODownloader

downloader = AWSFileIODownloader()

downloader.download(bucket: str,
                    object_key: str,
                    msg: bool = False)
```


<br>

***

<br>

## Upload IO File (BytesIO)
Returns True if the upload was successful, otherwise False.

<br>

**API**

```python
from aws_s3_upload_io_file import AWSFileIOUploader

uploader = AWSFileIOUploader()

uploader.upload(io_data: bytes,
                bucket: str,
                object_key: str,
                msg: bool = False)
```

<br>

***

<br>

## Bucket Tagging
- *Get*: return a STR of the current tags if successfull, else FALSE
- *Put*: Add tags with key and value
- *Delete*: Delete all tags

<br>

**API**
```python
from aws_s3_tag_bucket import AWSBucketTagging

tags = AWSBucketTagging(bucket: str)

#retrieve all tags
tags.get(msg: bool = False)

#add new tags
tags.put(key: str,
         value: str,
         msg: bool = False)

#delete all tags
tags.delete(msg: bool = False)
```

**CLI**
```bash
python aws_s3_tag_bucket.py \
--bucket <bucket-name> \
--intend <get | put | delete>
--key <key-of-tag>
--value <value-of-tag>
--msg <TRUE | FALSE>
```

<br>

***

<br>

## File Tagging
- *Get*: return a STR of the current tags if successfull, else FALSE
- *Put*: Add tags with key and value
- *Delete*: Delete all tags

<br>

**API**
```python
from aws_s3_tag_file import AWSFileTagging

tags = AWSFileTagging(bucket: str)

#retrieve all tags
tags.get(msg: bool = False)

#add new tags
tags.put(key: str,
         value: str,
         msg: bool = False)

#delete all tags
tags.delete(msg: bool = False)
```

**CLI**
```bash
python aws_s3_tag_file.py \
--bucket <bucket-name> \
--object_key <path-to-the-file>
--intend <get | put | delete> \
--key <key-of-tag> \
--value <value-of-tag> \
--msg <TRUE | FALSE>
```

<br>

***

<br>

## Bucket Versioning
- *Get*: return a STR of the current status if successfull, else FALSE
- *Put*: Enable the versioning
- *Delete*: Disable the versioning

<br>

**API**
```python
from aws_s3_bucket_versioning import AWSBucketVersioning

versioning = AWSBucketVersioning(bucket: str)

#get the current version status
versioning.get(msg: bool = False)

#set the versioning to enabled
versioning.put(msg: bool = False)

#disable the versioning
versioning.delete(msg: bool = False)
```

**CLI**
```bash
python aws_s3_bucket_versioning.py \
--bucket_from <bucket-name> \
--intend <get | put | delete>
--msg <TRUE | FALSE>
```

<br>

***

<br>

## Presigned Bucket/File URL
Returns the STRING with the URL if successfull, else FALSE

<br>

**API**
```python
from aws_s3_presigned_url import AWSPresignedURL

url = AWSPresignedURL()

#retrieve all tags
url.create(bucket: str,
           object_key: bool,
           time: int,
           msg: bool = False)
```

**CLI**
```bash
python aws_s3_presigned_bucket_url.py \
--bucket <bucket-name> \
--object_key <path-to-file> \
--time <seconds> \
--msg <TRUE | FALSE>
```

<br>

***

<br>

## Bucket Policy
- *Get*: return a STR of the current status if successfull, else FALSE
- *Put*: Enable the versioning
- *Delete*: Disable the versioning

<br>

**API**
```python
from aws_s3_bucket_policy import AWSBucketPolicy

policy = AWSBucketPolicy(bucket: str)

#retrieve all policies
policy.get(msg: bool = False)

#add new policies
policy.put(action: str,
           effect: dict,
           msg: bool = False)

#delete all policies
policy.delete(msg: bool = False)
```

**CLI**
```bash
python aws_s3_bucket_policy.py \
--bucket <bucket-name> \
--intend <get | put | delete> \
--action <name-of-policy> \
--effect <Allow | Deny | Other> \
--msg <TRUE | FALSE>

```

<br>
<br>
