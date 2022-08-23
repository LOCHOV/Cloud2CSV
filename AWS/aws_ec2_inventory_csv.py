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


""" GET THE INVENTORY OF THE VMs """
def get_ec2_info():
    # list to store all of the output for the account
    globallist = []
    # get account id
    account = boto3.client('sts').get_caller_identity().get('Account')
    # scan each region for the assets
    regions_list = get_regions('ec2')
    for region in regions_list:
        try:
            print("checking " + region)

            # Create EC2 client and call ec2_describe_instances to get all the data for the EC2s in that account
            ec2_client = boto3.Session().client('ec2', region_name=region)
            ec2_describe_response = ec2_client.describe_instances()
            # loop to handle the ec2 data and store it to the list
            for reservation in ec2_describe_response["Reservations"]:
                # save the output (dict) to "instance" for better handling

                for instance in reservation["Instances"]:
                    instanceinfo = {}

                    # Check the state to only go through running or stopped VMs
                    state = instance["State"]
                    if state["Name"] == "running" or state["Name"] == "stopped":
                        # create list to store the output and append all required fields

                        # tags requires a try-except because it might be that no tags are set
                        try:
                            addplaceholder = True
                            tags = instance["Tags"]
                            #print(instance[u"PublicIpAddress"])
                            for item in tags:
                                if item['Key'] == 'Name':
                                    addplaceholder = False
                                    instance_name = item['Value']
                                    if instance_name == "" or len(instance_name) == 0:
                                        instanceinfo["AWS Name"] = "-"
                                    else:
                                        instanceinfo["AWS Name"] = instance_name

                            if addplaceholder == True:
                                instanceinfo["AWS Name"] = "-"

                        except KeyError:
                            instanceinfo["AWS Name"] = "-"

                        instanceinfo["InstanceID"] = instance["InstanceId"]
                        instanceinfo["IP Address"] = instance["PrivateIpAddress"]
                        instanceinfo["State"] = instance["State"].get("Name")
                        placement = instance["Placement"]
                        instanceinfo["Availability Zone"] = placement["AvailabilityZone"]
                        instanceinfo["AccountID"] = account
                        instanceinfo["AWS Private FQDN"] = instance["PrivateDnsName"]

                        # add all the information for this ec2 to the globallist
                        globallist.append(instanceinfo)
                        print(instanceinfo)
        except ClientError:
            print("Failure when scanning: " + region)
    # print(globallist)
    return globallist


""" WRITE DATA TO CSV """
def writetocsv(ec2inventory):
    # Prepare the CSV file
    outputfile = open("Reports/ec2inventory.csv", "w")
    fieldnames = ["AWS Name", "InstanceID", "IP Address", "State", "Availability Zone", "AccountID", "AWS Private FQDN"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if ec2inventory:
        for line in ec2inventory:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


def main():
    ec2inventory = get_ec2_info() # get the inventory
    writetocsv(ec2inventory) # write the output to CSV


if __name__ == "__main__":
    main()

