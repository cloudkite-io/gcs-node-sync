#!/usr/bin/env python3

import os
import pathlib
import argparse
from helper_utils import exec_shell_command
import logging
from pubsub import poll_notifications

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
    )
    parser.add_argument(
        "--project", help="The ID of the project that owns the subscription (Required)",
        default=os.getenv("GCLOUD_PROJECT_ID")
    )
    parser.add_argument(
        "--pubsub_topic", help="The ID of the Pub/Sub topic configured to receive notifications from GCS (Required)",
        default=os.getenv("GCLOUD_PUBSUB_TOPIC_ID")
    )
    parser.add_argument(
        "--source_bucket", help="The GCS Bucket to fetch data from (Required)",
        default=os.getenv("GCLOUD_BUCKET_NAME")
    )
    parser.add_argument(
        "--source_bucket_path", required=False, help="The specific GCS Bucket's path to fetch data from",
        default=os.getenv("GCLOUD_BUCKET_PATH")
    )
    parser.add_argument(
        "--destination_folder", required=False, help="The absolute local path where the GCS bucket's contents will be stored",
        default=os.getenv("GCLOUD_DESTINATION_FOLDER")
    )   

    logger = logging.getLogger(__name__)

    logging.basicConfig(
        format="%(asctime)-15s %(levelname)-8s %(message)s",
        level=logging.INFO
    )
    args = parser.parse_args()
    logger.debug(args)

    if (not args.project) or (not args.source_bucket) or (not args.pubsub_topic):
        exit(parser.print_help())
      
    if (args.source_bucket_path):
        source_bucket_path = args.source_bucket_path.lstrip('/')
        bucket_path = f"gs://{args.source_bucket}/{source_bucket_path}"
    else:
        source_bucket_path = None
        bucket_path = f"gs://{args.source_bucket}"

    if args.destination_folder:
        destination_folder = args.destination_folder.rstrip('/')
    else:
        destination_folder = f"/var/tmp/buckets/{args.source_bucket}"
    
    if not os.path.exists(destination_folder):
        pathlib.Path(
            destination_folder).mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving GCS bucket {bucket_path} to {destination_folder}")

    rsync_output = exec_shell_command(
        ['time', 'gsutil', '-m', 'cp', '-r', bucket_path, destination_folder]
    )
    
    # TO-DO: Write to a file after successfull file sync
    poll_notifications(args.project, args.pubsub_topic, args.source_bucket,
                       source_bucket_path, destination_folder, logger)
