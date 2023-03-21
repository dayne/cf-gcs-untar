## cf-gcs-untar
---
# gcp cloud function to listen for gcs finalize events for objects of type .tar or .tar.gz
# untar them and write the contents back to the bucket with the prefix /untarred
---

Google Cloud Storage (GCS) is an object storage service designed for storing, accessing, and managing large amounts of unstructured data. It is not a file system like POSIX, so it doesn't have support for traditional file operations like tarring and untarring directly within the service.

The main reasons you can't tar or untar a file directly in Cloud Storage are:

- Immutable objects: Once an object is uploaded to GCS, it is immutable, meaning it cannot be modified or appended. To perform a tar or untar operation, you would need to modify the data, which is not possible within GCS.

- No native support for compression/decompression: GCS is designed for storing and serving data rather than for processing it. It doesn't have built-in support for compression or decompression algorithms like tar or gzip.

- Lack of file system operations: GCS treats files as objects with metadata, and it doesn't support the range of file system operations that would be required to perform tar or untar operations directly within the storage.

To perform tar or untar operations on data stored in GCS, you'll need to process the data outside of the storage service. You can use services like Cloud Functions, Cloud Run, or Compute Engine instances to read the data from GCS, perform the desired operation, and then write the result back to GCS or another desired location.

---

# local testing 

pip install -r requiremnets.txt

cli invokation for the functions framework for testing:

functions-framework --source=main.py --target=gcs_untar --signature-type=event

curl payload to test with. change bucket and file to your bucket and file.
functions framework will interact with the file and the bucket. 
test with a .tar and a .tar.gz. the tar or tar.gz should exist in the bucket.

curl -X POST \
    -H "Content-Type: application/json" \
    -H "ce-specversion: 1.0" \
    -H "ce-type: google.cloud.storage.object.v1.finalized" \
    -H "ce-source: https://example.com" \
    -H "ce-id: test-event-id" \
    -d '{
          "bucket": "thatjody",
          "name": "water.tar.gz"
        }' \
    http://localhost:8080

---
# deployment

cli deployment to GCP
change region and bucket appropriately

gcloud functions deploy gcs-untar \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --source=. \
  --entry-point=hello_gcs \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=thatjody"