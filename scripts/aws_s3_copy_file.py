import aws_config
from argparse import ArgumentParser


class AWSCopyFile:

    def copy(self, bucket_from: str, bucket_to: str, object_key_from: str, object_key_to: str, msg: bool = False) -> bool:
        """ Copy an object from one bucket to another, or in the same bucket
        - ARGS
            - bucket_from: (required, str) Name of the specific S3 bucket, the file should be copied from
            - bucket_to: (required, str) Name of the specific S3 bucket, the copy should be stored
            - object_key_from: (required, str) Filename incl. Pre- and Suffix in the cloud, which should be copied
            - object_key_to: (required, str) Filename incl. Pre- and Suffix in the cloud, which is the copy
        - RETURN
            - (bool) TRUE if copy process is successfull, else FALSE
        """
        
        #connect with the AWS environment 
        s3_resource = aws_config.s3r

        copy_source = {'Bucket': f'{bucket_from}',
                       'Key': object_key_from}
        bucket = s3_resource.Bucket(bucket_to)

        try:
            #copy the file from one bucket into the other (or the same)
            bucket.copy(copy_source, object_key_to)
            if msg: print(f'Successfull copied {object_key_from} from {bucket_from} into {bucket_to} as {object_key_to}')
            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False


if __name__ == '__main__':
    parser = ArgumentParser(description='Copy an object from one bucket to another, or in the same bucket')
    parser.add_argument('--bucket_from', help='(required, str) TBD', type=str, required=True)
    parser.add_argument('--bucket_to', help='(required, str) TBD', type=str, required=True)
    parser.add_argument('--object_key_from', help='(required, str) TBD', type=str, required=True)
    parser.add_argument('--object_key_to', help='(required, str) TBD', type=str, required=True)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket_from = args.bucket_from
    bucket_to = args.bucket_to
    object_key_from = args.object_key_from
    object_key_to = args.object_key_to
    msg = args.msg

    awscopy = AWSCopyFile()
    awscopy.copy(bucket_from=bucket_from, bucket_to=bucket_to, object_key_from=object_key_from, object_key_to=object_key_to, msg=msg)

