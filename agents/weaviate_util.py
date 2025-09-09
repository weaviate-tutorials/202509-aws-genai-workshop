import weaviate
import boto3
import time

class WeaviateUtil:
    """

    Static class for Weaviate connection and search operations.
    Implements singleton pattern for database connection.
    """
    _weaviate_client = None

    _connection_timestamp = None
    _CONNECTION_TIMEOUT = 30 * 60  # 30 minutes in seconds
    
    def _get_aws_credentials():
        print("Getting AWS auth credentials ...")
        session = boto3.Session()
        credentials = session.get_credentials()
        current_credentials = credentials.get_frozen_credentials()

        return current_credentials

    def _get_aws_weaviate_private_ip():
        print("Getting AWS Weaviate Private IP ...")
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
        return WEAVIATE_IP
    
    def connect() -> weaviate.WeaviateClient:
        """
        Connect to Weaviate using singleton pattern.
        Only connects once, subsequent calls return existing connection.

        Expires the connection after 30 minutes (defined in _CONNECTION_TIMEOUT)
        """
        current_time = time.time()

        # Reset the connection if older than 30 minutes
        if(WeaviateUtil._weaviate_client != None and
            current_time - WeaviateUtil._connection_timestamp > WeaviateUtil._CONNECTION_TIMEOUT
          ):
            WeaviateUtil._weaviate_client.close()
            WeaviateUtil._weaviate_client = None
        
        # Connect to Weaviate if not yet connected
        if (not WeaviateUtil._weaviate_client):
            try:
                print("Connecting to Weaviate...")

                credentials = WeaviateUtil._get_aws_credentials()
                weaviate_ip = WeaviateUtil._get_aws_weaviate_private_ip()

                # Connect to Weaviate
                WeaviateUtil._weaviate_client = weaviate.connect_to_local(
                    weaviate_ip,
                    headers={
                        "X-AWS-Access-Key": credentials.access_key,
                        "X-AWS-Secret-Key": credentials.secret_key,
                        "X-AWS-Session-Token": credentials.token,
                    }
                )
                WeaviateUtil._connection_timestamp = current_time

                print("Weaviate client is ready: ", WeaviateUtil._weaviate_client.is_ready())

            except Exception as e:
                print(f"ERROR! Failed to connect to Weaviate: {e}\n")
        else:
            print("Retrieving existing connection:")
        
        return WeaviateUtil._weaviate_client