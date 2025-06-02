# Agent Chat UI

A simple Streamlit-based chat interface for interacting with agents deployed on Agent Engine.

## Prerequisites

- Python 3.9+
- A Google Cloud project with Agent Engine enabled
- An agent deployed on Agent Engine
- Google Cloud credentials configured

## Environment Variables

Create a `.env` file in the `chat-ui` directory with the following variables:

```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=your-location
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
```

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run main.py
```

The application will be available at http://localhost:8080.

## Usage

1. Enter the full resource name of your deployed agent in the sidebar.
   - Example: `projects/your-project-id/locations/your-location/agents/your-agent-id`

2. Click "Create New Session" to establish a connection with the agent.

3. Type your message in the chat input at the bottom of the screen and press Enter to send.

4. The agent's response will be displayed in the chat.

## Deployment to Cloud Run

This application can be deployed to Google Cloud Run for production use. We recommend using Google Cloud Build for an automated CI/CD pipeline:

```bash
# Deploy using Cloud Build (recommended)
gcloud builds submit --config=cloudbuild.yaml
```

For detailed deployment instructions and options, see [DEPLOY.md](DEPLOY.md).

For a summary of what we've accomplished and next steps, see [SUMMARY.md](SUMMARY.md).

## References

This application was built using:
- [Streamlit](https://streamlit.io/)
- [Vertex AI Agent Engine SDK](https://google.github.io/adk-docs/deploy/agent-engine/)
