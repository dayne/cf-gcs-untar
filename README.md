# cf-gcs-untar

to invoke functions framework for testing:

$functions-framework --source=main.py --target=gcs_untar --signature-type=event

curl payload to test with bucket and name replaced with appropriate bucket and file name

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
