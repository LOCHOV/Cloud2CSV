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


""" GENERATE A LIST OF ALL LAMBDAS"""


def get_functions():
    # list to store all of the output for the account
    globallist = []
    # get account id
    account = boto3.client("sts").get_caller_identity().get("Account")
    # scan each region for the assets
    regions_list = get_regions("lambda")

    for region in regions_list:
        try:
            print("checking " + region)
            # Create Client to collect data
            client = boto3.Session().client("lambda", region_name=region)
            response = client.list_functions()
            # pp(response)
            for function in response["Functions"]:
                data = {}
                data["Name"] = function["FunctionName"]
                data["ARN"] = function["FunctionArn"]
                try:
                    data["Runtime"] = function["Runtime"]
                except KeyError:
                    data["Runtime"] = ""
                data["Account"] = account
                # pp(data)
                try:
                    config = client.get_function_configuration(
                        FunctionName=function["FunctionName"]
                    )
                except KeyError:
                    pass
                globallist.append(data)
        except ClientError:
            print("Failure when scanning: " + region)

    return globallist


""" WRITE DATA TO CSV """


def writetocsv(lambdainventory):
    # Prepare the CSV file
    outputfile = open("Reports/lambdainventory.csv", "w")
    fieldnames = ["Name", "ARN", "Runtime", "Account"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if lambdainventory:
        for line in lambdainventory:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


def main():
    lambdainventory = get_functions()  # get the inventory
    writetocsv(lambdainventory)  # write the output to CSV


if __name__ == "__main__":
    main()
