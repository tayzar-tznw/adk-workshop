# Weather Agent Deployment Guide

This guide explains how to deploy the Weather Agent to Google Cloud using Vertex AI Agent Engines.

## Prerequisites

Before deploying the Weather Agent, ensure you have the following:

1. **Google Cloud Project**: You need a Google Cloud project with the Vertex AI API enabled.
2. **Google Cloud Storage Bucket**: A GCS bucket for staging deployment files.
3. **Environment Setup**: The following environment variables should be set:
   - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
   - `GOOGLE_CLOUD_LOCATION`: The Google Cloud region (e.g., "us-central1")
   - `GOOGLE_CLOUD_STORAGE_BUCKET`: The name of your GCS bucket (without "gs://")
   - `GOOGLE_API_KEY`: Your Google API key for Gemini models
   - Optional: `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` if using those models

   A template `.env.example` file is provided in this directory. You can copy it to `.env` and fill in your values:

   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Python Environment**: Python 3.11+ with the dependencies listed in pyproject.toml.

## Deployment Steps

### 1. Install Dependencies

Make sure you have the deployment dependencies installed:

```bash
pip install -e ".[deployment]"
```

This will install the required packages like `absl-py` and `cloudpickle`.

### Example Deployment Script

For a complete example of the deployment workflow, see the `example_deploy.py` script in this directory. This script demonstrates:

- Checking environment variables
- Deploying the agent
- Testing the deployed agent with a conversation
- Deleting the agent when done

You can run it with:

```bash
python -m weather_agent.deployment.example_deploy
```

### 2. Deploy the Agent

To create a new deployment, run:

```bash
python -m weather_agent.deployment.deploy --create
```

Or with explicit parameters:

```bash
python -m weather_agent.deployment.deploy \
  --create \
  --project_id=your-project-id \
  --location=us-central1 \
  --bucket=your-bucket-name
```

The script will output the resource name of the deployed agent. Save this for future operations.

### 3. Test the Deployment

To test the deployed agent with a simple query:

```bash
python -m weather_agent.deployment.deploy \
  --quicktest \
  --resource_id=projects/your-project-id/locations/us-central1/reasoningEngines/your-resource-id
```

This will send a test message ("What's the weather in London?") to the agent and print the response.

### 4. Delete the Deployment

When you're done with the deployment, you can delete it:

```bash
python -m weather_agent.deployment.deploy \
  --delete \
  --resource_id=projects/your-project-id/locations/us-central1/reasoningEngines/your-resource-id
```

## Deployment Architecture

The Weather Agent deployment uses Vertex AI Agent Engines to host the agent in Google Cloud. The deployment includes:

1. The main Weather Agent with its sub-agents (greeting and farewell)
2. All necessary tools and utilities
3. Initial session state configuration (temperature unit preference)

The deployed agent maintains the same functionality as the local version, including:
- Weather information lookup
- Multi-model support (if API keys are provided)
- Sub-agent delegation
- Session state for memory
- Safety guardrails

## Troubleshooting

If you encounter issues during deployment:

1. **Missing Dependencies**: Ensure all required packages are installed.
2. **Environment Variables**: Check that all required environment variables are set.
3. **API Enablement**: Verify that the Vertex AI API is enabled in your Google Cloud project.
4. **Permissions**: Ensure your Google Cloud account has the necessary permissions.
5. **Logs**: Check the Google Cloud logs for detailed error information.

For more information, refer to the [Vertex AI Agent Engines documentation](https://cloud.google.com/vertex-ai/docs/agent-engines/overview).
