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
            print(self.message)

    def azure_selected(self):
        print("You selected: " + self.script)
        if self.script == "Azure_VM_instances":
            import AZR.azure_vm_inventory_csv
            AZR.azure_vm_inventory_csv.main()
        elif self.script == "Azure_Read_Exposed_Blob_Anonymously":
            import AZR.azureblobread
            AZR.azureblobread.main()
        elif self.script == "Azure_SecurityAlerts":
            import AZR.azure_securityalerts_csv
            AZR.azure_securityalerts_csv.main()
        else:
            print(self.message)

    def gcp_selected(self):
        print("You selected: " + self.script)
        if self.script == "GCP_VM_Instances":
            import GCP.gcp_vm_inventory_csv
            GCP.gcp_vm_inventory_csv.main()
        else:
            print(self.message)