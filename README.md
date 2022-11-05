# Cloud2CSV
#### Collection of cloud API scripts to collect data from your cloud environments to CSV files

Here you can find several public cloud API scripts for **AWS**, **Azure** and **GCP**. These scripts are mainly oriented to listing cloud resources into CSV/XLSX files in order to gain quick insights into your assets.

### CLI Requirements:

  - **AWS**: 
      - read-only access to AWS via a IAM-Role (assume-role) or IAM-User. Login to aws cli
      - https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/
      
  - **Azure**: 
      - a user with its API keys or a Service Principal with "Reader" role. Login to az cli.
      - https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli
  
  - **GCP**: 
      - JSON key to either a service account or a private IAM user
      - To get the JSON key of your private IAM user run ``gcloud auth application-default login``
      - https://cloud.google.com/security-command-center/docs/how-to-programmatic-access
  

### Required Packages:
You can install the required python packages automatically via:
```pip3 install -r requirements.txt```

### Usage
The main script can be run with ```python3 cloudscripts.py```  
Get help: ```-h``` or ```--help```  
Specify the module to run: ```-m``` or ``--module`` and the module id 
Example: ```python3 cloudscripts.py -s a1```

Individual scripts can also be found on the corresponding folder (AWS, AZR, GCP)

### Modules available ``-m or --module``:

  - **Amazon Web Services**:  
    - ``a1 -> AWS EC2 Instances Enumerator`` enumerates all EC2 instances and relevant info
    - ``a2 -> AWS EC2 public IPs Enumerator`` enumerates all public IPs associated to EC2 instances  
    - ``a3 -> AWS EC2 ELB Enumerator``enumerates all Elastic Load Balancers
    - ``a4 -> AWS Lambda Functions Enumerator`` enumerates all Lambda Functions  
    - ``a5 -> AWS S3 Bucket Enumerator`` enumerates all S3-Buckets and relevant info
    - ``a6 -> AWS SecurityHub CIS Findings Listing`` lists all CIS findings from the SecurityHub Service
    - ``a7 -> AWS SecurityHub All Findings Listing`` lists all findings of any standard from the SecurityHub Service
    - ``a8 -> AWS VPC Subnets Enumerator`` enumerates all VPC subnets
    

  - **Microsoft Azure**: 
    - ``m1 -> Azure VM Instances Enumerator`` lists all VM instances in **all** subscriptions available. 
    - ``m2 -> Azure Blob/Container Storage Anonymous Access Tester`` tests anonymous access to an exposed Blob or Container via it´s URI/URL.
    - ``m3 -> Azure Security Alerts Listing`` lists all security alerts associated to **all** subscriptions available.
    - ``m4 -> Azure VM Encryption Enumerator`` checks all Subscriptions and VMs available for the ADE (Azure Disk Encryption) and EncryptionAtHost features.
    
  - **Google Cloud Platform**: 
    - ``g1 - GCP_VM_Instances`` lists all VM instances in **one** project and **one** or **all** regions. 

