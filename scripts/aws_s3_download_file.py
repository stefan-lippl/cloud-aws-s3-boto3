import boto3
import aws_config
from argparse import ArgumentParser
import sys


class AWSDownloader:

    def download(self, bucket: str, object_key: str, filename: str, msg: bool = False) -> bool: 
        """ Download all kinds of files from a given AWS S3 bucket
        - ARGS
            - bucket: (required, str) Name of the specific S3 bucket, the file is stored in
            - object_key: (required, str) Filename incl. Pre- and Suffix in the cloud, which should be downloaded
            - filename: (required, str) Filename incl. Pre- and Suffix locally, of the download
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if download is successfull, else FALSE
        """       

        #connect with the AWS environment
        s3_client = aws_config.s3c
        
        try:
            #grab metadata of the file to make calculations for progress bar
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

            #download the file with a progress bar
            if msg: 
                with open(filename, 'wb') as f:
                    # download and save the file
                    s3_client.download_file(bucket, object_key, filename, Callback=progress)
            #download the file without a progress bar
            else:
                with open(filename, 'wb') as f:
                    # download and save the file
                    s3_client.download_file(bucket, object_key, filename)

            if msg: print(f'Download of file {object_key} from bucket {bucket} successfull')

            return True

        except Exception as e: 
            #if there is an error, show the error
            if msg: print(e)
            return False

    
if __name__ == '__main__':
    parser = ArgumentParser(description='Download file(s) from a S3 bucket')
    parser.add_argument('--bucket', help='(required, str) TBD', type=str, required=True)
    parser.add_argument('--object_key', help='(required, str) TBD', type=str, required=True)
    parser.add_argument('--filename', help='(required, str) TBD', type=str, required=True)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    object_key = args.object_key
    filename = args.filename
    msg = args.msg

    downloader = AWSDownloader()
    downloader.download(bucket=bucket, object_key=object_key, filename=filename, msg=msg)