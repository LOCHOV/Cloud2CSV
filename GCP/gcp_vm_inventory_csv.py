import json
import csv
import pprint as pp
import os
from typing import Iterable
from google.cloud import compute_v1
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account



""" Login required with service principal or gcloud auth application-default login -> you need the json key """

def get_zones(project_id):
    #credentials = GoogleCredentials.get_application_default()
    #credentials = service_account.Credentials.from_service_account_file('cred.json')
    service = discovery.build('compute', 'v1')#, credentials=credentials)
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
        instance_list = instance_client.list(project=project_id,zone=zone)
        for instance in instance_list:
            vm_data = {}
            #print(instance)
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
    outputfile = open("gcpinventory.csv", "w")
    fieldnames = ["Name", "Zone", "Created", "Project","privIP"]
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
    cred = input("Json credential file full path:")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred
    project = input("Project ID (number):")
    zones = get_zones(project)
    vm_inventory = list_instances(project,zones)
    writetocsv(vm_inventory)

if __name__ == "__main__":
    main()