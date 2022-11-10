import aws_config
from argparse import ArgumentParser


class AWSDeleteBucket:

    def delete(self, bucket: str, msg: bool = False) -> bool:
        """ Delete a specific S3 bucket
        - ARGS
            - bucket: (str, required): Name of the specific S3 bucket, which should be deleted
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        -RETURN:
            - (bool) TRUE if deletion was successfull, else FALSE
        """

        #connect with the AWS environment 
        s3_resource = aws_config.s3r
        
        try:
            #connect with a specific S3 bucket
            bucket = s3_resource.Bucket(bucket)
            #delete all files (also all versions of the files) in the bucket
            bucket.object_versions.delete()
            #delete the bucket itself
            bucket.delete()

            if msg: print(f'Bucket {bucket} successfull deleted')

            return True

        except Exception as e:
            #if there is an error, show the error
            if msg: print('Deletion unsuccessfull, see error below \n', e)
            return False


if __name__ == '__main__':
    parser = ArgumentParser(description='Delete a specific S3 bucket')
    parser.add_argument('--bucket', help='(required, str) Bucket name of the AWS S3 bucket', type=str, required=True)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    msg = args.msg

    deleter = AWSDeleteBucket()
    deleter.delete(bucket=bucket, msg=msg)
