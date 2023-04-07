import functions_framework
import os
import tarfile
import tempfile
from google.cloud import storage

storage_client = storage.Client()

def is_tar_or_tar_gz_file(filename):
    return filename.endswith('.tar') or filename.endswith('.tar.gz')

def get_archive_subdir(filename):
    # Remove the file extension
    if filename.endswith('.tar.gz'):
        return filename[:-7]
    elif filename.endswith('.tar'):
        return filename[:-4]
    else:
        return None

@functions_framework.cloud_event
def gcs_untar(cloud_event):
    data = cloud_event.data

    bucket = data["bucket"]
    name = data["name"]

    if is_tar_or_tar_gz_file(name):
        archive_subdir = get_archive_subdir(name)
        source_bucket = storage_client.get_bucket(bucket)
        tar_blob = source_bucket.blob(name)

        # Use a new bucket to store untarred files
        destination_bucket_name = "untar"
        destination_bucket = storage_client.get_bucket(destination_bucket_name)

        # Read the tar or tar.gz file as a stream
        with tempfile.NamedTemporaryFile() as tar_file:
            tar_blob.download_to_file(tar_file)
            tar_file.seek(0)

            with tarfile.open(fileobj=tar_file, mode='r|*') as tar:
                for tar_info in tar:
                    if tar_info.isfile():
                        # Read the file as a stream and upload it directly
                        with tar.extractfile(tar_info) as file_obj:
                            destination_blob = destination_bucket.blob(f"untarred/{archive_subdir}/{tar_info.name}")
                            destination_blob.upload_from_file(file_obj)

        print(f"-Successfully untarred and uploaded files from {name} to the destination bucket.")
    else:
        print(f"{name} is not a tar or tar.gz file.")
