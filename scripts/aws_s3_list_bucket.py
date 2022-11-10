import aws_config
from argparse import ArgumentParser


class AWSBucketsLister():

    def list_buckets(self, msg: bool = False) -> list:
        """ List all buckets in your AWS environment 
        - ARGS
            - msg: (option, bool) Should the respons be showed. DEFAULT: False
        - RETURN
            - (list) LIST with bucket names or empty LIST
        """
        
        #connect with the AWS environment 
        s3_resource = aws_config.s3r
                            
        try:
            #get all buckets as response
            response = s3_resource.buckets.all()

            l_buckets = []

            #iterate through the list of buckets
            for bucket in response:
                l_buckets.append(bucket.name)
                if msg: print(bucket.name)

            return l_buckets

        except Exception as e:
            #if there is an error, show the error
            if msg: print(e)
            return []


if __name__ == '__main__':
    parser = ArgumentParser(description='List all buckets in your AWS environment ')
    parser.add_argument('--msg', help='(option, bool) Should the respons be showed. DEFAULT: TRUE', default=True, type=bool, required=False)

    args = parser.parse_args()
    msg = args.msg

    lister = AWSBucketsLister()
    lister.list_buckets(msg=msg)