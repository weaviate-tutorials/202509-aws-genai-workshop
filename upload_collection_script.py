#!/usr/bin/env python3
"""
Script to upload financial articles collection to Weaviate
Based on 1.1-load-data-complete.ipynb
"""
import weaviate
import pandas as pd
import boto3
from tqdm import tqdm
from weaviate.util import generate_uuid5
from weaviate.classes.config import Configure, Property, DataType

# Configuration
COLLECTION_NAME = "FinancialArticles"
DATA_FILE = "multimodal-rag/data/fin_news_articles_5000.parquet"
BATCH_SIZE = 100
MAX_ERRORS = 10


def update_creds():
    from boto3 import Session

    # Get the AWS Credentials
    session = Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()

    AWS_ACCESS_KEY = current_credentials.access_key
    AWS_SECRET_KEY = current_credentials.secret_key
    AWS_SESSION_TOKEN = current_credentials.token
    return AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_SESSION_TOKEN


def main():
    # Get AWS credentials
    print("Getting AWS credentials...")
    AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_SESSION_TOKEN = update_creds()

    # Get Weaviate IP address
    print("Getting Weaviate IP address...")
    try:
        # Initialize AWS clients
        ecs_client = boto3.client('ecs')
        ec2_client = boto3.client('ec2')

        # Get the task ARN
        response = ecs_client.list_tasks(cluster='weaviate-cluster', serviceName='weaviate-service')
        task_arn = response['taskArns'][0]

        # Get the ENI ID
        response = ecs_client.describe_tasks(cluster='weaviate-cluster', tasks=[task_arn])
        eni_id = next(
            detail['value']
            for task in response['tasks']
            for attachment in task['attachments']
            for detail in attachment['details']
            if detail['name'] == 'networkInterfaceId'
        )

        # Get the Weaviate IP
        response = ec2_client.describe_network_interfaces(NetworkInterfaceIds=[eni_id])
        WEAVIATE_IP = response['NetworkInterfaces'][0]['Association']['PublicIp']
        print(f"Weaviate IP: {WEAVIATE_IP}")
    except Exception as e:
        print(f"Error getting Weaviate IP: {e}")
        return False

    # Connect to Weaviate
    print("Connecting to Weaviate...")
    client = weaviate.connect_to_local(
        WEAVIATE_IP,
        headers = {
            "X-AWS-Access-Key": AWS_ACCESS_KEY,
            "X-AWS-Secret-Key": AWS_SECRET_KEY,
            "X-AWS-Session-Token": AWS_SESSION_TOKEN,
        }
    )

    if not client.is_ready():
        print("Error: Weaviate client not ready")
        return False

    print("Connected to Weaviate successfully")

    try:
        # Delete existing collection if it exists
        if client.collections.exists(COLLECTION_NAME):
            print(f"Deleting existing collection: {COLLECTION_NAME}")
            client.collections.delete(COLLECTION_NAME)

        # Create collection with named vectors
        print(f"Creating collection: {COLLECTION_NAME}")
        client.collections.create(
            name=COLLECTION_NAME,
            properties=[
                Property(name="article_title", data_type=DataType.TEXT),
                Property(name="article", data_type=DataType.TEXT),
                Property(name="url", data_type=DataType.TEXT),
            ],
            vector_config=[
                Configure.Vectors.text2vec_aws(
                    name="title",
                    source_properties=["article_title"],
                    region="us-east-1",
                    service="bedrock",
                    model="amazon.titan-embed-text-v2:0"
                ),
                Configure.Vectors.text2vec_aws(
                    name="content",
                    source_properties=["article"],
                    region="us-east-1",
                    service="bedrock",
                    model="amazon.titan-embed-text-v2:0"
                )
            ],
        )

        # Load data
        print(f"Loading data from {DATA_FILE}...")
        df = pd.read_parquet(DATA_FILE)
        print(f"Loaded {len(df)} articles")

        # Get collection reference
        articles = client.collections.use(COLLECTION_NAME)

        # Import data with batch processing
        print("Importing articles...")
        with articles.batch.fixed_size(batch_size=BATCH_SIZE) as batch:
            for _, row in tqdm(df.iterrows(), total=len(df)):
                # Create object from dataframe row
                obj = {
                    "article_title": row["article_title"],
                    "article": row["article"],
                    "url": row["url"] if "url" in row else ""
                }

                # Generate UUID to prevent duplicates
                uuid = generate_uuid5(row["article_title"] + str(row.get("url", "")))

                batch.add_object(
                    properties=obj,
                    uuid=uuid
                )

                # Check for errors during import
                if batch.number_errors > MAX_ERRORS:
                    print("Too many errors during import")
                    break

        # Check for import errors
        if len(articles.batch.failed_objects) > 0:
            print(f"Import completed with {len(articles.batch.failed_objects)} errors")
            for err in articles.batch.failed_objects[:5]:  # Show first 5 errors
                print(err)
        else:
            print("Import completed successfully with no errors")

        # Verify the data
        print(f"Total articles in collection: {len(articles)}")

        # Test basic search
        response = articles.query.near_text(
            query="technology earnings",
            target_vector="title",
            limit=3
        )

        print("Sample search results for 'technology earnings':")
        for item in response.objects:
            print(f"- {item.properties['article_title']}")

        print(f"Successfully uploaded collection: {COLLECTION_NAME}")
        return True

    except Exception as e:
        print(f"Error during upload: {e}")
        return False

    finally:
        # Close the client
        client.close()
        print("Client connection closed")

if __name__ == "__main__":
    success = main()
    if success:
        print("Upload completed successfully!")
    else:
        print("Upload failed!")
