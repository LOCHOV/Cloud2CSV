import boto3, json
from botocore.utils import InstanceMetadataFetcher
from botocore.credentials import InstanceMetadataProvider

"""
This script will help getting your credentials from the AWS Secrets-Manager.
You need to configure your machine to be able to reach the Secrets Manager via a role and the Instance Metadata credentials.

In case you dont need/have the AWS Secrets Manager to store your security credentials, 
replace aws_key and aws_secret with your security credentials like this:

aws_key = your AWS Key
aws_secret = your AWS Secret Key

"""

# Grab credentials from instance metadata to be able to access the secrets manager store
provider = InstanceMetadataProvider(iam_role_fetcher=InstanceMetadataFetcher(timeout=1000, num_attempts=2))
creds = provider.load()

# Get the secrets from the secrets manager
region_name = "some-region" # replace with your region
secret_name = "arn:aws:secretsmanager:region:accountid:secret:secretname"  # replace with your secret ARN

session = boto3.session.Session(
    aws_access_key_id=creds.access_key,
    aws_secret_access_key=creds.secret_key,
    aws_session_token=creds.token)  # creates the base session

client = session.client(service_name='secretsmanager',region_name=region_name) # prepares the connection to the Secrets Manager

secret = json.loads(client.get_secret_value(SecretId=secret_name)["SecretString"]) # Runs the API call and stores the json response

aws_key = secret["Keyid"]
aws_secret = secret["Secret"]
