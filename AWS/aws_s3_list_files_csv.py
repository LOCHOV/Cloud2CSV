import boto3
from pprint import pprint as pp
from botocore.exceptions import ClientError


def main():
    bucket_name = input("Bucket-Name:\n")
    client = boto3.Session().client("s3")
    try:
        paginator = client.get_paginator("list_objects")
        page_iterator = paginator.paginate(Bucket=bucket_name)
    except ClientError as e:
        print("Could not connect to bucket. The error was:\n" + str(e))
        exit()
    for page in page_iterator:
        for file in page["Contents"]:
            pp(
                file["Key"]
                + " --- timestamp: "
                + file["LastModified"].strftime("%m/%d/%Y, %H:%M:%S")
            )


if __name__ == "__main__":
    main()
