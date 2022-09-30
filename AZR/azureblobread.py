from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobServiceClient
import sys
import argparse


""" download file from the publicly facing blob """
def download_blob(url):
    print("Blob URL = " + url)
    client = BlobClient.from_blob_url(blob_url=url)
    blob_data = client.download_blob()
    # write it to a local file with the same name as the remote file
    filename = url.rsplit('/', 1)
    file = open(filename[1], "wb")
    blob_data.readinto(file)


""" enumerate the blob storages and files in the azure container """
def list_container(url):
    print("Container URL = " + url)
    container = ContainerClient.from_container_url(container_url=url)
    blob_list = []
    for blob in container.list_blobs():
        blob_list.append(blob)
    for item in blob_list:
        print(url + "/" + item["name"]+"\n")


def main():
    # argument parser
    type = input("Are you testing access to a blob (b/B) or a container (c/C)? ")
    url = input("Please specify the URL endpoint for the asset: ")

    if type == "c" or type == "C":
        list_container(url)
    elif type == "b" or type == "B":
        download_blob(url)
    else:
        print("Input for URL or container/blob was wrong. Please retry")


if __name__ == "__main__":
    main()