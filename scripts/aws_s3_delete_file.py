import aws_config
from typing import Union
from argparse import ArgumentParser


class AWSDeleteFile:

    def delete(self, bucket: str, object_key: str, msg: bool = False) -> Union[str, bool]:
        """ Delete a specific file inside a bucket
        - ARGS
            - bucket: (required, str): Name of the specific S3 bucket, the file is stored in
            - object_key: (required, str): Filename incl. Pre- and Suffix in the cloud, which should be deleted
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (str | bool) The response as STR if deletion is successfull, else FALSE
        """

        #connect with the AWS environment 
        s3_resource = aws_config.s3r

        try:
            #delete the file
            response = s3_resource.delete_object(
                Bucket=bucket,
                Key=object_key,
            )
            if msg: print(f'File {object_key} on {bucket} successfully deleted')

            return response

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False
            

if __name__ == '__main__':
    parser = ArgumentParser(description='Delete a specific file inside a bucket')
    parser.add_argument('--bucket', help='(required, str) Bucket name of the AWS S3 bucket', type=str, required=True)
    parser.add_argument('--object_key', help='(required, str) Filename incl. Pre- and Suffix in the cloud', type=str, required=True)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    object_key = args.object_key
    msg = args.msg

    deleter = AWSDeleteFile()
    deleter.delete(bucket=bucket, object_key=object_key, msg=msg)