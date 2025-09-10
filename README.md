# AWS GenAI + Weaviate: *Hands-on Workshop*

This repository is for a hands-on workshop for building intelligent search systems, RAG workflows, and AI agents, with [Weaviate vector database](https://docs.weaviate.io/weaviate) and [AWS Bedrock](https://aws.amazon.com/bedrock/) in less than a day.

> [!CAUTION]
> Optionally, you can run the workshop on your own AWS account. **Doing so will incur costs on your own account.** We cannot be responsible for any costs incurred on your personal AWS account. Please proceed with caution and at your own risk.

## Prerequisites

**None required** - AWS account and development environment provided.

Recommended: Some familiarity with AWS services and Python programming.

## Workshop instructions

> [!NOTE]
> At the workshop, the instructor will guide you through the setup. If you miss any steps, you can follow the visual GuideFlow guides linked below.

### AWS account & resources setup

Set up your own AWS account and resources for the workshop.

The instructor will take you through the same steps as in this <a href="https://app.guideflow.com/player/zklz623bop" target="_blank">GuideFlow visual guide</a>. The steps are to:

1. Go to the provided AWS workshop link to access the temporary AWS account for the workshop
    - <a href="https://catalog.us-east-1.prod.workshops.aws/join?access-code=b2e1-02c699-db" target="_blank">2025 Sep 10</a>
2. Download this <a href="./0-setup-weaviate.yaml" target="_blank">CloudFormation template file (0-setup-weaviate.yaml)</a>.
3. Set up the AWS resources, including:
    - Access the AWS workshop account.
      - You may need to authenticate with a one-time password (OTP) sent to your email.
    - Open the AWS Management Console
    - Obtain access to the Bedrock AI models
    - Spin up a Weaviate database on AWS ECS
    - Set up SageMaker Studio where you will run the workshop notebooks

### Workshop setup

1. Follow this <a href="https://app.guideflow.com/player/3r3d3nmsnp" target="_blank">visual guide for setting up the workshop repository</a>. This shows you how to:
    - Set up a SageMaker Studio JupyterLab environment
    - Clone this repository into your SageMaker Studio environment

- The "Multimodal RAG" workshop is in the `multimodal-rag` directory, with the `0-setup.ipynb` notebook.
- The "Build your own agent" workshop is in the `agent` directory, with the `lesson-1.ipynb` notebook.

## Resources

- Weaviate documentation: https://docs.weaviate.io/weaviate
- Weaviate Python client: https://weaviate-python-client.readthedocs.io
- AWS Bedrock documentation: https://docs.aws.amazon.com/bedrock/latest/userguide/
- Pydantic AI documentation: https://ai.pydantic.dev/

## Repository notes

- For students, most of the required packages are pre-installed in the SageMaker Studio environment.
    - The notebooks include any installation instructions for any additional required packages.
- This project was developed with `uv`. The primary list of required packages are in `pyproject.toml`; although a `requirements.txt` file is also provided for convenience.

## Instructor / developer notes

- There are two versions of notebooks in the `multimodal-rag` workshop:
    - `*.ipynb`: The student notebooks with student TODOs
    - `*-complete.ipynb`: The completed notebooks with solutions
- Run `generate_student_notebooks.py` from the `multimodal-rag` directory to regenerate the student notebooks from the completed notebooks.
    - See the comments in the script for more details.
