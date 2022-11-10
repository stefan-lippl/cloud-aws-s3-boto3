import aws_config as aws_config
from typing import Union
from argparse import ArgumentParser


class AWSPresignedURL():

    def create(self, bucket: str, object_key: str, time: int, msg: bool = False) -> Union[str, bool]:
        """ Create a public, time restricted link to a AWS file in a bucket
        - ARGS
            - bucket: (required, str) Name of the specific S3 bucket
            - object_key: (str, required): Filename incl. Pre- and Suffix in the cloud
            - time: (required, int) Time in seconds
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (str | bool) A STR with the public URL if successfull else FALSE
        """
        
        #connect with the AWS environment 
        s3_client = aws_config.s3c

        try:
            url = s3_client.generate_presigned_url(ClientMethod='get_object',
                    Params={'Bucket': bucket, 'Key': object_key},
                    ExpiresIn=time)  #seconds
                    
            if msg: print('\nURL creation successfull:\n{url}\n')

            return url
            
        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


if __name__ == '__main__':
    parser = ArgumentParser(description='Creates a public link to a file in the S3 bucket')
    parser.add_argument('--bucket', help='(required, str) The buckets name', type=str, required=True)
    parser.add_argument('--object_key', help='(required, str) The files name', type=str, required=True)
    parser.add_argument('--time', help='(required, str) Time in seconds', type=int, required=True)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    object_key = args.object_key
    time = args.time
    msg = args.msg

    url = AWSPresignedURL()
    url.create(bucket=bucket, object_key=object_key, time=time, msg=msg)
    