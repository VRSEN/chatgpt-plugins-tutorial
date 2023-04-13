# ChatGPT Plugins Tutorial
This is a FastAPI-based project that demonstrates how to create your own contextual Q&A chatgpt plugin. The application can be deployed to Google Cloud Run.

## Prerequisites
* Python 3.9
* Google Cloud SDK
# Project Structure
* main.py: The FastAPI application file.
* Dockerfile: Docker configuration file to build the application container.
* requirements.txt: Lists the required Python packages.
* README.md: This file, which explains the project setup and deployment.
## Setup
1. Clone the project to your local machine.
2. Create a virtual environment and activate it:


```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```
3. Install the required packages:

```bash 
pip install -r requirements.txt
```

## Run the Application Locally
Start the FastAPI application:

4. Add your Pinecone and OpenAI API keys to the .env file:
    
```bash
# windows
setx PINECONE_API_KEY your_pinecone_api_key
setx PINECONE_ENVIRONMENT your_pinecone_environment
setx OPENAI_API_KEY your_openai_api_key

# mac, linux
export PINECONE_API_KEY=your_pinecone_api_key
export PINECONE_ENVIRONMENT=your_pinecone_environment
export OPENAI_API_KEY=your_openai_api_key
```
# Run the Application Locally

1. Start the FastAPI application:

```
python main.py
```

# Deploy the Application to Google Cloud Run
1. Authenticate with your Google account:

```
gcloud auth login
```
2. Build the Docker image in the cloud:

```bash
gcloud builds submit --tag gcr.io/your-project-id/fastapi-app
```
Replace your-project-id with your Google Cloud project ID.

3. Deploy the Docker image to Cloud Run:

```bash
# windows
gcloud run deploy fastapi-app --image gcr.io/your-project-id/fastapi-app --platform managed --region your-region --allow-unauthenticated --set-env-vars="PINECONE_API_KEY=your_pinecone_api_key,PINECONE_ENVIRONMENT=your_pinecone_environment,OPENAI_API_KEY=your_openai_api_key"

# mac, linux
gcloud run deploy fastapi-app --image gcr.io/your-project-id/fastapi-app --platform managed --region your-region --allow-unauthenticated --set-env-vars=PINECONE_API_KEY=your_pinecone_api_key,PINECONE_ENVIRONMENT=your_pinecone_environment,OPENAI_API_KEY=your_openai_api_key
```
Replace your-project-id with your Google Cloud project ID, and your-region with the desired region for your Cloud Run service (e.g., us-central1).

4. Access the deployed FastAPI application using the URL provided in the output.