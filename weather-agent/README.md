# Weather Agent

A sophisticated weather agent built with the [Agent Development Kit (ADK)](https://github.com/google/adk-python) that provides weather information for specific cities. This agent demonstrates several advanced ADK features:

## Features

- **Weather Information**: Provides weather reports for specific cities
- **Multi-Model Support**: Can use different AI models (Gemini, GPT, Claude) via LiteLLM integration
- **Agent Team**: Uses specialized sub-agents for different tasks:
  - **Greeting Agent**: Handles greetings and welcomes
  - **Farewell Agent**: Handles goodbyes and conversation endings
  - **Root Agent**: Coordinates the team and handles weather requests
- **Memory**: Remembers user preferences (like temperature unit) and previous cities checked using Session State
- **Safety Guardrails**: Implements input validation and filtering using callbacks

## Project Structure

```
weather-agent/
├── weather_agent/           # Main code directory
│   ├── agent.py             # Root agent definition
│   ├── prompt.py            # Prompt templates
│   ├── sub_agents/          # Specialized sub-agents
│   │   ├── greeting/        # Greeting agent
│   │   └── farewell/        # Farewell agent
│   ├── shared_libraries/    # Shared code and utilities
│   └── tools/               # Tool implementations
├── deployment/              # Deployment-related files
├── examples/                # Some sample codes to undertand what weather agent can do
├── tests/                   # Test files
├── eval/                    # Evaluation files
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## Getting Started

### Prerequisites

Ensure you have the following:

1. **Google Cloud Project**: You need a Google Cloud project with the Vertex AI API enabled.
2. **Google Cloud Storage Bucket**: A GCS bucket for staging deployment files.
3. **Environment Setup**: The following environment variables should be set:
    - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
    - `GOOGLE_CLOUD_LOCATION`: The Google Cloud region (e.g., "us-central1")
    - `GOOGLE_CLOUD_STORAGE_BUCKET`: The name of your GCS bucket (without "gs://")
    - `GOOGLE_API_KEY`: Your Google API key for Gemini models
4. **Python Environment**: Python 3.11+ with the dependencies listed in pyproject.toml.

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd weather-agent
   ```

2. Install dependencies and activate environment:
   ```bash
   poetry install
   eval $( poetry env activate)
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root.
   - Fill in the necessary variables based on `.env.sample`
   - Run `set -a ; . ./.env ; set +a` in bash to load all the environment variables

### Running the Agent

You can run the agent using the ADK CLI:

```bash
adk web
```

Or programmatically:

```python
from weather_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Set up session service
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name="weather_agent_app",
    user_id="user_1",
    session_id="session_001"
)

# Create runner
runner = Runner(
    agent=root_agent,
    app_name="weather_agent_app",
    session_service=session_service
)
```

## Deployment

The Weather Agent can be deployed to Google Cloud using Vertex AI Agent Engines. This allows you to host the agent in the cloud and make it accessible via API.

Key deployment features:
- Cloud-based hosting on Google Cloud
- Scalable infrastructure
- Persistent sessions
- Monitoring and logging
- API access


## Deployment Steps
### 1. Deploy the Agent

To create a new deployment, run:

```bash
python -m deployment.deploy --create
```

Or with explicit parameters:

```bash
python -m deployment.deploy \
  --create \
  --project_id=your-project-id \
  --location=us-central1 \
  --bucket=your-bucket-name
```

The script will output the resource name of the deployed agent. Save this for future operations.

### 2. Test the Deployment

To test the deployed agent with a simple query:

```bash
python -m deployment.deploy \
  --quicktest \
  --resource_id=your-resource-id
```

This will send a test message ("What's the weather in London?") to the agent and print the response.

### 3. Delete the Deployment

When you're done with the deployment, you can delete it:

```bash
python -m deployment.deploy \
  --delete \
  --resource_id=your-resource-id
```

### Testing the deployment workflow

For a complete example of the deployment workflow, see the `tests/deploy_test.py` script in this directory. This script demonstrates:

- Checking environment variables
- Deploying the agent
- Testing the deployed agent with a conversation
- Deleting the agent when done

You can run it with:

```bash
python -m tests.deploy_test
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
