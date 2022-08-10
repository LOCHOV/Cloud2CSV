import boto3
import csv
from botocore.exceptions import ClientError

# test
""" COLLECT S3 BUCKET INVENTORY """
def get_buckets():
    # list to store all of the output for the account
    globallist = []

    # get account id
    account = boto3.client('sts').get_caller_identity().get('Account')

    # Create Client to collect data
    s3_client = boto3.Session().client('s3')
    try:
        print("Collecting S3 Buckets...")
        buckets = s3_client.list_buckets()
        # loop to handle the data and store it to the list
        for bucket in buckets["Buckets"]:
            print(bucket)
            bucket_data = {}
            bucket_data["Name"] = bucket["Name"]
            bucket_data["CreationDate"] = str(bucket["CreationDate"])
            bucket_data["Location"] = s3_client.get_bucket_location(Bucket=bucket["Name"].strip())["LocationConstraint"]
            bucket_data["AccountID"] = account
            # attach everything to the globallist
            globallist.append(bucket_data)
    except ClientError:
        pass
    print(globallist)
    return globallist


""" WRITE DATA TO CSV """
def writetocsv(s3inventory):
    
    # Prepare the CSV file
    outputfile = open("s3buckets.csv", "w")
    fieldnames = ["Name", "CreationDate", "Location", "AccountID"]
    wr = csv.DictWriter(outputfile, fieldnames=fieldnames)
    wr.writeheader()
    # Write the data in
    print("Writing to CSV...")
    if s3inventory:
        for line in s3inventory:
            wr.writerow(line)
        print("Finished!")
    outputfile.close()


def main():
    s3inventory = get_buckets() # get the s3 buckets
    writetocsv(s3inventory) # write the output to CSV


if __name__ == "__main__":
    main()