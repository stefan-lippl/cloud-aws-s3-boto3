import boto3
import aws_config as aws_config
from typing import Union
from argparse import ArgumentParser
import json


class AWSBucketPolicy():
    # https://awspolicygen.s3.amazonaws.com/policygen.html

    def __init__(self, bucket: str):
        """ Handle Bucket Policies
        - ARGS
            - bucket: (required, str) Name of the specific S3 bucket
        """
        
        #connect with the AWS environment 
        self.s3_client = aws_config.s3c
        self.bucket = bucket


    def get(self, msg: bool = False) -> Union[str, bool]:
        """ Get Bucket Policies
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (str | bool) Response as STR if creation is successfull, else FALSE
        """

        try:
            response = self.s3_client.get_bucket_policy(Bucket=self.bucket)
            if msg:
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(f'\n{response["Policy"]}\n')
                else:
                    print('\nSee Responste: \n', response)
            return response["Policy"]

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False

    def put(self, action: str, effect: str, msg: bool = False) -> bool:
        """ Create a Bucket Policy
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if creation is successfull, else FALSE
        """
        
        BUCKET_POLICY = {
            "Statement": [{
                "Principal": {
                    "AWS": "*"
                },
                "Action": [
                    f'{action}'
                ],
                "Effect": f'{effect}',
                "Resource": f'arn:aws:s3:::{self.bucket}'
                }
            ]
        }

        try:
            policy_document = json.dumps(BUCKET_POLICY)
            self.s3_client.put_bucket_policy(Bucket=self.bucket, Policy=policy_document)
            if msg: print(f'\nPolicy "{action}" has been added to bucket "{self.bucket}"\n')
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


    def delete(self, msg: bool = False) -> bool:
        """ Delete Bucket Policies
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if deletion is successfull, else FALSE
        """
        
        try:
            self.s3_client.delete_bucket_policy(Bucket=self.bucket)
            if msg: print(f'\nBucket Policies has been deleted from bucket "{self.bucket}"\n')
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False
            

if __name__ == '__main__':
    parser = ArgumentParser(description='Handle a buckets policies')
    parser.add_argument('--bucket', help='(required, str) The buckets name', type=str, required=True)
    parser.add_argument('--intend', help='(required, str) get, put or delete', type=str, required=True)
    parser.add_argument('--action', help='(optional, str) Name of the Policy Rule', type=str, required=False)
    parser.add_argument('--effect', help='(optional, str) E.g. Allow or Deny', type=str, required=False)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    intend = args.intend
    msg = args.msg

    policy = AWSBucketPolicy(bucket=bucket)

    if intend == 'get':
        policy.get(msg=msg)

    elif intend == 'put':
        action = args.action
        effect = args.effect
        policy.put(action=action, effect=effect, msg=msg)

    elif intend == 'delete':
        policy.delete(msg=msg)

    else:
        print('Wrong intend selected. Choose between: get, put, delete or type -h for help')