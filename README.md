# Cloud2CSV
## This project is still work in progress and some functions might not be fully functioning yet...

Here you can find several public cloud API scripts for **AWS**, **GCP** and **Azure** cloud. These scripts are mainly oriented to listing cloud resources into CSV/XLSX files in order to gain quick insights into your assets.

### CLI Requirements:

  - **AWS**: 
      - read-only access to AWS via a IAM-Role (assume-role) or IAM-User. Login to aws cli
      - https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/
  
  - **GCP**: 
      - JSON key to either a service account or a private IAM user
      - To get the JSON key of your private IAM user run ``gcloud auth application-default login``
      - https://cloud.google.com/security-command-center/docs/how-to-programmatic-access
  
  - **Azure**: 
      - a user with its API keys or a Service Principal with "Reader" role. Login to az cli.
      - https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli

### Required Packages:
You can install the required python packages automatically via:
```pip3 install -r requirements.txt```

### Usage
The main script can be run with ```python3 cloudscripts.py```  
Get help: ```-h``` or ```--help```  
Specify the module to run: ```-s``` or ``--script``  
Example: ```python3 cloudscripts.py -s AWS_S3_Buckets```

### Modules available ``-s or --script``:

  - **AWS**:  
    - ``AWS_EC2_Instances`` lists all EC2 instances in the logged in account  
    - ``AWS_EC2_Public_IPs`` lists all public IPs associated to EC2 instances in the logged in account  
    - ``AWS_EC2_ELB``lists all Elastic Load Balancers in the logged in account   
    - ``AWS_Lambda_Functions`` lists all Lambda Functions in the logged in account  
    - ``AWS_S3_Buckets`` lists all S3-Buckets in the logged in account  
    - ``AWS_VPC_Subnets`` lists all Subnets in the logged in account  

  - **Azure**: 
    - ``Azure_Read_Exposed_Blob_Anonymously`` Tests anonymous access to an exposed Blob or Container via it´s URL.
    - ``Azure_VM_instances`` lists all VM instances in **all**  subscriptions available. To check which are available, run ``az account list``

  - **GCP**: 
    - ``GCP_VM_Instances`` lists all VM instances in **one** project. To check whichare available, run ``gcloud projects list``

