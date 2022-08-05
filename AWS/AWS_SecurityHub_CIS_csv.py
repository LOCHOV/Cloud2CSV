import boto3
import csv
import AWS_config
import botocore
import botocore.exceptions
import sys
from datetime import datetime
import os
import pandas as pd

"""
This script will help gathering the CIS hardening results from the securityhub of one account. 
To run the script, use the following command with your account id:
    python3 SecurityHub_CIS_csv.py 12345678910
It is required to have a role and your machine to be able to assume-role into it.

The last part of the script enables a conversion to excel, comment it out if it is not needed
"""

# create base session with the API credentials from AWS_config, then open STS client to assume role
session = boto3.Session(
    aws_access_key_id=AWS_config.aws_key,
    aws_secret_access_key=AWS_config.aws_secret,
    region_name="eu-central-1")
sts_client = session.client('sts')


def get_securityhub(accountid):
    # list to store all of the output for the account
    globallist = []
    rolename = "rolename" # specify yours here
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
        aws_session_token=credentials['SessionToken'])
        #region_name="eu-central-1")

    # Create Client to collect data
    support_client = new_session.client('securityhub')
    filters = {
        'RecordState': [{
                'Value': 'ACTIVE',
                'Comparison': 'EQUALS'}],
         'GeneratorId': [{
                'Value': 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/',
                'Comparison': 'PREFIX'}]
            } # this will filter out only the results related to CIS

    # Run the API call and get the CIS checks back
    paginator = support_client.get_paginator('get_findings')
    response_iterator = paginator.paginate(Filters=filters) # a boto3 paginator is needed because of the large output
    for page in response_iterator:
        for check in page["Findings"]:
            print(check["RecordState"] + "   " + check["GeneratorId"])
            security_data = {}
            security_data["AccountID"] = accountid
            try:
                security_data["Status"] = check["Compliance"]["Status"]
            except KeyError:
                security_data["Status"] = "-"
            security_data["Title"] = check["Title"]
            security_data["Date"] = check["CreatedAt"]
            security_data["Description"] = check["Description"]
            try:
                security_data["Severity"] = check["FindingProviderFields"]["Severity"]["Original"]
            except KeyError:
                security_data["Severity"] = "-"
            security_data["Resource"] = check["Resources"]
            try:
                security_data["Remediation"] = check["Remediation"]["Recommendation"]["Url"]
            except KeyError:
                security_data["Remediation"] = "-"
            security_data["Types"] = check["GeneratorId"]
            security_data["RecordState"] = check["RecordState"]

            globallist.append(security_data)

    return globallist


# function to write the data to the csv file
def writetocsv(accountid, wr):
    account_counter = 0
    print("running...")

    account_counter += 1
    outputdata = get_securityhub(accountid.rstrip())
    print("Account " + accountid.rstrip() + " done " + str(account_counter))
    if outputdata:
        for line in outputdata:
            tmplist = []
            for key, value in line.items():
                tmplist.append(value)
            wr.writerow(tmplist)
    print("Finished!")


def main():
    account = sys.argv[1]
    filename = "CISAWS_" + account + ".csv"
    outputfile = open(filename, "w")
    wr = csv.writer(outputfile, quoting=csv.QUOTE_MINIMAL)
    wr.writerow(["Account","Result","Title","Date","Description","Severity","Resource","Remediation","Standard","Status"])
    writetocsv(account, wr)
    outputfile.close()

    """
    This script section will convert the CSV file to excel, in case you dont want that, just delete this section
    .
    """
    read_file = pd.read_csv(filename)
    read_file.to_excel("CISAWS_" + account + ".xlsx", index=None, header=True)
    os.remove(filename)


main()
