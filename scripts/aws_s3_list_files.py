import aws_config
from argparse import ArgumentParser


class AWSFilesLister():

    def list_files(self, bucket: str, msg: bool = False) -> list:
        """ List all files in an AWS S3 bucket, per list view as following:\n
        ['sub-folder1', 'sub-folder2', 'sub-folder3', ... , 'filename.filetype']
        - ARGS
            - bucket: (required, str) Name of the specific S3 bucket, the files are stored
            - msg: (optional, bool) Print the result in the CLI
        - RETURN
            - (list) A LIST with all keys
        """

        #connect with the AWS environment 
        s3_resource = aws_config.s3r
                            
        try:
            bucket = s3_resource.Bucket(bucket)

            list_keys = []

            #requrest and save the object keys
            for obj in bucket.objects.all():
                list_keys.append(obj.key.split('/'))

            if msg: print(f'\n{list_keys}\n')

            return list_keys

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return []


if __name__ == '__main__':
    parser = ArgumentParser(description='List all files in an AWS S3 bucket incl. prefix (sub-folder)')
    parser.add_argument('--bucket', help='(required, str) Bucket name of the AWS S3 bucket', type=str, required=True)
    parser.add_argument('--msg', help='(option, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    msg = args.msg

    filelister = AWSFilesLister()
    filelister.list_files(bucket=bucket, msg=msg)