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

#### Option 1: Using the Default Service Account (Simple)

1. Assign the necessary IAM roles to the default Cloud Run service account:
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

#### Option 2: Creating a Custom Service Account (Recommended for Production)

Creating a custom service account for your Chat UI Cloud Run service follows the principle of least privilege and provides better security and access control:

1. Create custom service accounts:

```bash
# For demonstration purposes, we'll create two service accounts:
# - agent-deny-sa: A service account without proper permissions (will fail)
# - agent-allowed-sa: A service account with proper permissions (will succeed)

# Create a service account for demonstrating access denial
gcloud iam service-accounts create agent-deny-sa \
  --display-name="Agent Deny Service Account" \
  --description="Service account for demonstrating access denial"

# Create a service account for demonstrating access approval
gcloud iam service-accounts create agent-allowed-sa \
  --display-name="Agent Allow Service Account" \
  --description="Service account for demonstrating access approval"
```

> **Note**: In a real production environment, you would typically create a single service account with the appropriate permissions, such as `chat-ui-sa`. The two service accounts created here are for demonstration purposes to show how access management works.

2. Assign the necessary IAM roles to the custom service accounts:

```bash
# For the agent-allowed-sa (the one that will work)
# Grant Vertex AI User role for accessing Agent Engine
gcloud projects add-iam-policy-binding your-project-id \
  --member=serviceAccount:agent-allowed-sa@your-project-id.iam.gserviceaccount.com \
  --role=roles/aiplatform.user
# Note: We intentionally don't assign roles to agent-deny-sa to demonstrate access denial
```

3. Grant the Cloud Build service account permission to act as the custom service accounts:

```bash
# Get the Cloud Build service account email
CLOUDBUILD_SA=$(gcloud projects get-iam-policy your-project-id \
  --filter="(bindings.role:roles/cloudbuild.builds.builder)" \
  --format="value(bindings.members)" | grep serviceAccount | sed "s/serviceAccount://")

# If the above command doesn't work, you can manually specify the Cloud Build service account
# CLOUDBUILD_SA="your-project-number@cloudbuild.gserviceaccount.com"

# Grant the Cloud Build service account permission to act as both service accounts
# This is the critical step that resolves the "iam.serviceaccounts.actAs" permission error

# For agent-deny-sa
gcloud iam service-accounts add-iam-policy-binding agent-deny-sa@your-project-id.iam.gserviceaccount.com \
  --member="serviceAccount:${CLOUDBUILD_SA}" \
  --role="roles/iam.serviceAccountUser"

# For agent-allowed-sa
gcloud iam service-accounts add-iam-policy-binding agent-allowed-sa@your-project-id.iam.gserviceaccount.com \
  --member="serviceAccount:${CLOUDBUILD_SA}" \
  --role="roles/iam.serviceAccountUser"
```

4. Update your Cloud Run deployment command to use the custom service accounts:

For manual deployment:
```bash
# Deploy with agent-deny-sa (will fail due to missing permissions)
gcloud run deploy chat-ui-deny \
  --image gcr.io/your-project-id/chat-ui:latest \
  --platform managed \
  --region your-region \
  --service-account agent-deny-sa@your-project-id.iam.gserviceaccount.com \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project-id,GOOGLE_CLOUD_LOCATION=your-location,GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name

# Deploy with agent-allowed-sa (will succeed with proper permissions)
gcloud run deploy chat-ui-allow \
  --image gcr.io/your-project-id/chat-ui:latest \
  --platform managed \
  --region your-region \
  --service-account agent-allowed-sa@your-project-id.iam.gserviceaccount.com \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project-id,GOOGLE_CLOUD_LOCATION=your-location,GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
```

For Cloud Build deployment, you can use the provided `cloudbuild-custom-sa.yaml` file which includes the service account configuration:

```bash
# Deploy using Cloud Build with custom service account
gcloud builds submit --config=cloudbuild-custom-sa.yaml
```

The `cloudbuild-custom-sa.yaml` file includes the following configuration for the service account:

```yaml
steps:
  # ... other steps ...
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: Deploy
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'chat-ui'
      - '--image'
      - 'gcr.io/$PROJECT_ID/chat-ui:latest'
      - '--region'
      - '${_REGION}'
      - '--platform'
      - 'managed'
      - '--service-account'
      - 'agent-deny-sa@$PROJECT_ID.iam.gserviceaccount.com'
      - '--allow-unauthenticated'
      - '--set-env-vars'
      - 'GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=${_REGION},GOOGLE_CLOUD_STORAGE_BUCKET=${_BUCKET}'
```

> **Note**: The deployment using `agent-deny-sa` will fail with the error "Permission 'iam.serviceaccounts.actAs' denied" if you haven't completed step 3 above to grant the Cloud Build service account permission to act as the custom service accounts.

5. If you need to grant additional permissions for specific Agent Engine features, you can add more granular roles:

```bash
# For accessing specific Agent Engine features (for agent-allowed-sa)
gcloud projects add-iam-policy-binding your-project-id \
  --member=serviceAccount:agent-allowed-sa@your-project-id.iam.gserviceaccount.com \
  --role=roles/aiplatform.agentEndpointUser
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

1. **Permission 'iam.serviceaccounts.actAs' denied**: This error occurs when the Cloud Build service account doesn't have permission to act as the custom service account. To fix this:

   ```bash
   # Get the Cloud Build service account email
   
   CLOUDBUILD_SA=$(gcloud projects get-iam-policy your-project-id \
     --filter="(bindings.role:roles/cloudbuild.builds.builder)" \
     --format="value(bindings.members)" | grep serviceAccount | sed "s/serviceAccount://")

   # Grant the Cloud Build service account permission to act as the custom service account
   gcloud iam service-accounts add-iam-policy-binding your-custom-sa@your-project-id.iam.gserviceaccount.com \
     --member="serviceAccount:${CLOUDBUILD_SA}" \
     --role="roles/iam.serviceAccountUser"
   
    CLOUDBUILD_SA=$(gcloud projects get-iam-policy development-459201 \
     --filter="(bindings.role:roles/cloudbuild.builds.builder)" \
     --format="value(bindings.members)" | grep serviceAccount | sed "s/serviceAccount://")

   # Grant the Cloud Build service account permission to act as the custom service account
   gcloud iam service-accounts add-iam-policy-binding agent-deny-sa@development-459201.iam.gserviceaccount.com \
     --member="serviceAccount:1017461389635-compute@developer.gserviceaccount.com" \
     --role="roles/iam.serviceAccountUser"
   ```

   Make sure to replace `your-custom-sa` with the actual service account name (e.g., `agent-deny-sa` or `agent-allowed-sa`).

2. **Authentication Errors**: Ensure that the service account has the necessary permissions for accessing Vertex AI and other required services.

3. **Missing Environment Variables**: Verify that all required environment variables are set.

4. **Agent Not Found**: Double-check the agent resource name format.

5. **Connection Issues**: Ensure that the necessary APIs are enabled in your Google Cloud project.

### Viewing Logs

To view the application logs:

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chat-ui" --limit=50
```
