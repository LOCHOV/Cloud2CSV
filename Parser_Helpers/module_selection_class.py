from Parser_Helpers.title import title


class user_selection:
    def __init__(self, script, message):
        self.script = script
        self.message = message

    def aws_selected(self):
        # if the user just wrote "a", dont display script banner
        if self.script != "a":
            title(self.script, "aws")
        # run chosen script
        if self.script == "a1":
            import AWS.aws_ec2_inventory_csv

            AWS.aws_ec2_inventory_csv.main()
        elif self.script == "a2":
            import AWS.aws_ec2_publicip_inventory_csv

            AWS.aws_ec2_publicip_inventory_csv.main()
        elif self.script == "a3":
            import AWS.aws_elb_inventory_csv

            AWS.aws_elb_inventory_csv.main()
        elif self.script == "a4":
            import AWS.aws_lambda_inventory_csv

            AWS.aws_lambda_inventory_csv.main()
        elif self.script == "a5":
            import AWS.aws_s3_inventory_csv

            AWS.aws_s3_inventory_csv.main()
        elif self.script == "a6":
            import AWS.aws_securityhub_cis_csv

            AWS.aws_securityhub_cis_csv.main()
        elif self.script == "a7":
            import AWS.aws_securityhubcollector_csv

            AWS.aws_securityhubcollector_csv.main()
        elif self.script == "a8":
            import AWS.aws_subnets_inventory_csv

            AWS.aws_subnets_inventory_csv.main()
        elif self.script == "a9":
            import AWS.aws_s3_list_files_csv

            AWS.aws_s3_list_files_csv.main()
        else:
            print(self.message)

    def azure_selected(self):
        if self.script != "m":
            title(self.script, "azure")
        if self.script == "m1":
            import AZR.azure_vm_inventory_csv

            AZR.azure_vm_inventory_csv.main()
        elif self.script == "m2":
            import AZR.azure_container_check

            AZR.azure_container_check.main()
        elif self.script == "m3":
            import AZR.azure_securityalerts_csv

            AZR.azure_securityalerts_csv.main()
        elif self.script == "m4":
            import AZR.azure_vm_encryption_csv

            AZR.azure_vm_encryption_csv.main()
        else:
            print(self.message)

    def gcp_selected(self):
        if self.script != "g":
            title(self.script, "gcp")
        if self.script == "g1":
            import GCP.gcp_vm_inventory_csv

            GCP.gcp_vm_inventory_csv.main()
        else:
            print(self.message)
