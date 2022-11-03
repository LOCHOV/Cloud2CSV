from azure.mgmt.resource import SubscriptionClient
from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
import subprocess
import json
import csv


def encryption_at_host(credential, sub_client):
    # Specifies output file for the overview by subscription
    output_file_subs = open("Reports/EncAtHost_overview_Subs.csv", "w")
    writer_subs = csv.writer(output_file_subs)
    writer_subs.writerow(["Subscription", "EncryptionAtHost-Status"])
    # Specifies output file for the overview by vm
    output_file_vms = open("Reports/EncAtHost_overview_VMs.csv", "w")
    writer_vms = csv.writer(output_file_vms)
    writer_vms.writerow(["Subscription", "VM Name", "EncAtHost-Status"])

    cmd = "az feature show --name EncryptionAtHost --namespace Microsoft.Compute"
    for sub in sub_client.subscriptions.list():
        sub_id = sub.subscription_id.strip()
        subprocess.run('az account set --subscription ' + sub_id, shell=True)
        output = json.loads(subprocess.check_output(cmd, shell=True).decode('utf-8'))
        data = [sub_id, output["properties"]["state"]]
        writer_subs.writerow(data)
        compute_client = ComputeManagementClient(credential, sub_id)
        vm_list = compute_client.virtual_machines.list_all()
        for vm in vm_list:
            if vm.security_profile:
                vmdata = [sub_id, vm.name, str(vm.security_profile.encryption_at_host)]
            else:
                vmdata = [sub_id, vm.name, "False"]
            writer_vms.writerow(vmdata)
        print(sub_id)
def azure_disk_encryption(credential,sub_client):
    output_file = open("Reports/ADE_overview_VMs.csv", "w")
    writer = csv.writer(output_file)
    writer.writerow(["Subscription", "VM Name", "ADE-Status"])
    counter = 0
    for sub in sub_client.subscriptions.list():
        sub_id = sub.subscription_id.strip() # define subscription ID
        subprocess.run('az account set --subscription ' + sub_id, shell=True)
        compute_client = ComputeManagementClient(credential, sub_id)
        vm_list = compute_client.virtual_machines.list_all()
        for vm in vm_list:
            cmd = "az vm encryption show --ids " + vm.id
            output = subprocess.run(cmd, shell=True, capture_output=True)
            if output.stdout:
                data = [sub_id, vm.name, output.stdout.decode('utf-8').strip()]
            elif output.stderr:
                data = [sub_id, vm.name, output.stderr.decode('utf-8').strip()]
            writer.writerow(data)
        counter += 1
        print(str(counter) + "   " + sub_id)


def main():
    credential = AzureCliCredential()
    sub_client = SubscriptionClient(credential)
    print("Checking each Subscription for the 'Encryption at Host' feature")
    encryption_at_host(credential,sub_client)
    print("Checking each VM in each Subscription for the 'Azure Disk Encryption' feature")
    azure_disk_encryption(credential,sub_client)

if __name__ == "__main__":
    main()