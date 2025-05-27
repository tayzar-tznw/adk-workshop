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

- Python 3.11 or higher
- API keys for the LLMs you intend to use (Google AI Studio for Gemini, OpenAI Platform for GPT, Anthropic Console for Claude)

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

# Run the agent (async)
# See documentation for details on how to interact with the agent
```

### Deployment

The Weather Agent can be deployed to Google Cloud using Vertex AI Agent Engines. This allows you to host the agent in the cloud and make it accessible via API.

For detailed deployment instructions, see the [Deployment Guide](deployment/README.md).

Key deployment features:
- Cloud-based hosting on Google Cloud
- Scalable infrastructure
- Persistent sessions
- Monitoring and logging
- API access
