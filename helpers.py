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