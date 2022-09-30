import csv
import os
import sys
from typing import Iterable
from google.cloud import compute_v1
from googleapiclient import discovery
import google.auth

""" Login required with service principal or gcloud auth application-default login -> you need the json key """


def get_zones(project_id):
    try:
        service = discovery.build('compute', 'v1')
    except google.auth.exceptions.DefaultCredentialsError as error:
        print("Login to GCP failed. Maybe the path provided was not correct or the key is not valid.")
        print("Error message: " + str(error))
        sys.exit(1)
    request = service.zones().list(project=project_id)
    zone_list = []
    while request is not None:
        response = request.execute()
        for zone in response['items']:
            zone_list.append(zone["name"])
        request = service.zones().list_next(previous_request=request, previous_response=response)
    return zone_list


def list_instances(project_id, zones) -> Iterable[compute_v1.Instance]:
    globallist = []
    instance_client = compute_v1.InstancesClient()
    for zone in zones:
        print("Checking " + zone)
        instance_list = instance_client.list(project=project_id, zone=zone)
        for instance in instance_list:
            vm_data = {}
            # print(instance)
            vm_data["Name"] = instance.name
            vm_data["Zone"] = zone
            vm_data["Created"] = instance.creation_timestamp
            vm_data["Project"] = project_id
            vm_data["privIP"] = instance.network_interfaces[0].network_i_p
            globallist.append(vm_data)

    return globallist


""" WRITE DATA TO CSV """


def writetocsv(vm_inventory):
    # Prepare the CSV file
    outputfile = open("Reports/gcpinventory.csv", "w")
    fieldnames = ["Name", "Zone", "Created", "Project", "privIP"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if vm_inventory:
        for line in vm_inventory:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


def main():
    """ Specify required inputs """
    cred = input("Json credential file full path:")
    project = input("Project ID (number):")
    region = input("Region ID (e.g. us-east5-a) or 'all' for each one available:")
    """ Check if inputs are empty """
    if cred == "" or project == "" or region == "":
        print("The input for the credential or project-id was wrong, please retry")
    else:
        """ Run scripts with the content of the inputs """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred
        if region == "all":
            zones = get_zones(project)  # if the user selected all, list all available zones
        else:
            zones = [region]  # if user specified the region, run the script just on that one
        """ Run function to list instances and write to CSV"""
        vm_inventory = list_instances(project, zones)
        writetocsv(vm_inventory)


if __name__ == "__main__":
    main()
