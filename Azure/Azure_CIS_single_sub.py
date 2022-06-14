import requests
import sys
import json
import subprocess
import time
import csv
import pandas
import os

"""
This script will help gathering the CIS hardening results from the Microsoft Defender for Cloud of your subscription. Can be also used to get the check results for policies other then CIS. 
- To run the script, use the following command with your subscription ID and credentials:
    python3 Azure_CIS_single_sub.py YourSubscriptionID YourTenantID YourClientID YourSecretKey "policy name or id"

- create the directory "/reports" if needed
- It is required to have a user with API-Keys or a Service Principal with its credentials available for use. 
- The last part of the script enables a conversion to excel, comment it out if it is not needed
"""


def get_cis_results(subscription, access_token, policy_name):
    url = "https://management.azure.com/subscriptions/" + subscription + "/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2019-10-01&%24filter=policySetDefinitionName%20eq%20'" + policy_name + "'"
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + access_token}
    response = requests.post(url=url, headers=headers)
    if response.status_code == 200:
        print("---successfully dumped cis hardening results---")
        return response.text
    else:
        print("---failure when getting the hardening results---")


def parse_results(cis_results, subscription, client_id, secret, tenant):
    json_data = json.loads(cis_results)
    # print(json_data["value"])
    global_list = []
    print("---parsing the dumped data (you could uncomment some of the print statements to see the progress)---")
    compliant_counter = 0
    noncompliant_counter = 0
    for check in json_data["value"]:
        check_data = {}
        # Get the information of the check
        policy_definition_name = check['policyDefinitionName'].strip()
        policy_definition_data = subprocess.check_output(
            "az policy definition show --name '" + policy_definition_name + "'", shell=True).decode("utf-8")
        policy_definition_data_json = json.loads(policy_definition_data)
        # add the data to the dict
        check_data["Subscription"] = subscription
        check_data["Name"] = policy_definition_data_json["displayName"]
        check_data["Status"] = check['complianceState']
        if check_data["Status"] == "Compliant":
            compliant_counter += 1
        else:
            noncompliant_counter += 1
        check_data["Description"] = policy_definition_data_json["description"]
        check_data["Category"] = policy_definition_data_json["metadata"]["category"]
        check_data["AffectedAsset"] = check['resourceId']
        # print(check_data["Status"] + " ---- " + check_data["Category"])
        check_data["Standard"] = check['policyAssignmentName']
        # time.sleep(0.3)
        global_list.append(check_data)
    print("RESULT: compliant = " + str(compliant_counter) + "  non-compliant = " + str(noncompliant_counter))
    return global_list


# function to write the data to the csv file
def writetocsv(data, cis_csv_report_name):
    print("---writing to csv---")
    cis_csv_report_file = open("reports/" + cis_csv_report_name, "w")
    wr = csv.writer(cis_csv_report_file, quoting=csv.QUOTE_MINIMAL)
    wr.writerow(["Subscription", "Name", "Status", "Description", "Category", "AffectedAsset", "Standard"])
    for item in data:
        tmplist = []
        for key, value in item.items():
            tmplist.append(value)
        wr.writerow(tmplist)
    print("Finished!")


def main():
    subscription = sys.argv[1]
    tenant = sys.argv[2]
    client_id = sys.argv[3]
    secret = sys.argv[4]
    policy_name = sys.argv[5]

    print("---API Call to get access_token from microsoft---")
    login_url = 'https://login.microsoftonline.com/' + tenant + '/oauth2/v2.0/token'
    login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    login_data = {'client_id': client_id, 'scope': 'https://management.azure.com/.default',
                  'client_secret': secret, 'grant_type': 'client_credentials'}
    login_response = requests.post(url=login_url, headers=login_headers, data=login_data)

    if login_response.status_code == 200:
        print("---Successfully received access_token for login---")
        access_token = login_response.json()['access_token']
        cis_results = get_cis_results(subscription, access_token, policy_name)
        cis_results_parsed = parse_results(cis_results, subscription, client_id, secret, tenant)
        cis_report_name = "CIS_Azure_" + subscription + ".csv"
        writetocsv(cis_results_parsed, cis_report_name)

        """csv to excel -> remove if you wish"""
        read_file = pandas.read_csv("reports/" + cis_report_name)
        read_file.to_excel("reports/CIS_Azure" + subscription + ".xlsx", index=None, header=True)
        os.remove("reports/" + cis_report_name)

    else:
        print("---Authentication error when getting the access_token---")


main()

