import aws_config
from argparse import ArgumentParser
from typing import Union


class AWSCreateS3Bucket:

    def create(self, bucket: str, region: str = 'eu-central-1', msg: bool = False) -> Union[str, bool]:
        """ Creates an AWS S3 bucket in a specific region
        - ARGS
            - bucket: (required, str) Name of the specific S3 bucket, which should be created. Attention: must be unique in the whole AWS environment
            - region: (optional, str) Region where the bucket should be created e.g. us-west-1, eu-west-2. Default: eu-central-1 For more information see https://docs.aws.amazon.com/general/latest/gr/s3.html
            - msg: (option, bool) Should the respons be showed. DEFAULT: FALSE
        - RETURN
            - (str | bool) Response as STR if creation is successfull, else FALSE
        """

        #connect with the AWS environment 
        s3_client = aws_config.s3c

        #specify the required region as a dictionary
        s3_region = {
            'LocationConstraint': region
        }

        try:
            #create the bucket
            response = s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration=s3_region)
            print(f'{bucket} in region {region} successfull created.')
            if msg == True: print(response)

            return response
            
        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return False
            

if __name__ == '__main__':
    parser = ArgumentParser(description='Creates an AWS S3 bucket in a specific region')
    parser.add_argument('--bucket', help='(required, str) The bucket name can only contains characters and - no _, $ etc.', type=str, required=True)
    parser.add_argument('--region', help='(optional, str) Default: eu-central-1 (Frankfurt)', default='eu-central-1', type=str, required=False)
    parser.add_argument('--msg', help='(optional, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    bucket = args.bucket
    region = args.region
    msg = args.msg

    creator = AWSCreateS3Bucket()
    creator.create(bucket=bucket, region=region, msg=msg)