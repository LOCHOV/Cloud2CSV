import boto3
import csv
import botocore
import botocore.exceptions
from datetime import datetime

""" 
This script helps collecting the Security Hub Cloud hardening results from various AWS Account at once.
It is required to have a role with access to the AWS Security Hub in each of the accounts that is meant to be checked.
Assume-Role should be possible from the server you are running this script from.
"""

# create a base session with the security credentials provided by AWS_config, then opens the STS client to assume role
# the awsconfig script can be found on my Github also
session = boto3.Session(
    aws_access_key_id=AWS_config.aws_key,
    aws_secret_access_key=AWS_config.aws_secret,
    region_name="eu-central-1",
)
sts_client = session.client("sts")


# Runs the API call to the securityhub endpoint to gather the data for the account
def get_securityhub(accountid):
    rolename = "rolename"  # replace with your roles name
    globallist = []  # list to store all of the output for the account
    rolearn = "arn:aws:iam::" + accountid + ":role/" + rolename
    try:
        assumed_role = sts_client.assume_role(
            RoleArn=rolearn, RoleSessionName="session1"
        )
    except ClientError:
        print("Failed to assume role in " + accountid)
        return None
    credentials = assumed_role[
        "Credentials"
    ]  # get temporary credentials & session token for the assumed role
    # pass assumed role credentials to a new session
    new_session = boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )
    # region_name="eu-central-1")

    # Create Client to collect data
    support_client = new_session.client("securityhub")
    try:
        paginator = support_client.get_paginator(
            "get_findings"
        )  # runs the API Call to get all the findings
        response_iterator = paginator.paginate()
        for page in response_iterator:
            for check in page["Findings"]:
                security_data = {}  # saves each finding into a dictionary
                security_data["AccountID"] = accountid
                security_data["Status"] = check["Compliance"]["Status"]
                security_data["Title"] = check["Title"]
                security_data["Date"] = check["CreatedAt"]
                security_data["Description"] = check["Description"]
                security_data["Severity"] = check["FindingProviderFields"]["Severity"][
                    "Original"
                ]
                security_data["Resource"] = check["Resources"]
                security_data["Remediation"] = check["Remediation"]["Recommendation"][
                    "Url"
                ]
                security_data["Types"] = check["Types"]
                globallist.append(
                    security_data
                )  # appends each finding to the list of findings

    except:
        security_data = {}
        security_data["AccountID"] = accountid
        security_data["Status"] = "Not subscribed to SecurityHub"
        globallist.append(security_data)  # stores everything into one list
    return globallist


# write the data to the csv file
def writetocsv(accountsfile, wr):
    account_counter = 0
    print("running...")

    for accountid in accountsfile:
        account_counter += 1
        outputdata = get_securityhub(accountid.rstrip())  # Starts the API call function
        print("Account " + accountid.rstrip() + " done " + str(account_counter))
        if outputdata:
            for line in outputdata:
                tmplist = []
                for key, value in line.items():
                    tmplist.append(value)
                wr.writerow(tmplist)
    print("Finished!")


def main():
    accountsfile = open(
        "Reports/accountlist.txt", "r"
    )  # specify your accounts list here
    outputfile = open("SecurityHubResults.csv", "w")  # specify your output file here
    wr = csv.writer(outputfile, quoting=csv.QUOTE_MINIMAL)
    wr.writerow(
        [
            "Account",
            "Result",
            "Title",
            "Date",
            "Description",
            "Severity",
            "Resource",
            "Remediation",
            "Standard",
        ]
    )
    writetocsv(accountsfile, wr)
    accountsfile.close()
    outputfile.close()


if __name__ == "__main__":
    main()
