import aws_config as aws_config
from typing import Union
from argparse import ArgumentParser


class AWSFileTagging():

    def __init__(self, bucket: str):
        """ Handle tags from files
        - ARGS
            - bucket: (required, str) Name of the specific S3 bucket
        """

        self.s3_client = aws_config.s3c
        self.bucket = bucket


    def get(self, object_key: str, msg: bool = False) -> Union[str, bool]:
        """ Get the files tags
        - ARGS
            - object_key: (required, str) Filename incl. Pre- and Suffix in the cloud
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (str | bool) A list as STR with the Tag Sets (Key + Value) if successfull, else FALSE
        """

        try:
            response = self.s3_client.get_object_tagging(
                Bucket=self.bucket,
                Key=object_key
            )

            if len(response["TagSet"]) > 0:
                if msg:
                    for tagset in response["TagSet"]:
                        print(f'{tagset}')
                    print()
                return response["TagSet"]
            if len(response['TagSet']) == 0:
                if msg:
                    print('\nThis file has currently no tags')
                    print('Length TagSet: ', len(response['TagSet']), '\n')
                return False

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


    def put(self, object_key: str, key: str, value: str, msg: bool = False) -> bool:
        """ Add tags to a file
        - ARGS
            - object_key: (required, str) Filename incl. Pre- and Suffix in the cloud
            - key: (required, str) Tag key
            - value: (required, str) Tag value
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if successfull else FALSE
        """

        tag = {
            'TagSet': [
                {
                    'Key': key,
                    'Value': value,
                }
            ]
        }

        existing_tags = self.s3_client.get_object_tagging(Bucket=self.bucket,
                                                          Key=object_key)

        if len(existing_tags["TagSet"]) > 0:
            for tagset in existing_tags["TagSet"]:
                tag['TagSet'].append(tagset)

        try:
            tag = self.s3_client.put_object_tagging(
                Bucket=bucket,
                Key=object_key,    
                Tagging=tag
            )
            if msg:
                if tag['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(f'\nKey "{key}" with value "{value}" successfull added to file "{object_key}" in bucket "{self.bucket}"\n')
                else:
                    print('See response\n', tag)
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


    def delete(self, object_key: str, msg: bool = False) -> bool:
        """ Delete tags from a file
        - ARGS     
            - object_key: (required, str) Filename incl. Pre- and Suffix in the cloud       
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (bool) TRUE if successfull else FALSE
        """

        try:
            response = self.s3_client.delete_object_tagging(
                Bucket=self.bucket,
                Key=object_key
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
    parser = ArgumentParser(description='Add tags to files in an AWS S3 bucket')
    parser.add_argument('--bucket', help='(required, str) The buckets names', type=str, required=True)
    parser.add_argument('--object_key', help='(required, str) Name (Path) to the', type=str, required=True) 
    parser.add_argument('--intend', help='(required, str) get, put or delete', type=str, required=True)  
    parser.add_argument('--key', help='(required, str) Key of tag', type=str, required=False)
    parser.add_argument('--value', help='(required, str) Value of tag', type=str, required=False)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)
    
    args = parser.parse_args()
    bucket = args.bucket
    object_key = args.object_key
    intend = args.intend
    key = args.key
    value = args.value
    msg = args.msg

    tagging = AWSFileTagging(bucket=bucket, object_key=object_key)

    if intend == 'get':
        tagging.get(object_key=object_key, msg=msg)

    elif intend == 'put':
        tagging.put(object_key=object_key, key=key, value=value, msg=msg)

    elif intend == 'delete':
        tagging.delete(object_key=object_key, msg=msg)

    else:
        print('Wrong intend selected. Choose between: get, put, delete or type -h for help')