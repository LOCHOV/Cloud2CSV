from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobClient
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
        print(item["name"])


def main():
    # argument parser
    parser = argparse.ArgumentParser(description='Anonymous Access test to Container and Blob Storages')
    parser.add_argument("-c", dest='container_url', help="specify container URL to list the blobs in the container", type=str, action="store")
    parser.add_argument("-b", dest='blob_url', help="specify blob URL to download the blob file", type=str, action="store")
    args = parser.parse_args()
    if args.blob_url:
        download_blob(args.blob_url)
    if args.container_url:
        list_container(args.container_url)


main()