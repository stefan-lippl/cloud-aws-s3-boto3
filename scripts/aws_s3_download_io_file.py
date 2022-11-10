import aws_config
import sys
from io import BytesIO
from typing import Union


class AWSFileIODownloader:

    def download(self, bucket: str, object_key: str, msg: bool = False) -> Union[any, bool]: 
        """ Download files from a given AWS S3 bucket into RAM
        - ARGS
            - bucket: (required, str) Name of the specific S3 bucket, the file is stored in
            - object_key: (required, str) Filename incl. Pre- and Suffix in the cloud, which should be downloaded
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (any | bool) The BYTESIO file if download is successfull, else FALSE
        """       

        #connect with the AWS environment 
        s3_client = aws_config.s3c
        #connect with the AWS environment
        s3_resource = aws_config.s3r

        try:
            meta_data = s3_client.head_object(Bucket=bucket, Key=object_key)
            total_length = int(meta_data.get('ContentLength', 0))
            downloaded = 0

            #create progress bar for CLI output
            def progress(chunk):
                nonlocal downloaded
                downloaded += chunk
                done = int(50 * downloaded / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                sys.stdout.flush()

            #create the bytesio filetype
            string_io = BytesIO()
            #download the file into a bytesio filetype with a progress bar
            if msg: s3_resource.Object(bucket, object_key).download_fileobj(string_io, progress)
            #download the file into a bytesio filetype without a progress bar
            else: s3_resource.Object(bucket, object_key).download_fileobj(string_io)
            
            if msg: print(f'File {object_key} from bucket {bucket} successfull downloaded to RAM')

            return string_io.getvalue()
            
        except Exception as e: 
            #if there is an error, show the error
            if msg: print(e)

            return False