This application synchronizes a GCS bucket to a local folder.

## How it works
The application starts off by running [gsutil rsync](https://cloud.google.com/storage/docs/gsutil/commands/rsync) to get all the contents of a GCS bucket.  
The application then creates a Pub/Sub subscription attached to the topic (where notifications from GCS are sent to) and indefinitely listens to it for events while writing/deleting files based on the event type.

## Prerequisites
1. Activate the Google Cloud Pub/Sub API, if you have not already done so.
   https://console.cloud.google.com/flows/enableapi?apiid=pubsub

2. Configure Pub/Sub notifications for Cloud Storage https://cloud.google.com/storage/docs/reporting-changes#rest-apis_1

## Usage
The application is started by navigating to the `app` directory and running:  
```
main.py --project GCLOUD_PROJECT_ID --pubsub_topic GCLOUD_PUBSUB_TOPIC_ID --source_bucket GCLOUD_BUCKET_NAME --source_bucket_path GCLOUD_BUCKET_PATH --destination_folder GCLOUD_DESTINATION_FOLDER
```

The input parameters may also be passed as environment variables as shown in the table below:  

| INPUT PARAMETER NAME                                  | DESCRIPTION                                                                                          |         REQUIRED? |         DEFAULT VALUE |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------- |
| GCLOUD_PROJECT_ID                                  | The ID of the GCP project that owns the subscription | Yes | None |
| GCLOUD_PUBSUB_TOPIC_ID                    | The ID of the Pub/Sub topic that receives notifications of changes to your GCS bucket | Yes | None |
| GCLOUD_BUCKET_NAME                                 | The name of the GCS Bucket to sync data from | Yes | None |
| GCLOUD_BUCKET_PATH                                 | The path to a specific folder in your GCS Bucket that you'd like to sync data from (Optional) | No | / |
| GCLOUD_DESTINATION_FOLDER                          | The absolute local path where the GCS bucket's contents will be stored (Optional) | No | /tmp/buckets/  |

A `sample.env` file is provided in the root folder to be used as a template for the environment variables.

### Docker image
gcs-node-sync is publicly accessible as a Docker image:

```
gcr.io/cloudkite-public/gcs-node-sync:latest
```

### Deleting the Pub/Sub subscription.
The `app/delete_pubsub_subscription.py` is a small Python script which deletes the Pub/Sub subscription created by the `app/main.py` script. It requires only two arguments which can be passed as environment variables:

| INPUT PARAMETER NAME                                  | DESCRIPTION                                                                                          |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| GCLOUD_PROJECT_ID                                  | The ID of the GCP project that owns the subscription |
| GCLOUD_PUBSUB_TOPIC_ID                    | The ID of the Pub/Sub topic that receives notifications of changes to your GCS bucket |

Usage:
`app/delete_pubsub_subscription.py --project GCLOUD_PROJECT_ID --pubsub_topic GCLOUD_PUBSUB_TOPIC_ID`