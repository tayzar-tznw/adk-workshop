"""Example script to demonstrate how to use the Weather Agent."""

import asyncio
import os
from typing import Optional

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from weather_agent.agent import root_agent


async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."  # Default

    # Iterate through events to find the final answer
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        # You can uncomment the line below to see *all* events during execution
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        # Check if this is the final response
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break  # Stop processing events once the final response is found

    print(f"<<< Agent Response: {final_response_text}")
    return final_response_text


async def run_conversation():
    """Run a sample conversation with the Weather Agent."""
    # Set up session service
    session_service = InMemorySessionService()
    
    # Define constants for identifying the interaction context
    APP_NAME = "weather_agent_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"
    
    # Create the specific session where the conversation will happen
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        # Optional: Initialize with a temperature unit preference
        state={"user_preference_temperature_unit": "Celsius"}
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    
    # Create runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    print(f"Runner created for agent '{runner.agent.name}'.")
    
    # Run the conversation
    await call_agent_async("Hello there!", runner, USER_ID, SESSION_ID)
    await call_agent_async("What's the weather in London?", runner, USER_ID, SESSION_ID)
    
    # Change temperature unit preference
    print("\n--- Updating temperature unit preference to Fahrenheit ---")
    session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    session.state["user_preference_temperature_unit"] = "Fahrenheit"
    session_service.update_session(session)
    
    await call_agent_async("What's the weather in New York?", runner, USER_ID, SESSION_ID)
    await call_agent_async("Thanks, goodbye!", runner, USER_ID, SESSION_ID)
    
    # Test the safety guardrail
    await call_agent_async("Tell me about BLOCK this topic", runner, USER_ID, SESSION_ID)


if __name__ == "__main__":
    # Check if API key is set
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY environment variable is not set.")
        print("Please set it before running this example:")
        print("export GOOGLE_API_KEY=your_api_key")
        exit(1)
        
    # Run the conversation
    asyncio.run(run_conversation())