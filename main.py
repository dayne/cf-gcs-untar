import functions_framework
import os
import tarfile
import tempfile
from google.cloud import storage

storage_client = storage.Client()

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data

    bucket = data["bucket"]
    name = data["name"]

    # Check if file is a tar file
    if os.path.splitext(name)[1] == '.tar':
        source_bucket = storage_client.get_bucket(bucket)
        tar_blob = source_bucket.blob(name)

        # Download the tar file to a temporary file
        with tempfile.NamedTemporaryFile() as tar_file:
            tar_blob.download_to_file(tar_file)
            tar_file.seek(0)

            # Extract the tar file contents
            with tarfile.open(fileobj=tar_file) as tar:
                for tar_info in tar:
                    if tar_info.isfile():
                        file_data = tar.extractfile(tar_info).read()

                        # Upload the extracted file to the same bucket
                        destination_blob = source_bucket.blob(f"untarred/{tar_info.name}")
                        destination_blob.upload_from_string(file_data)
                        
        print(f"-Successfully untarred and uploaded files from {name} to the same bucket.")
    else:
        print(f"{name} is not a tar file.")