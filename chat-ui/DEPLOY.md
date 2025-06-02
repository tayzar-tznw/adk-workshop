# Deploying Chat UI to Cloud Run

This document provides instructions for deploying the Chat UI application to Google Cloud Run and connecting it to an agent deployed on Agent Engine.

## Prerequisites

- Google Cloud SDK installed and configured
- Docker installed (for local testing)
- A Google Cloud project with the following APIs enabled:
  - Cloud Run API
  - Cloud Build API
  - Container Registry API
  - Vertex AI API
- An agent deployed on Agent Engine

## Deployment Options

### Option 1: Manual Deployment

1. Build the Docker image locally:

```bash
cd chat-ui
docker build -t chat-ui .
```

2. Test the Docker image locally:

```bash
docker run -p 8080:8080 \
  -e GOOGLE_CLOUD_PROJECT=your-project-id \
  -e GOOGLE_CLOUD_LOCATION=your-location \
  -e GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name \
  chat-ui

docker run -p 8080:8080 \
  -e GOOGLE_CLOUD_PROJECT=development-459201 \
  -e GOOGLE_CLOUD_LOCATION=us-central1 \
  -e GOOGLE_CLOUD_STORAGE_BUCKET=adk-mini-tap \
  chat-ui
```

3. Tag and push the image to Google Container Registry:

```bash
docker tag chat-ui gcr.io/your-project-id/chat-ui:latest
docker push gcr.io/your-project-id/chat-ui:latest
```

4. Deploy to Cloud Run:

```bash
gcloud run deploy chat-ui \
  --image gcr.io/your-project-id/chat-ui:latest \
  --platform managed \
  --region your-region \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project-id,GOOGLE_CLOUD_LOCATION=your-location,GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
```

### Option 2: Automated Deployment with Cloud Build (Recommended)

Cloud Build provides a fully managed CI/CD platform that automates the build, test, and deployment process. This is the recommended approach for deploying the Chat UI application.

1. Update the substitution values in `cloudbuild.yaml` if needed:

```yaml
substitutions:
  _REGION: your-region  # e.g., us-central1
  _BUCKET: your-bucket-name
```

2. Verify your Cloud Build configuration (optional but recommended):

```bash
# Make the test script executable
chmod +x test_cloudbuild.sh

# Run the test script
./test_cloudbuild.sh
```

This script will check if:
- The gcloud CLI is installed and configured
- Required Google Cloud APIs are enabled
- The cloudbuild.yaml syntax is valid
- Substitution variables are properly set

3. Trigger the build and deployment:

```bash
gcloud builds submit --config=cloudbuild.yaml
```

4. Monitor the build progress in the Google Cloud Console:
   - Go to Cloud Build > History
   - Click on the running build to view logs and details

#### Benefits of Using Cloud Build

- **Fully Managed**: No need to maintain build infrastructure
- **Integrated**: Seamless integration with other Google Cloud services
- **Scalable**: Automatically scales to handle your build needs
- **Efficient**: Uses build caching to speed up subsequent builds
- **Consistent**: Ensures consistent build environments
- **Secure**: Runs in isolated environments with IAM controls

#### Customizing the Build Process

The `cloudbuild.yaml` file can be customized to fit your specific needs:

- **Machine Type**: Change the `machineType` in the options section for faster builds
- **Build Steps**: Add or modify steps for additional build tasks
- **Caching**: Adjust caching settings for optimal performance
- **Timeout**: Set custom timeouts for long-running builds
- **Notifications**: Configure build notifications via Cloud Pub/Sub

## Authentication

The application needs to authenticate with Google Cloud to access Agent Engine. There are several ways to handle this:

### For Local Development

1. Use Application Default Credentials:

```bash
gcloud auth application-default login
```

2. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
```

### For Cloud Run Deployment

1. Assign the necessary IAM roles to the Cloud Run service account:
   - Vertex AI User
   - Storage Object Viewer (if accessing files in Cloud Storage)

```bash
gcloud projects add-iam-policy-binding your-project-id \
  --member=serviceAccount:your-project-number-compute@developer.gserviceaccount.com \
  --role=roles/aiplatform.user

gcloud projects add-iam-policy-binding your-project-id \
  --member=serviceAccount:your-project-number-compute@developer.gserviceaccount.com \
  --role=roles/storage.objectViewer
```

## Testing the Deployed Application

### Manual Testing

1. After deployment, Cloud Run will provide a URL for your application (e.g., `https://chat-ui-abcdef-uc.a.run.app`).

2. Open the URL in your browser.

3. In the sidebar, enter the full resource name of your deployed agent:
   - Format: `projects/your-project-id/locations/your-location/agents/your-agent-id`

4. Click "Create New Session" to establish a connection with the agent.

5. Type a message in the chat input and press Enter to send.

6. The agent's response will be displayed in the chat.

### Automated Testing

You can use the included `test_deployment.py` script to verify your deployment and connection to Agent Engine:

```bash
# Install test dependencies
pip install requests

# Test only the agent connection
python test_deployment.py --agent "projects/your-project-id/locations/your-location/agents/your-agent-id"

# Test both the Cloud Run deployment and agent connection
python test_deployment.py --url "https://chat-ui-abcdef-uc.a.run.app" --agent "projects/your-project-id/locations/your-location/agents/your-agent-id"
```

The script will:
- Check if the required environment variables are set
- Test if the Cloud Run deployment is accessible (if URL is provided)
- Test if the agent can be accessed and queried
- Display the results with clear success/failure indicators

## Deploying an Agent to Agent Engine

If you haven't already deployed an agent to Agent Engine, you can follow these steps:

1. Navigate to the agent directory (e.g., `weather-agent`).

2. Use the deployment script:

```bash
python -m weather_agent.deployment.deploy --create
```

3. Note the resource name of the deployed agent, which will be displayed in the output.

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure that the service account has the necessary permissions.

2. **Missing Environment Variables**: Verify that all required environment variables are set.

3. **Agent Not Found**: Double-check the agent resource name format.

4. **Connection Issues**: Ensure that the necessary APIs are enabled in your Google Cloud project.

### Viewing Logs

To view the application logs:

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chat-ui" --limit=50
```
