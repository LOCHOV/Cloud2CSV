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


def get_elbs():
    # list to store all of the output for the account
    globallist = []
    # get account id
    account = boto3.client("sts").get_caller_identity().get("Account")
    # scan each region for the assets
    regions_list = get_regions("elbv2")
    for region in regions_list:
        try:
            print("checking " + region)
            client = boto3.Session().client("elbv2", region_name=region)
            elbs = client.describe_load_balancers()
            # loop to handle the ec2 data and store it to the list
            for elb in elbs["LoadBalancers"]:
                elb_data = {}
                elb_data["DNSName"] = elb["DNSName"]
                elb_data["State"] = elb["State"]
                elb_data["Type"] = elb["Type"]
                elb_data["CreatedTime"] = str(elb["CreatedTime"])
                elb_data["Account"] = account
                # attach everything to the globallist
                globallist.append(elb_data)
        except ClientError:
            print("Failure when scanning: " + region)
    # print(globallist)
    return globallist


""" WRITE DATA TO CSV """


def writetocsv(elbinventory):
    # Prepare the CSV file
    outputfile = open("Reports/elbinventory.csv", "w")
    fieldnames = ["Account", "CreatedTime", "DNSName", "State", "Type"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if elbinventory:
        for line in elbinventory:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


def main():
    elbinventory = get_elbs()  # get the inventory
    writetocsv(elbinventory)  # write the output to CSV


if __name__ == "__main__":
    main()
