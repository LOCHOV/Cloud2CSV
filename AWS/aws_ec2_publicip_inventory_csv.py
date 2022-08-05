import boto3
import csv
import AWS_config
from botocore.exceptions import ClientError

""" 
This script helps collecting the ec2 instance public IPs from various AWS Account at once.
It is required to have a role with read-access to EC2 in each of the accounts that is meant to be checked.
Assume-Role should be possible from the server you are running this script from.
"""

# create a base session with the security credentials provided by awsconfig, then opens the STS client to assume role
# the awsconfig script can be found on my Github also
session = boto3.Session(
    aws_access_key_id=AWS_config.aws_key,
    aws_secret_access_key=AWS_config.aws_secret,
    region_name="eu-central-1")
sts_client = session.client('sts')


# Runs the API call to the ec2 endpoint to gather the data from the account
def get_data(accountid):
    # list to store all of the output for the account
    rolename = "rolename" # replace with your roles name
    globallist = []  # list to store all of the output for the account
    rolearn = "arn:aws:iam::" + accountid + ":role/" + rolename
    try:
        assumed_role = sts_client.assume_role(RoleArn=rolearn, RoleSessionName="session1")
    except ClientError:
        print("Failed to assume role in " + accountid)
        return None
    credentials = assumed_role['Credentials'] # get temporary credentials & session token for the assumed role
    # pass assumed role credentials to a new session
    new_session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name="eu-central-1")

    # Create Client to collect data

    client = new_session.client('ec2')
    addresses_dict = client.describe_addresses() # runs the API Call to get all the findings

    for eip_dict in addresses_dict['Addresses']:
        eip_data = {}
        eip_data["IP"] = eip_dict['PublicIp'].strip()
        eip_data["Account"] = accountid.strip()
        # attach everything to the globallist
        globallist.append(eip_data)  # appends each finding to the list of findings
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
    accountsfile = open("accountlist.txt", "r") # specify your accounts list here
    outputfile = open("publicIPs.csv", "w") # specify your output file here
    wr = csv.writer(outputfile, quoting=csv.QUOTE_MINIMAL)
    wr.writerow(["PublicIP", "AccountId"])
    writetocsv(accountsfile, wr)
    accountsfile.close()
    outputfile.close()


main()
