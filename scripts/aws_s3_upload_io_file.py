import aws_config


class AWSFileIOUploader():

    def upload(self, io_data: any, bucket: str, object_key: str, msg: bool = False) -> bool: 
        """Upload a Bytes File
        - ARGS
            - io_data: (requried, Object) Bytes-Object which should get uploaded
            - bucket: (required, str) Name of the specific S3 bucket, the file should be stored in
            - object_key: (required, str) Filename incl. Pre- and Suffix in the cloud
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - True if upload is successfull, else False
        """  

        #connect with the AWS environment 
        s3_client = aws_config.s3c
       
        try:
            s3_client.upload_fileobj(io_data, bucket, object_key)
            if msg: print(f'Upload of IO File to bucket {bucket} with the key {object_key} successfull')
            
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print('FAILED\n', e)
            return False