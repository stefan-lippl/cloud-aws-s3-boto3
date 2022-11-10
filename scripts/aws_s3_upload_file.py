import aws_config
import os
import progressbar
from argparse import ArgumentParser


class AWSFileUploader:

    def upload(self, bucket: str, filename: str, object_key: str, msg: bool = False) -> bool:
        """ Upload files/objects to S3 bucket
        - ARGS
            - bucket: (str, required): Name of the specific S3 bucket, the file should be stored in
            - filename: (str, required): Filename incl. Pre- and Suffix locally, which should get uploaded
            - object_key: (str, required): Filename incl. Pre- and Suffix in the cloud
            - msg: (option, bool) Should the respons be showed. DEFAULT: False
        - RETURN
            - (bool) TRUE if creation is successfull, else FALSE
        """

        #connect with the AWS environment 
        s3_resource = aws_config.s3r
        
        #create progress bar
        statinfo = os.stat(filename)
        up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
        up_progress.start()

        def upload_progress(chunk):
            up_progress.update(up_progress.currval + chunk)

        try:
            #upload the file to the bucket
            if msg:
                s3_resource.Bucket(bucket).upload_file(filename, object_key, Callback=upload_progress)
                print(f'Upload of file {filename} into bucket {bucket} successfull')
            else:
                s3_resource.Bucket(bucket).upload_file(filename, object_key)

            up_progress.finish()
                
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


if __name__ == '__main__':
    parser = ArgumentParser(description='Upload file(s) to a S3 bucket')
    parser.add_argument('--bucket', help='(required, str) Name of the specific S3 bucket, the file should be stored in', type=str, required=True)
    parser.add_argument('--filename', help='(required, str) Filename incl. Pre- and Suffix locally, which should get uploaded', type=str, required=True)
    parser.add_argument('--object_key', help='(required, str) Filename incl. Pre- and Suffix in the cloud', type=str, required=True)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    filename = args.filename
    object_key = args.object_key
    msg = args.msg
    
    uploader = AWSFileUploader()
    uploader.upload(bucket=bucket,  filename=filename, object_key=object_key, msg=msg)