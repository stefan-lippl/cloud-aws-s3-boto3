import aws_config as aws_config
from typing import Union
from argparse import ArgumentParser


class AWSBucketTagging():

    def __init__(self, bucket: str):
        """ Class to work with S3 bucket tags
        - ARGS
            - s3_client: (boto3.resource, required) Connected client to the AWS environment
            - bucket: (required, str) Name of the specific S3 bucket
        """

        self.s3_client = aws_config.s3c
        self.bucket = bucket


    def get(self, msg: bool = False) -> Union[list, bool]:
        """ Get the buckets tags
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (str | bool) A LIST with the Tag Sets (Key + Value) if successfull, else FALSE
        """

        try:
            response = self.s3_client.get_bucket_tagging(
                Bucket=self.bucket
            )
            if len(response["TagSet"]) > 0:
                if msg:
                    for tagset in response["TagSet"]:
                        print(f'{tagset}')
                return response["TagSet"]

            if len(response['TagSet']) == 0:
                if msg:
                    print('This bucket has currently no tags')
                    print('Length TagSet: ', len(response['TagSet']))

                return False

        except Exception as e:
            #if there is an error, show the error
            if msg:
                print(f'No tags available on bucket {self.bucket}')
                print(f'Error msg: \n', e)

            return False


    def put(self, key: str, value: str, msg: bool = False) -> bool:
        """ Add new tags to a bucket or to a set of existing tags
        - ARGS
            - key: (required, str) Tag key
            - value: (required, str) Tag value
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if successfull, else FALSE
        """

        tag = {
            'TagSet': [
                {
                    'Key': key,
                    'Value': value,
                }
            ]
        }

        try:
            existing_tags = self.s3_client.get_bucket_tagging(Bucket=self.bucket)

            if len(existing_tags["TagSet"]) > 0:
                for tagset in existing_tags["TagSet"]:
                    tag['TagSet'].append(tagset)
        
        except Exception as e:
            #if there is an error, show the error
            print(e)

        try:
            response = self.s3_client.put_bucket_tagging(
                Bucket=self.bucket,
                Tagging=tag
            )
            
            if msg:
                if response['ResponseMetadata']['HTTPStatusCode'] == 204:
                    print(f'\nKey: {key} with Value: {value} successfull added to bucket {self.bucket}\n')
                else:
                    print('See response\n', response)
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


    def delete(self, msg: bool = False) -> bool:
        """ Delete all tags from a bucket
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if successfull, else FALSE
        """

        try:
            response = self.s3_client.delete_bucket_tagging(
                Bucket=self.bucket,
            )
            if msg:
                if response['ResponseMetadata']['HTTPStatusCode'] == 204:
                    print(f'\nTags successfull removed from bucket {self.bucket}\n')
                else:
                    print('See response\n', response)

            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


if __name__ == '__main__':
    parser = ArgumentParser(description='Creates an AWS S3 bucket in a specific region')
    parser.add_argument('--bucket', help='(required, str) The buckets names', type=str, required=True)
    parser.add_argument('--intend', help='(required, str) get, put or delete', type=str, required=True)  
    parser.add_argument('--key', help='(required, str)', type=str, required=False)
    parser.add_argument('--value', help='(required, str)', type=str, required=False)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    intend = args.intend
    key = args.key
    value = args.value
    msg = args.msg

    tagging = AWSBucketTagging(bucket)

    if intend == 'get':
        tagging.get(msg=msg)

    elif intend == 'put':
        action = args.key
        effect = args.value
        tagging.put(key=key, value=value, msg=msg)

    elif intend == 'delete':
        tagging.delete(msg=msg)

    else:
        print('Wrong intend selected. Choose between: get, put, delete or type -h for help')