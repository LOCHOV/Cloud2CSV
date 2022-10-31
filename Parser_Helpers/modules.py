""" Define the options and the help message for the argparser """
options_aws = [
    "a1 - AWS_EC2_Instances",
    "a2 - AWS_EC2_Public_IPs",
    "a3 - AWS_EC2_ELB",
    "a4 - AWS_Lambda_Functions",
    "a5 - AWS_S3_Buckets",
    "a6 - AWS_SecurityHub_CIS_Findings",
    "a7 - AWS_SecurityHub_All_Findings",
    "a8 - AWS_VPC_Subnets"]

options_azure = [
    "m1 - Azure_Read_Exposed_Blob_Anonymously",
    "m2 - Azure_VM_instances",
    "m3 - Azure_SecurityAlerts"
]

options_gcp = [
    "g1 - GCP_VM_Instances"
]