import argparse


class user_selection:
    def __init__(self, script):
        self.script = script

    def aws_selected(self):
        print("You selected: " + self.script)

        if self.script == "AWS EC2 Instances":
            import AWS.aws_ec2_inventory_csv
            AWS.aws_ec2_inventory_csv.main()
        elif self.script == "AWS EC2 Public IPs":
            import AWS.aws_ec2_publicip_inventory_csv
            AWS.aws_ec2_publicip_inventory_csv.main()
        elif self.script == "AWS EC2 ELB":
            import AWS.aws_elb_inventory_csv
            AWS.aws_elb_inventory_csv.main()
        elif self.script == "AWS Lambda Functions":
            import AWS.aws_lambda_inventory_csv
            AWS.aws_lambda_inventory_csv.main()
        elif self.script == "AWS S3 Buckets":
            import AWS.aws_s3_inventory_csv
            AWS.aws_s3_inventory_csv.main()
        elif self.script == "AWS SecurityHub CIS Findings":
            import AWS.AWS_SecurityHub_CIS_csv
            AWS.AWS_SecurityHub_CIS_csv.main()
        elif self.script == "AWS SecurityHub All Findings":
            import AWS.AWS_SecurityHubCollector_csv
            AWS.AWS_SecurityHubCollector_csv.main()
        elif self.script == "AWS VPC Subnets":
            import AWS.aws_subnets_inventory_csv
            AWS.aws_subnets_inventory_csv.main()
        else:
            print("Module was not found. Maybe it is mispelled or I just didnt have time to develop it yet :)")

    def azure_selected(self):
        print("You selected: " + self.script)

        if self.script == "Azure Microsoft Defender CIS Findings":
            import AZR.Azure_CIS_single_sub
            AZR.Azure_CIS_single_sub.main()
        elif self.script == "Azure VM instances":
            import AZR.azure_vm_inventory_csv
            AZR.azure_vm_inventory_csv.main()
        elif self.script == "Azure Read Exposed Blob Anonymously":
            import AZR.azureblobread
            AZR.azureblobread.main()
        else:
            print("Module was not found. Maybe it is misspelled or I just didn't have time to develop it yet :)")

    def gcp_selected(self):
        print("You selected: " + self.script)
        if self.script == "Google Security Command Center CIS Findings":
            import GCP.GCP_CIS_scc_singleproject_csv
            GCP.GCP_CIS_scc_singleproject_csv.main()
        elif self.script == "GCP VM Instances":
            import GCP.gcp_vm_inventory_csv
            GCP.gcp_vm_inventory_csv.main()
        else:
            print("Module was not found. Maybe it is misspelled or I just didn't have time to develop it yet :)")


def main():

    user = user_selection("GCP VM Instances")
    user.gcp_selected()


main()


