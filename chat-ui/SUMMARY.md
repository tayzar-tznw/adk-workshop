# Chat UI Deployment Summary

## What We've Accomplished

We've created a complete solution for deploying the Chat UI application to Google Cloud Run and connecting it to agents deployed on Agent Engine:

1. **Streamlit Application**
   - A simple, user-friendly chat interface
   - Connection to Agent Engine using the Vertex AI SDK
   - Support for streaming responses

2. **Deployment Infrastructure**
   - Dockerfile for containerization
   - Cloud Build configuration for automated CI/CD
   - Optimized build process with caching and parallel execution
   - Comprehensive deployment instructions

3. **Testing Tools**
   - Test script for verifying deployment
   - Instructions for both manual and automated testing

## Files Created

- `main.py`: The Streamlit application
- `requirements.txt`: Dependencies for the application
- `Dockerfile`: Container configuration for Cloud Run
- `cloudbuild.yaml`: CI/CD configuration for Google Cloud Build
- `test_deployment.py`: Script for testing the deployment
- `DEPLOY.md`: Detailed deployment instructions
- `.env.example`: Template for environment variables

## Next Steps

1. **Deploy an Agent to Agent Engine**
   ```bash
   cd ../weather-agent
   python -m weather_agent.deployment.deploy --create
   ```
   Note the resource name of the deployed agent.

2. **Deploy the Chat UI to Cloud Run using Cloud Build (Recommended)**
   ```bash
   cd ../chat-ui

   # Optional: Update region and bucket name in cloudbuild.yaml if needed
   # Edit the substitutions section in cloudbuild.yaml

   # Verify your Cloud Build configuration (recommended)
   chmod +x test_cloudbuild.sh
   ./test_cloudbuild.sh

   # Trigger the build and deployment
   gcloud builds submit --config=cloudbuild.yaml

   # Monitor the build in the Google Cloud Console
   # Go to Cloud Build > History to view build progress
   ```
   Note the URL of the deployed application, which will be displayed in the build output and in the Cloud Run console.

3. **Create a Custom Service Account for Cloud Run (Recommended for Production)**
   ```bash
   # Create a new service account for the Chat UI application
   gcloud iam service-accounts create agent-deny-sa \
     --display-name="Agent Deny Service Account" \
     --description="Service account for demonstrating accessing denial"

   gcloud iam service-accounts create agent-allowed-sa \
     --display-name="Agent Allow Service Account" \
     --description="Service account for demonstrating accessing approval"

   # Grant Vertex AI User role for accessing Agent Engine
   gcloud projects add-iam-policy-binding your-project-id \
     --member=serviceAccount:agent-allowed-sa@your-project-id.iam.gserviceaccount.com \
     --role=roles/aiplatform.user

   gcloud projects add-iam-policy-binding development-459201 \
     --member=serviceAccount:agent-allowed-sa@development-459201.iam.gserviceaccount.com \
     --role=roles/aiplatform.user

   # Grant the Cloud Build service account permission to act as the custom service account
   CLOUDBUILD_SA=$(gcloud projects get-iam-policy your-project-id \
     --filter="(bindings.role:roles/cloudbuild.builds.builder)" \
     --format="value(bindings.members)" | grep serviceAccount | sed "s/serviceAccount://")

   gcloud iam service-accounts add-iam-policy-binding agent-deny-sa@your-project-id.iam.gserviceaccount.com \
     --member="serviceAccount:${CLOUDBUILD_SA}" \
     --role="roles/iam.serviceAccountUser"

   gcloud iam service-accounts add-iam-policy-binding agent-allowed-sa@your-project-id.iam.gserviceaccount.com \
     --member="serviceAccount:${CLOUDBUILD_SA}" \
     --role="roles/iam.serviceAccountUser"

   # Update an existing Cloud Run service to use the custom service account
   gcloud run services update chat-ui \
     --service-account chat-ui-sa@your-project-id.iam.gserviceaccount.com \
     --region your-region

   # Deploy using Cloud Build with the custom service account
   gcloud builds submit --config=cloudbuild-custom-sa.yaml
   ```
   This step follows the principle of least privilege and provides better security and access control for your production deployment.

4. **Test the Deployment**
   ```bash
   python test_deployment.py --url "https://chat-ui-abcdef-uc.a.run.app" --agent "projects/your-project-id/locations/your-location/agents/your-agent-id"
   ```

5. **Access the Application**
   Open the Cloud Run URL in your browser and start chatting with your agent!

## Troubleshooting

If you encounter any issues:

1. **Permission 'iam.serviceaccounts.actAs' denied**: This is a common error when using custom service accounts with Cloud Build. Make sure you've granted the Cloud Build service account permission to act as your custom service account:
   ```bash
   # Get the Cloud Build service account email
   CLOUDBUILD_SA=$(gcloud projects get-iam-policy your-project-id \
     --filter="(bindings.role:roles/cloudbuild.builds.builder)" \
     --format="value(bindings.members)" | grep serviceAccount | sed "s/serviceAccount://")

   # Grant the Cloud Build service account permission to act as the custom service account
   gcloud iam service-accounts add-iam-policy-binding agent-deny-sa@your-project-id.iam.gserviceaccount.com \
     --member="serviceAccount:${CLOUDBUILD_SA}" \
     --role="roles/iam.serviceAccountUser"
   ```

2. Check the logs in Cloud Run
   ```bash
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chat-ui" --limit=50
   ```

3. Verify your environment variables are set correctly

4. Ensure your service account has the necessary permissions

5. Check that your agent is deployed correctly and accessible

## Why Cloud Build?

Using Cloud Build for deployment offers several advantages:

- **Automation**: Fully automates the build, test, and deployment process
- **Consistency**: Ensures consistent build environments and results
- **Speed**: Optimized builds with caching and parallel execution
- **Integration**: Seamlessly integrates with other Google Cloud services
- **Monitoring**: Built-in logging and monitoring capabilities
- **Scalability**: Automatically scales to handle your build needs
- **Security**: Runs in isolated environments with IAM controls

## Conclusion

You now have a production-ready chat interface for your Agent Engine agents. This setup can be customized and extended to meet your specific requirements. By using Cloud Build for deployment, you've implemented a modern CI/CD pipeline that will make future updates and maintenance easier and more reliable.
