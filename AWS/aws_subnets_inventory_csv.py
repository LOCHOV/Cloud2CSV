import boto3
from pprint import pprint as pp
import csv
from botocore.exceptions import ClientError
from boto3.session import Session


""" GENERATE A LIST OF ALL AVAILABLE REGIONS"""
def get_regions(service):
    # define regions to scan
    regions_session = Session()
    regions_list = regions_session.get_available_regions(service)
    return regions_list


""" COLLECT EC2 SUBNETS INVENTORY """
def get_subnets():
    # list to store all of the output for the account
    globallist = []
    # get account id
    account = boto3.client('sts').get_caller_identity().get('Account')
    # scan each region for the assets
    regions_list = get_regions('ec2')
    for region in regions_list:
        try:
            print("checking " + region)
            ec2_client = boto3.Session().client('ec2', region_name=region)
            all_subnets = ec2_client.describe_subnets()
            # loop to handle the subnet data and store it to the dict
            for subnet in all_subnets["Subnets"]:
                subnetdata = {}
                subnetdata["SubnetCIDR"] = subnet["CidrBlock"]
                subnetdata["AccountID"] = subnet["OwnerId"]
                subnetdata["ARN"] =  subnet['SubnetArn']
                subnetdata["Region"] = region
                globallist.append(subnetdata)
                print(subnetdata)
        except ClientError:
            print("Failure when scanning: " + region)
    return globallist


""" WRITE DATA TO CSV """
def writetocsv(subnetinventory):
    # Prepare the CSV file
    outputfile = open("subnetinventory.csv", "w")
    fieldnames = ["SubnetCIDR", "AccountID", "ARN", "Region"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if subnetinventory:
        for line in subnetinventory:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


def main():
    subnetinventory = get_subnets() # get the inventory
    writetocsv(subnetinventory) # write the output to CSV

main()

