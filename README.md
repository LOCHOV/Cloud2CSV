# Public Cloud API Scripts 
## This project is still work in progress and some functions might not be fully functioning yet...

Here you can find several public cloud API scripts for **AWS**, **GCP** and **Azure** cloud. These scripts are mainly oriented to listing cloud resources into CSV/XLSX files in order to gain quick insights into your assets.

### CLI Requirements:

  - **AWS**: 
      - read-only access to AWS via a IAM-Role (assume-role) or IAM-User. Login to aws cli
      - https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/
  
  - **GCP**: 
      - user or service account with read permissions to the service you want to scan. Login to gcloud cli.
      - https://cloud.google.com/security-command-center/docs/how-to-programmatic-access
  
  - **Azure**: 
      - a user with its API keys or a Service Principal with "Reader" role. Login to az cli.
      - https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli

### Required Packages:
You can install the required python packages automatically via:
```pip3 install -r requirements.txt```