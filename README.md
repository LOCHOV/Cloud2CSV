# Public Cloud API Scripts - WORK IN PROGRESS

Here you can find several public cloud API and CLI scripts for **AWS**, **GCP** and **Azure** cloud. Hope it might help you get some ideas :)

You will find scripts to dump configuration data from your cloud environments and generate CSV/XLSX reports. You can export the following data with help of them.  

## Technical requirements:

  - **AWS**: 
      - read-only access to AWS via a IAM-Role (assume-role) or IAM-User
      - Be logged in on your aws cli
      - https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/
  
  - **GCP**: 
      - user or service account with read permissions to the service you want to scan
      - Be logged in on your gcloud cli
      - https://cloud.google.com/security-command-center/docs/how-to-programmatic-access
  
  - **Azure**: 
      - a user with its API keys or a Service Principal with "Reader" role
      - Be logged in on your az cli
      - https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli
