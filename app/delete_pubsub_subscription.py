import os
import argparse
from google.cloud import pubsub_v1

def delete_subscription(project_id, topic_id):
    """Delete an autogenerated Cloud Pub/Sub subscription"""
    host_name = os.uname()[1]
    subscription_id = f"{topic_id}-{host_name}"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project_id, subscription_id
    )
    try:
        with subscriber:
            subscriber.delete_subscription(
                subscription=subscription_path)
            print(
                f"Deleted subscription {subscription_path} in topic {topic_id}")
    except Exception as err:
        print(f"Error occured when deleting subscription {subscription_path}: {err}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project", help="The ID of the project that owns the subscription (Required)",
        default=os.getenv("GCLOUD_PROJECT_ID")
    )
    parser.add_argument(
        "--pubsub_topic", help="The ID of the Pub/Sub topic (Required)",
        default=os.getenv("GCLOUD_PUBSUB_TOPIC_ID")
    )

    args = parser.parse_args()
    print(args)

    if (not args.project) or (not args.pubsub_topic):
        exit(parser.print_help())
    delete_subscription(args.project, args.pubsub_topic)
