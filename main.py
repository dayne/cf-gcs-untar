import functions_framework
import os
import tarfile
import tempfile
from google.cloud import storage

storage_client = storage.Client()

def is_tar_or_tar_gz_file(filename):
    return filename.endswith('.tar') or filename.endswith('.tar.gz')

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def gcs_untar(cloud_event):
    data = cloud_event.data

    bucket = data["bucket"]
    name = data["name"]

    # Check if file is a tar or tar.gz file
    if is_tar_or_tar_gz_file(name):
        source_bucket = storage_client.get_bucket(bucket)
        tar_blob = source_bucket.blob(name)

        # Download the tar or tar.gz file to a temporary file
        with tempfile.NamedTemporaryFile() as tar_file:
            tar_blob.download_to_file(tar_file)
            tar_file.seek(0)

            # Extract the tar or tar.gz file contents
            with tarfile.open(fileobj=tar_file) as tar:
                for tar_info in tar:
                    if tar_info.isfile():
                        file_data = tar.extractfile(tar_info).read()

                        # Upload the extracted file to the same bucket
                        destination_blob = source_bucket.blob(f"untarred/{tar_info.name}")
                        destination_blob.upload_from_string(file_data)

        print(f"-Successfully untarred and uploaded files from {name} to the same bucket.")
    else:
        print(f"{name} is not a tar or tar.gz file.")