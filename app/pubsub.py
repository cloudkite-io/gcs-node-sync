#!/usr/bin/env python3

import os
import pathlib
import time

from google.cloud import pubsub_v1
from google.cloud import storage
from google.api_core.exceptions import AlreadyExists


def update_files(message, bucket, source_bucket_path, destination_folder, logger):
    attributes = message.attributes

    event_type = attributes["eventType"]
    object_id = attributes["objectId"]

    update_file = True
    file_path = f"{destination_folder}/{object_id}"
    if source_bucket_path:
        if object_id.startswith(source_bucket_path):
            file_path = f"{destination_folder}/{object_id}".replace(
                f"{source_bucket_path}/", "")
        else:
            update_file = False

    logger.debug(file_path, update_file)
    if update_file:
        try:
            file_dir = ("/").join(file_path.split("/")[:-1])
            if not os.path.exists(file_dir):
                pathlib.Path(
                    file_dir).mkdir(parents=True, exist_ok=True)
            if event_type == "OBJECT_DELETE" and ("overwrittenByGeneration" not in attributes):
                logger.debug(f"Deleted {file_path}")
                os.remove(file_path)
            elif event_type == "OBJECT_FINALIZE":
                # Download the file to a destination
                blob = bucket.blob(object_id)
                logger.debug(f"Added {file_path}")
                blob.download_to_filename(file_path)
        except Exception as err:
            logger.error("Error occured: ", err)


def poll_notifications(project_id, topic_id, source_bucket, source_bucket_path, destination_folder, logger):
    """Polls a Cloud Pub/Sub subscription for new GCS events to update local files."""
    host_name = os.uname()[1]
    subscription_id = f"{topic_id}-{host_name}"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project_id, subscription_id
    )

    storage_client = storage.Client(project_id)
    bucket = storage_client.get_bucket(source_bucket)

    def callback(message):
        update_files(message, bucket, source_bucket_path,
                     destination_folder, logger)
        message.ack()
    try:
        expiration_policy = pubsub_v1.types.ExpirationPolicy(
            ttl=pubsub_v1.types.duration_pb2.Duration(seconds=86400))
        subscriber.create_subscription(
            request={"expiration_policy": expiration_policy, "name": subscription_path, "topic": topic_path})
        logger.info(
            f"Created a subscription {subscription_path} in topic {topic_path}")
    except AlreadyExists:
        logger.info(
            f"Subscription {subscription_path} already exists in topic {topic_path}")
    subscriber.subscribe(
        subscription_path, callback=callback)

    logger.info(f"Listening for messages on {subscription_path}")
    while True:
        time.sleep(60)