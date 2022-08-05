import boto3
import csv
from botocore.exceptions import ClientError
from boto3.session import Session


""" GENERATE A LIST OF ALL AVAILABLE REGIONS"""
def get_regions(service):
    # define regions to scan
    regions_session = Session()
    regions_list = regions_session.get_available_regions(service)
    return regions_list


"""COLLECT EC2 PUBLIC IP INVENTORY"""
def get_IPs():
    # list to store all of the output for the account
    globallist = []

    # get account id
    account = boto3.client('sts').get_caller_identity().get('Account')

    # scan each region for the assets
    regions_list = get_regions('ec2')
    for region in regions_list:
        try:
            print("checking " + region)
            # Create Client to collect data
            client = boto3.Session().client('ec2', region_name=region)
            addresses_dict = client.describe_addresses()

            for eip_dict in addresses_dict['Addresses']:
                print(eip_dict)
                eip_data = {}
                try:
                    eip_data["InstanceId"] = eip_dict['InstanceId'].strip()
                except KeyError:
                    eip_data["InstanceId"] = "none"
                eip_data["IP"] = eip_dict['PublicIp'].strip()
                eip_data["Account"] = account.strip()
                eip_data["Region"] = region.strip()
                # attach everything to the globallist
                globallist.append(eip_data)
            #print(globallist)
        except ClientError:
            print("Failure when scanning: " + region)
    return globallist


""" WRITE DATA TO CSV """
def writetocsv(pubIpInventory):
    # Prepare the CSV file
    outputfile = open("ec2_public_ips.csv", "w")
    fieldnames = ["IP", "Account","InstanceId","Region"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if pubIpInventory:
        for line in pubIpInventory:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


def main():
    pubIpInventory = get_IPs() # get the inventory
    writetocsv(pubIpInventory) # write the output to CSV


main()