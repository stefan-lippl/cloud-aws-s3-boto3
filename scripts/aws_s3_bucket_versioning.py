import boto3
import aws_config
from typing import Union
from argparse import ArgumentParser


class AWSBucketVersioning():
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#bucketversioning

    def __init__(self, bucket: str):
        """ Class to work with a buckets versioning
        - ARGS
            - bucket: (required, str) Name of the specific S3 bucket
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        """

        #connect with the AWS environment 
        self.s3_resource = aws_config.s3r
        self.bucket = bucket


    def get(self, msg: bool = False) -> Union[str,bool]:
        """ Get a buckets versioning status
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (str | bool) Response as STR with the currenct Versioning status, else FALSE
        """

        try:
            versioning = self.s3_resource.BucketVersioning(self.bucket)
            if msg:print(f'S3 Bucket versioning: {versioning.status}')
            return versioning.status

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


    def put(self, msg: bool = False) -> bool:
        """ Set a buckets versioning status
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if successfull, else FALSE
        """
        
        try:
            versioning = self.s3_resource.BucketVersioning(self.bucket)
            versioning.enable()
            if msg: print(f'S3 Bucket versioning: {versioning.status}')
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False
    
    def delete(self, msg: bool = False) -> bool:
        """ Delete a buckets versioning status
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if successfull else FALSE
        """
        
        try:
            versioning = self.s3_resource.BucketVersioning(self.bucket)
            versioning.suspend()
            if msg: print(f'S3 Bucket versioning: {versioning.status}')
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e) 
            return False


if __name__ == '__main__':
    parser = ArgumentParser(description='Class to work with a buckets versioning')
    parser.add_argument('--bucket', help='(required, str) The buckets name', type=str, required=True)
    parser.add_argument('--intend', help='(required, str) Choose between get, put or delete', type=str, required=True)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    intend = args.intend
    msg = args.msg

    versioning = AWSBucketVersioning(bucket)

    if intend == 'get':
        versioning.get(msg=msg)
    elif intend == 'put':
        versioning.put(msg=msg)
    elif intend == 'delete':
        versioning.delete(msg=msg)
    else:
        print('Wrong intend selected. Choose between: get, put, delete or type -h for help')

