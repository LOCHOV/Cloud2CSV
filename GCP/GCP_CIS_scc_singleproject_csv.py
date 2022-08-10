import json
import csv
import pprint
import os
import sys
import time

"""
This script will help gathering the CIS hardening results from the Security Command Center of GCP for one account. 
The CIS checks can be found among the findings of GCP Security Health Analytics and need to be filtered out.
https://cloud.google.com/security-command-center/docs/how-to-use-security-health-analytics

It is required to have your machine configured with an active login to "gcloud" and a user/service account able to read the 
Security Command Center of your organization. You will need to change the commands below according to your GCP environment.

To run the script use:
    python3 GCP_CIS_scc_singleproject_csv.py your-project-id-here
"""


# get source id of Security Health Analytics findins with gcloud scc sources describe organizations/1123456789 --source-display-name='Security Health Analytics'
def get_data(id):
    os.popen(r'gcloud scc findings list projects/' + id + r' --source=123456789 --filter="state=\"ACTIVE\"" --format json  > cis_temp.json')
    print("--- Getting the Security Health Analytics findings for " + id + " ---")
    time.sleep(20) # gives some time for the command to finish
    print("--- cis_temp.json generated ---")


# function to write the data to the csv file
def writetocsv(data,id):
    cis_csv_report_name = "GCP_CIS_" + id + "_report.csv"
    cis_csv_report_file = open(cis_csv_report_name,"w")
    wr = csv.writer(cis_csv_report_file, quoting=csv.QUOTE_MINIMAL)
    wr.writerow(["Project-ID", "CIS-Check", "Severity", "ID", "Asset_Name", "Asset_Type", "Description", "Remediation","Status"])
    for item in data:
        tmplist = []
        for key, value in item.items():
            tmplist.append(value)
        wr.writerow(tmplist)
    print("Finished!")


def process_data(tmp_file,id):
    globallist = []
    file = open(tmp_file)
    json_data = json.load(file)
    total_counter = 0
    cis_counter = 0
    for finding in json_data:
        total_counter += 1
        try:
            if "cis" in finding['finding']["sourceProperties"]['compliance_standards']:
                findings_data = {}
                findings_data['ProjectID'] = id
                findings_data['Name'] = finding['finding']['category']
                findings_data['Severity'] = finding['finding']['severity']
                findings_data['CIS_Check_ID'] = "cis_" + finding['finding']["sourceProperties"]['compliance_standards']['cis'][0]["ids"][0]
                findings_data["AffectedAsset"] = finding['resource']['displayName']
                findings_data["Asset_Type"] = finding['resource']['type']
                findings_data["Description"] = finding["finding"]["sourceProperties"]["Explanation"]
                findings_data["Remediation"] = finding["finding"]["sourceProperties"]["Recommendation"]
                findings_data["State"] = finding["finding"]["state"]
                cis_counter += 1
                globallist.append(findings_data)
            else:
                pass
        except KeyError: # should trigger when a non-CIS check is detected
            pass

    print(str(cis_counter) + " CIS checks to fix")

    writetocsv(globallist, id)
    return globallist


def main():
    project_id = sys.argv[1]
    filename = "cis_temp.json"
    get_data(project_id)
    process_data(filename,project_id)
    os.remove(filename)
    time.sleep(5)
    print("--- cis_temp.json deleted ---")


if __name__ == "__main__":
    main()
