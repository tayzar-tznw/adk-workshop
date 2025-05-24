#!/usr/bin/env python3
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example script demonstrating how to deploy and interact with the Weather Agent."""

import os
import sys
import time
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

# Add the parent directory to the path so we can import the weather_agent package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from weather_agent.agent import root_agent


def check_environment():
    """Check if the required environment variables are set."""
    required_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION",
        "GOOGLE_CLOUD_STORAGE_BUCKET",
        "GOOGLE_API_KEY",
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: The following required environment variables are not set:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        return False
    
    return True


def deploy_agent():
    """Deploy the Weather Agent to Google Cloud."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    
    print(f"Deploying Weather Agent to project: {project_id}")
    print(f"Location: {location}")
    print(f"Bucket: {bucket}")
    
    # Initialize Vertex AI
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket}",
    )
    
    # Create the AdkApp
    app = AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )
    
    # Deploy the agent
    print("Creating remote agent... (this may take a few minutes)")
    remote_agent = agent_engines.create(
        app,
        requirements=[
            "google-adk (==1.1.0)",
            "google-cloud-aiplatform[agent_engines] (==1.95.0)",
            "google-genai (>=1.9.0,<2.0.0)",
            "pydantic (>=2.10.6,<3.0.0)",
            "absl-py (>=2.2.1,<3.0.0)",
            "python-dotenv (>=1.0.1,<2.0.0)",
            "litellm (>=1.0.0,<2.0.0)",
        ],
        extra_packages=[
            "./weather_agent",  # The main package
        ],
    )
    
    resource_name = remote_agent.resource_name
    print(f"Successfully deployed agent: {resource_name}")
    return resource_name


def test_agent(resource_name):
    """Test the deployed agent with a few queries."""
    print(f"\nTesting agent: {resource_name}")
    
    # Get the remote agent
    remote_agent = agent_engines.get(resource_name)
    
    # Create a session with initial state
    initial_state = {"user_preference_temperature_unit": "Celsius"}
    session = remote_agent.create_session(
        user_id="example_user",
        state=initial_state
    )
    session_id = session["id"]
    
    # Test queries
    test_queries = [
        "Hello there!",
        "What's the weather in London?",
        "What about New York?",
        "Thanks, goodbye!"
    ]
    
    for query in test_queries:
        print(f"\n>>> User: {query}")
        print("<<< Agent: ", end="")
        
        # Stream the response
        for event in remote_agent.stream_query(
            user_id="example_user",
            session_id=session_id,
            message=query,
        ):

            # Attempt to parse the event as a dictionary based on observed log structure
            if isinstance(event, dict):
                content = event.get("content")
                if isinstance(content, dict):
                    parts = content.get("parts")
                    if isinstance(parts, list):
                        for part_item in parts:
                            if isinstance(part_item, dict):
                                text_content = part_item.get("text")
                                if isinstance(text_content, str) and text_content:
                                    print(text_content, end="")
            # Add back the original checks as a fallback, in case some events are objects
            # This is less likely given the logs, but provides a safety net.
            elif hasattr(event, "text") and event.text:
                print(event.text, end="")
            elif hasattr(event, "content") and event.content and \
                 hasattr(event.content, "parts") and event.content.parts:
                for part_item_obj in event.content.parts:
                    if hasattr(part_item_obj, "text") and part_item_obj.text:
                        print(part_item_obj.text, end="")
        
        print()  # New line after response
        time.sleep(1)  # Small delay between queries
    
    print("\nTest completed successfully!")


def delete_agent(resource_name):
    """Delete the deployed agent."""
    print(f"\nDeleting agent: {resource_name}")
    
    # Get the remote agent
    remote_agent = agent_engines.get(resource_name)
    
    # Delete the agent
    remote_agent.delete(force=True)
    print("Agent deleted successfully!")


def main():
    """Main function to demonstrate deployment workflow."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required environment variables are set
    if not check_environment():
        return
    
    try:
        # Deploy the agent
        # resource_name = deploy_agent()
        resource_name = "1287686445800095744"
        
        # Test the agent
        test_agent(resource_name)
        
        # Ask if the user wants to delete the agent
        delete_choice = input("\nDo you want to delete the deployed agent? (y/n): ")
        if delete_choice.lower() == 'y':
            delete_agent(resource_name)
        else:
            print(f"\nKeeping agent deployed. Resource name: {resource_name}")
            print("You can delete it later using:")
            print(f"python -m weather_agent.deployment.deploy --delete --resource_id={resource_name}")
    
    except Exception as e:
        print(f"Error: {e}")
        print("Deployment failed. Please check your environment variables and permissions.")


if __name__ == "__main__":
    main()