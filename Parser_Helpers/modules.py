""" Define the options and the help message for the argparser """
options_aws = [
    "AWS_EC2_Instances",
    "AWS_EC2_Public_IPs",
    "AWS_EC2_ELB",
    "AWS_Lambda_Functions",
    "AWS_S3_Buckets",
    "AWS_SecurityHub_CIS_Findings",
    "AWS_SecurityHub_All_Findings",
    "AWS_VPC_Subnets"]

options_azure = [
    "Azure_Read_Exposed_Blob_Anonymously",
    "Azure_VM_instances",
    "Azure_SecurityAlerts"
]

options_gcp = [
    "GCP_VM_Instances"
]