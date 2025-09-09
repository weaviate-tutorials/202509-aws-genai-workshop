from weaviate import WeaviateClient


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


def setup_weaviate_connection(WEAVIATE_IP, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_SESSION_TOKEN):
    """Helper function to connect to Weaviate with AWS credentials"""
    import weaviate

    client = weaviate.connect_to_local(
        WEAVIATE_IP,
        headers = {
            "X-AWS-Access-Key": AWS_ACCESS_KEY,
            "X-AWS-Secret-Key": AWS_SECRET_KEY,
            "X-AWS-Session-Token": AWS_SESSION_TOKEN,
        }
    )
    return client


def demo_vector_visualization():
    """Create and display vector embeddings visualization"""
    import numpy as np
    import plotly.express as px
    from sklearn.decomposition import PCA
    import pandas as pd
    import boto3
    import json

    def get_embeddings(sent_inputs):
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-west-2',
        )

        embeddings = []
        for sent in sent_inputs:
            body = json.dumps({
                "inputText": sent,
            })

            response = bedrock_runtime.invoke_model(
                body=body,
                modelId='amazon.titan-embed-text-v2:0',
                accept='application/json',
                contentType='application/json'
            )

            response_body = json.loads(response['body'].read())
            embeddings.append(response_body.get('embedding'))

        return np.array(embeddings)

    def plot_vectors(arr_in, text_inputs):
        pca = PCA(n_components=2)
        embeddings_pca = pca.fit_transform(arr_in)

        df = pd.DataFrame(embeddings_pca, columns=["PC1", "PC2"])
        df["sentence"] = text_inputs
        df["category"] = "other"
        df.loc[:4, "category"] = "cats"
        df.loc[5:9, "category"] = "dogs"
        df.loc[10:, "category"] = "other"

        fig = px.scatter(
            df,
            template="ggplot2",
            x="PC1",
            y="PC2",
            color="category",
            hover_data="sentence",
        )
        fig.update_layout(
            title="Vector Embeddings: Similar Concepts Cluster Together",
            margin=dict(l=20, r=20, b=20, t=40, pad=4)
        )
        fig.update_traces(marker_size=15)
        return fig

    # Sample sentences for demonstration
    sent_inputs = [
        # Cat-related sentences
        "The Bengal showed off its striking coat pattern.",
        "A lion's powerful roar echoed through the plains.",
        "A leopard's spots provided perfect camouflage.",
        "A cheetah's unmatched speed was impressive.",
        "The Sphynx basked in the warmth.",
        # Dog-related sentences
        "The golden retriever chased after the frisbee.",
        "The playful puppy rolled in the grass.",
        "A loyal companion is always by your side.",
        "The Labrador enjoyed playing in the water.",
        "The family adopted a furry friend.",
        # Other topics
        "The chef prepared a delicious meal.",
        "The astronomer gazed at distant stars."
    ]

    print("🔄 Generating embeddings for demonstration sentences...")
    emb_array = get_embeddings(sent_inputs)
    print(f"✅ Generated {emb_array.shape[0]} embeddings, each with {emb_array.shape[1]} dimensions")

    fig = plot_vectors(emb_array, sent_inputs)
    return fig


