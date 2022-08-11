import argparse
from argparse import RawTextHelpFormatter


class user_selection:
    def __init__(self, script, message):
        self.script = script
        self.message = message

    def aws_selected(self):
        print("You selected: " + self.script)
        if self.script == "AWS_EC2_Instances":
            import AWS.aws_ec2_inventory_csv
            AWS.aws_ec2_inventory_csv.main()
        elif self.script == "AWS_EC2_Public_IPs":
            import AWS.aws_ec2_publicip_inventory_csv
            AWS.aws_ec2_publicip_inventory_csv.main()
        elif self.script == "AWS_EC2_ELB":
            import AWS.aws_elb_inventory_csv
            AWS.aws_elb_inventory_csv.main()
        elif self.script == "AWS_Lambda_Functions":
            import AWS.aws_lambda_inventory_csv
            AWS.aws_lambda_inventory_csv.main()
        elif self.script == "AWS_S3_Buckets":
            import AWS.aws_s3_inventory_csv
            AWS.aws_s3_inventory_csv.main()
        elif self.script == "AWS_SecurityHub_CIS_Findings":
            import AWS.AWS_SecurityHub_CIS_csv
            AWS.AWS_SecurityHub_CIS_csv.main()
        elif self.script == "AWS_SecurityHub_All_Findings":
            import AWS.AWS_SecurityHubCollector_csv
            AWS.AWS_SecurityHubCollector_csv.main()
        elif self.script == "AWS_VPC_Subnets":
            import AWS.aws_subnets_inventory_csv
            AWS.aws_subnets_inventory_csv.main()
        else:
            print("Module was not found. Maybe it is misspelled or I just didnt have time to develop it yet :)")
            print(self.message)

    def azure_selected(self):
        print("You selected: " + self.script)
        if self.script == "Azure_Microsoft_Defender_CIS_Findings":
            import AZR.Azure_CIS_single_sub
            AZR.Azure_CIS_single_sub.main()
        elif self.script == "Azure_VM_instances":
            import AZR.azure_vm_inventory_csv
            AZR.azure_vm_inventory_csv.main()
        elif self.script == "Azure_Read_Exposed_Blob_Anonymously":
            import AZR.azureblobread
            AZR.azureblobread.main()
        else:
            print("Module was not found. Maybe it is misspelled or I just didn't have time to develop it yet :)")
            print(self.message)

    def gcp_selected(self):
        print("You selected: " + self.script)
        if self.script == "GCP_Security_Command_Center_CIS_Findings":
            import GCP.GCP_CIS_scc_singleproject_csv
            GCP.GCP_CIS_scc_singleproject_csv.main()
        elif self.script == "GCP_VM_Instances":
            import GCP.gcp_vm_inventory_csv
            GCP.gcp_vm_inventory_csv.main()
        else:
            print()
            print(self.message)


def main():
    """ Define the options and the help message for the argparser"""
    options_aws = ["AWS_EC2_Instances", "AWS_EC2_Public_IPs", "AWS_EC2_ELB", "AWS_Lambda_Functions", "AWS_S3_Buckets",
                   "AWS_SecurityHub_CIS_Findings", "AWS_SecurityHub_All_Findings", "AWS_VPC_Subnets"]
    options_azure = ["Azure_Read_Exposed_Blob_Anonymously", "Azure_VM_instances",
                     "Azure_Microsoft_Defender_CIS_Findings"]
    options_gcp = ["GCP_Security_Command_Center_CIS_Findings", "GCP_VM_Instances"]

    """ The message is splitted in two parts as a list in order to be able to chose one"""
    message = ['Allowed values are:\n\n------ AWS ------\n' + '\n'.join(options_aws) \
               + "\n\n------ Azure ------\n" + '\n'.join(options_azure) \
               + "\n\n------ GCP ------\n" + '\n'.join(options_gcp),
               "\nModule was not found. Maybe it is misspelled or I just didn't have time to develop it yet :)"]

    """ Argument Parser """
    parser = argparse.ArgumentParser(description='List the content of a folder', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s', '--script', dest="arg_value", metavar='', type=str, help=message[0])
    args = parser.parse_args()
    user = user_selection(args.arg_value, message)  # Add the value to the user class

    """ Run Script based on the provided value """
    if "AWS_" in args.arg_value:
        user.aws_selected()
    elif "Azure_" in args.arg_value:
        user.azure_selected()
    elif "GCP_" in args.arg_value:
        user.gcp_selected()
    else:
        print(message[1] + message[0])


main()
