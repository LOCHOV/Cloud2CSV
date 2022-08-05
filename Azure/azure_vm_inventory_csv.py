from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
import os
import csv
from pprint import pprint as pp

""" AUTHENTICATE VIA AZURE CLI CREDENTIALS"""
def auth():
    # Acquire a credential object using CLI-based authentication.
    credential = AzureCliCredential()
    # API clients needed to collect data
    sub_client = SubscriptionClient(credential)
    return sub_client, credential

""" GET VM INVENTORY """
def get_VMs(auth_data):
    sub_client = auth_data[0]
    credential = auth_data[1]
    globallist = []
    for sub in sub_client.subscriptions.list():
        sub_id = sub.subscription_id
        sub_name = sub.display_name

        # Clients needed to gather the VM and ressource group information
        resource_client = ResourceManagementClient(credential, sub_id)
        compute_client = ComputeManagementClient(credential, sub_id)
        network_client = NetworkManagementClient(credential, sub_id)

        # first generate dictionary for pubIPs
        pub_ip_dict = {}
        pub_ips = network_client.public_ip_addresses.list_all()
        for ip in pub_ips:
            pub_ip_dict[ip.id] = ip.ip_address

        # get data from all VMs
        vm_list = compute_client.virtual_machines.list_all()
        for vm in vm_list:

            vmdata = {}
            vmdata["Name"] = vm.name
            vmdata["ID"] = vm.id
            vmdata["Sub_Name"] = sub_name
            vmdata["Sub_ID"] = sub_id
            vmdata["RSG"] = vm.id.split("/")[4]  # strip it out from the id path
            vmdata["AvZone"] = vm.location

            privateIPs = []
            publicIPs = []
            for interface in vm.network_profile.network_interfaces:
                interface_name = " ".join(interface.id.split('/')[-1:])
                subscription = "".join(interface.id.split('/')[4])
                try:
                    configs = network_client.network_interfaces.get(subscription, interface_name).ip_configurations
                    for x in configs:
                        try:
                            publicIPs.append(pub_ip_dict.get(x.public_ip_address.id))
                        except:
                            pass
                        privateIPs.append(x.private_ip_address)
                except:
                    pass

            vmdata["privIP"] = privateIPs
            vmdata["pubIP"] = publicIPs

            # get information on the OS and base image
            try:
                osVendor = vm.storage_profile.image_reference.offer
            except:
                osVendor = ""
            try:
                osVersion = vm.storage_profile.image_reference.sku
            except:
                osVersion = ""
            if osVendor == None:
                osVendor = ""
            if osVersion == None:
                osVersion = ""
            os = osVendor + " " + osVersion
            vmdata["Image"] = os

            # Append all the data to the global list
            globallist.append(vmdata)
        print(sub_name + " done")
    return globallist


""" WRITE DATA TO CSV """
def writetocsv(vminventory):
    # Prepare the CSV file
    outputfile = open("AzureVMs.csv", "w")
    fieldnames = ["Name", "ID", "Sub_Name", "Sub_ID", "RSG", "AvZone", "privIP", "pubIP", "Image"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if vminventory:
        for line in vminventory:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


def main():
    auth_data = auth()
    vm_inventory = get_VMs(auth_data)
    writetocsv(vm_inventory)


main()