def load_articles_collection(client: WeaviateClient):
    """
    Script to upload financial articles collection to Weaviate
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
                    region="us-west-2",
                    service="bedrock",
                    model="amazon.titan-embed-text-v2:0"
                ),
                Configure.Vectors.text2vec_aws(
                    name="content",
                    source_properties=["article"],
                    region="us-west-2",
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



def demo_search_comparison(client: WeaviateClient):
    """Demonstrate different search types with the same query"""
    from weaviate.classes.query import MetadataQuery

    articles = client.collections.use("FinancialArticles")
    query = "technology earnings"

    print("🔍 **SEARCH COMPARISON DEMO**")
    print(f"Query: '{query}'\n")

    # Keyword Search (BM25)
    print("**1. KEYWORD SEARCH (BM25)**")
    print("Finds exact word matches...")
    response = articles.query.bm25(
        query=query,
        query_properties=["article_title"],
        limit=3,
        return_metadata=MetadataQuery(score=True)
    )

    for i, item in enumerate(response.objects, 1):
        print(f"   {i}. {item.properties['article_title']} (Score: {item.metadata.score:.2f})")

    print()

    # Vector Search
    print("**2. VECTOR SEARCH (Semantic)**")
    print("Finds conceptually similar content...")
    response = articles.query.near_text(
        query=query,
        target_vector="title",
        limit=3,
        return_metadata=MetadataQuery(distance=True)
    )

    for i, item in enumerate(response.objects, 1):
        print(f"   {i}. {item.properties['article_title']} (Distance: {item.metadata.distance:.3f})")

    print()

    # Hybrid Search
    print("**3. HYBRID SEARCH (Best of Both)**")
    print("Combines keyword matching + semantic understanding...")
    response = articles.query.hybrid(
        query=query,
        query_properties=["article_title"],
        target_vector="title",
        alpha=0.7,
        limit=3,
        return_metadata=MetadataQuery(score=True)
    )

    for i, item in enumerate(response.objects, 1):
        print(f"   {i}. {item.properties['article_title']} (Score: {item.metadata.score:.3f})")


def load_pages_collection(client: WeaviateClient):
    from weaviate.classes.config import Property, DataType, Configure, Tokenization
    from tqdm import tqdm
    from pathlib import Path
    import base64
    from weaviate.util import generate_uuid5

    client.collections.create(
        name="Pages",
        properties=[
            Property(
                name="document_title",
                data_type=DataType.TEXT,
            ),
            Property(
                name="page_image",
                data_type=DataType.BLOB,
            ),
            Property(
                name="filename",
                data_type=DataType.TEXT,
                tokenization=Tokenization.FIELD
            ),
        ],
        vector_config=[
            Configure.Vectors.multi2vec_aws(
                name="page",
                image_fields=["page_image"],
                region="us-west-2",
                model="amazon.titan-embed-image-v1"
            )
        ]
    )
    pages = client.collections.use("Pages")
    img_files = sorted(Path("data/imgs").glob("*.jpg"))

    with pages.batch.fixed_size(batch_size=10) as batch:
        for filepath in tqdm(img_files[:100]):
            image = filepath.read_bytes()
            base64_image = base64.b64encode(image).decode('utf-8')
            obj = {
                "document_title": "HAI report",
                "page_image": base64_image,
                "filename": filepath.name
            }

            # Add object to batch for import with (batch.add_object())
            batch.add_object(
                properties=obj,
                uuid=generate_uuid5(filepath.name)
            )


def demo_multimodal_rag(client):
    """Demonstrate multimodal RAG with PDF pages as images"""
    from weaviate.classes.generate import GenerativeConfig, GenerativeParameters
    import matplotlib.pyplot as plt
    from PIL import Image

    def display_imgs(images_to_display):
        fig, axes = plt.subplots(1, len(images_to_display), figsize=(15, 8))
        if len(images_to_display) == 1:
            axes = [axes]

        for i, img_path in enumerate(images_to_display):
            img = Image.open(img_path)
            axes[i].imshow(img)
            axes[i].axis('off')
            axes[i].set_title(f"Retrieved Page {i+1}", fontsize=12)

        plt.tight_layout()
        plt.show()

    pages = client.collections.use("Pages")

    print("🖼️ **MULTIMODAL RAG DEMO**")
    print("Searching PDF pages using text queries, then generating insights from images...\n")

    query = "self-driving cars"
    print(f"📝 Query: '{query}'")

    # Search for relevant pages
    response = pages.query.near_text(
        query=query,
        limit=2,
    )

    print(f"📄 Found {len(response.objects)} relevant pages:")
    for i, obj in enumerate(response.objects, 1):
        print(f"   {i}. {obj.properties['filename']}")

    # Display the retrieved images
    print(f"\n🔍 **Retrieved Pages:**")
    images = [f"data/imgs/" + o.properties['filename'] for o in response.objects]
    display_imgs(images)

    # Generate response using RAG
    print(f"🤖 **AI Analysis:**")
    prompt = GenerativeParameters.grouped_task(
        prompt="What does this say about self-driving cars? Provide a detailed analysis based on the images.",
        image_properties=["page_image"]
    )

    gen_config_aws = GenerativeConfig.aws(
        region="us-west-2",
        service="bedrock",
        model="us.amazon.nova-pro-v1:0"
    )

    response = pages.generate.near_text(
        query=query,
        limit=2,
        grouped_task=prompt,
        generative_provider=gen_config_aws
    )

    print(f"✨ **Generated Insights:**")
    print("-" * 60)
    print(response.generative.text)
    print("-" * 60)
