import boto3
import csv
import AWS_config
from botocore.exceptions import ClientError
from datetime import datetime
import pprint

""" 
This script helps to have an inventory of the S3-buckets from various AWS accounts.
It is required to have a role with read-access to S3 in each of the accounts that is meant to be checked.
Assume-Role should be possible from the server you are running this script from.
"""

# create a base session with the security credentials provided by awsconfig, then opens the STS client to assume role
# the awsconfig script can be found on my Github also
session = boto3.Session(
    aws_access_key_id=AWS_config.aws_key,
    aws_secret_access_key=AWS_config.aws_secret,
    region_name="eu-central-1")
sts_client = session.client('sts')


def get_data(accountid):
    # list to store all of the output for the account
    globallist = []
    rolename = "rolename" # replace with your roles name
    # get Credentials for the assumed role
    rolearn = "arn:aws:iam::" + accountid + ":role/" + rolename
    try:
        assumed_role = sts_client.assume_role(RoleArn=rolearn, RoleSessionName="session1")
    except ClientError:
        print("Failed to assume role in " + accountid)
        return None
    credentials = assumed_role['Credentials']
    # pass assumed role credentials to a new session
    new_session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name="eu-central-1")

    # Create S3-Client to collect data of S3 buckets
    s3_client = new_session.client('s3')
    buckets = s3_client.list_buckets()
    # loop to handle the ec2 data and store it to the list
    for bucket in buckets["Buckets"]:
        bucket_data = {}
        bucket_data["Name"] = bucket["Name"]
        bucket_data["CreationDate"] = str(bucket["CreationDate"])
        bucket_data["Location"] = s3_client.get_bucket_location(Bucket=bucket["Name"].strip())["LocationConstraint"]
        bucket_data["AccountID"] = accountid
        # attach everything to the globallist
        globallist.append(bucket_data)
    pprint(globallist)
    return globallist


# function to write the data to the csv file
def writetocsv(accountsfile, wr):
    account_counter = 0
    print("running...")

    for accountid in accountsfile:
        account_counter += 1
        outputdata = get_data(accountid.rstrip())
        print("Account " + accountid.rstrip() + " done " + str(account_counter))
        if outputdata:
            # each line contains the dictionary of the single EC2s
            for line in outputdata:
                tmplist = []
                for key, value in line.items():
                    tmplist.append(value)
                wr.writerow(tmplist)
    print("Finished!")


def main():
    accountsfile = open("accountlist.txt", "r") # specify your account list here
    outputfile = open("s3buckets.csv", "w") # specify your output file here
    wr = csv.writer(outputfile, quoting=csv.QUOTE_MINIMAL)
    wr.writerow(["S3-Bucket", "CreationDate", "Location", "AccountID"])
    writetocsv(accountsfile, wr)
    accountsfile.close()
    outputfile.close()


main()
