from azure.identity import AzureCliCredential
from azure.mgmt.security import SecurityCenter
import csv
from pprint import pprint
import datetime

""" AUTHENTICATION """
def auth(subscription):
    # Acquire a credential object from the CLI-based authentication.
    credential = AzureCliCredential()
    # any location will work here. To check the locations run "az account list-locations -o table"
    asc_location = "northeurope"
    # API clients needed to collect data
    client = SecurityCenter(credential, subscription, asc_location)
    return client, credential


""" WRITE DATA TO CSV """
def writetocsv(data):
    # Prepare the CSV file
    outputfile = open("Reports/AzureSecurityCenterAlerts.csv", "w", newline='')
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
def security_alerts(auth_data, subscription):
    """
    Relevant docs:
    https://docs.microsoft.com/en-us/python/api/azure-mgmt-security/azure.mgmt.security.securitycenter?view=azure-python
    https://azuresdkdocs.blob.core.windows.net/$web/python/azure-mgmt-security/1.0.0/azure.mgmt.security.models.html#azure.mgmt.security.models.Alert
    """

    client = auth_data[0]
    globallist = []  # list to store the content of the alerts
    request = client.alerts.list()  # ge the alerts via the security center client
    counter = 0
    for alert in request:
        alert_data = {}
        alert_data["Subscription"] = subscription
        alert_data["Name"] = alert.alert_display_name
        alert_data["Description"] = repr(alert.description).strip()
        alert_data["status"] = alert.status
        alert_data["severity"] = alert.severity
        alert_data["type"] = alert.type
        alert_data["id"] = alert.id
        alert_data["AffectedAsset"] = alert.resource_identifiers[0].azure_resource_id
        alert_data["URL"] = alert.alert_uri
        alert_data["Time"] = alert.time_generated_utc.strftime('%d/%m/%Y')
        globallist.append(alert_data)  # add the fields to the globallist
        counter += 1

    print(str(counter) + " alerts where found")
    return globallist


def main():
    subscription = input("Subscription-ID: ")
    auth_data = auth(subscription)
    alerts = security_alerts(auth_data, subscription)
    writetocsv(alerts)


if __name__ == "__main__":
    main()
