# Public Cloud API Scripts for Security

Here you can find several public cloud API and CLI scripts for **AWS**, **GCP** and **Azure** cloud. Hope it might help you get some ideas :)

You will find scripts to dump configuration data from your cloud environments and generate CSV/XLSX reports. You can export the following data with help of them.  


  - **CIS benchmark (hardening)** results from AWS accounts, GCP projects and Azure subscriptions based on the output of the cloud native security tools
      - Information about CIS Cloud Security Benchmarks: https://www.cisecurity.org/white-papers/cis-controls-cloud-companion-guide/ 
  - **Public IPs** of AWS EC2 Instances across several accounts
  - **AWS S3 Buckets** across several accounts


## Technical requirements:

  - **AWS**: 
      - AWS Security Hub needs to be activated.
      - a read-only access to AWS via a IAM-Role or IAM-User
      - Your machine needs to be able to assume-role into your account 
          - https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/
  
  - **GCP**: 
      - The Security Command Center needs to be activated
      - a user or service account able to read from the SCC (Security Command Center)
          - https://cloud.google.com/security-command-center/docs/how-to-programmatic-access
  
  - **Azure**: 
      - The Microsoft Defender for Cloud needs to be activated
      - a user with its API keys or a Service Principal with "Reader" role or read access to Microsoft Defender for Cloud
          - https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli
      - The CIS Standards needs to be set as a policy
          - https://docs.microsoft.com/en-us/azure/defender-for-cloud/policy-reference
       
