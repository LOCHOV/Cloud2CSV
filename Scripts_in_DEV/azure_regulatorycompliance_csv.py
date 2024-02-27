from azure.identity import AzureCliCredential
from azure.mgmt.security import SecurityCenter
from azure.mgmt.resource import SubscriptionClient
from azure.core.exceptions import HttpResponseError
import csv
from pprint import pprint
import datetime


""" CREATE THE SECURITYCENTER CLIENT"""
def create_security_client(subscription, credential):
    # any location will work here. To check the locations run "az account list-locations -o table"
    asc_location = "northeurope"
    # API clients needed to collect data
    client = SecurityCenter(credential, subscription, asc_location)
    return client


""" AUTHENTICATION """
def auth():
    # Acquire a credential object from the CLI-based authentication.
    credential = AzureCliCredential()
    # API clients needed to collect data
    sub_client = SubscriptionClient(credential)
    return credential, sub_client


""" WRITE DATA TO CSV """
def writetocsv(data):
    # Prepare the CSV file
    outputfile = open("Reports/AzureSecurityCenterRecommendations.csv", "w", newline='')
    fieldnames = ["Subscription", "Name", "Description", "status",
                  "severity", "type", "id", "AffectedAsset","URL", "Time"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if data:
        for line in data:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


""" GETS THE SECURITY ALERTS FROM THE SECURITY CENTER"""
def security_alerts(auth_data):
    """
    Relevant docs:
    https://docs.microsoft.com/en-us/python/api/azure-mgmt-security/azure.mgmt.security.securitycenter?view=azure-python
    https://azuresdkdocs.blob.core.windows.net/$web/python/azure-mgmt-security/1.0.0/azure.mgmt.security.models.html#azure.mgmt.security.models.Alert
    """

    credential = auth_data[0]
    sub_client = auth_data[1]  # define the subscription client to be able to go through subscriptions

    globallist = []  # list to store the content of the alerts
    for sub in sub_client.subscriptions.list():
        sub_id = sub.subscription_id
        sub_name = sub.display_name
        # define the security client with the subscription data and credential
        security_client = create_security_client(sub_id, credential)
        # get the alerts via the security center client

        print("\nRunning on " + sub_name + "\n")
        counter = 0
        try:
            request = security_client.regulatory_compliance_standards.list()
            for item in request:
                print(item.name)
                counter += 1
        except HttpResponseError as e:
            print(e)

        print(str(counter) + " compliance standards where found on subscription " + sub_name)
        #break
    return globallist


def main():
    auth_data = auth()
    alerts = security_alerts(auth_data)
    #writetocsv(alerts)


if __name__ == "__main__":
    main()
