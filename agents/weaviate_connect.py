import weaviate
from boto3 import Session

class WeaviateConnect:
    """
    Static class for Weaviate connection and search operations.
    Implements singleton pattern for database connection.
    """
    _weaviate_client = None
    # _client_connection_timestamp = None
    
    
    def _connect() -> weaviate.WeaviateClient:
        """
        Connect to Weaviate using singleton pattern.
        Only connects once, subsequent calls return existing connection.
        """

        # Connect to Weaviate if not yet connected
        if not WeaviateConnect._weaviate_client:
            print("Getting AWS auth credentials ...")
            session = Session()
            credentials = session.get_credentials()
            current_credentials = credentials.get_frozen_credentials()

            AWS_ACCESS_KEY = current_credentials.access_key
            AWS_SECRET_KEY = current_credentials.secret_key
            AWS_SECRET_TOKEN = current_credentials.token
            print(f"AWS_ACCESS_KEY:\t{AWS_ACCESS_KEY}")
            print(f"AWS_SECRET_KEY:\t{AWS_SECRET_KEY}")
            print(f"AWS_SECRET_TOKEN:\t{AWS_SECRET_TOKEN}")

            try:
                print("Connecting to Weaviate...")

                # Connect to Weaviate
                WeaviateConnect._weaviate_client = weaviate.connect_to_local(
                    "10.0.2.185", # YOU Private IP address goes here
                    headers={
                        "X-AWS-Access-Key": AWS_ACCESS_KEY,
                        "X-AWS-Secret-Key": AWS_SECRET_KEY,
                        "X-AWS-Session-Token": AWS_SECRET_TOKEN,
                    }
                )

                print("Weaviate client is ready: ", WeaviateConnect._weaviate_client.is_ready())

            except Exception as e:
                print(f"ERROR! Failed to connect to Weaviate: {e}\n")

        
        return WeaviateConnect._weaviate_client