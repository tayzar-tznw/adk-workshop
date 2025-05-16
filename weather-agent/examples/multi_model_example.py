"""Example script to demonstrate how to use the Weather Agent with different LLMs."""

import asyncio
import os
from typing import Optional

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from weather_agent.prompt import ROOT_AGENT_INSTR
from weather_agent.sub_agents.greeting.agent import greeting_agent
from weather_agent.sub_agents.farewell.agent import farewell_agent
from weather_agent.tools.weather import get_weather_stateful


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


async def run_multi_model_example():
    """Run a sample conversation with the Weather Agent using different LLMs."""
    # Check if API keys are set
    missing_keys = []
    if not os.environ.get("GOOGLE_API_KEY"):
        missing_keys.append("GOOGLE_API_KEY")
    if not os.environ.get("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        missing_keys.append("ANTHROPIC_API_KEY")
    
    if missing_keys:
        print(f"Warning: The following API keys are not set: {', '.join(missing_keys)}")
        print("Some examples may not work without these keys.")
        print("Please set them before running this example:")
        for key in missing_keys:
            print(f"export {key}=your_{key.lower()}")
    
    # Define model constants
    MODEL_GEMINI = "gemini-2.0-flash"
    MODEL_GPT = "openai/gpt-4o"
    MODEL_CLAUDE = "anthropic/claude-3-sonnet-20240229"
    
    # Create agents with different models
    try:
        # Gemini agent (default)
        gemini_agent = Agent(
            model=MODEL_GEMINI,
            name="weather_agent_gemini",
            description="Weather agent using Gemini",
            instruction=ROOT_AGENT_INSTR,
            tools=[get_weather_stateful],
            sub_agents=[greeting_agent, farewell_agent],
            output_key="last_weather_report"
        )
        
        # GPT agent
        gpt_agent = Agent(
            model=LiteLlm(model=MODEL_GPT),
            name="weather_agent_gpt",
            description="Weather agent using GPT",
            instruction=ROOT_AGENT_INSTR,
            tools=[get_weather_stateful],
            sub_agents=[greeting_agent, farewell_agent],
            output_key="last_weather_report"
        )
        
        # Claude agent
        claude_agent = Agent(
            model=LiteLlm(model=MODEL_CLAUDE),
            name="weather_agent_claude",
            description="Weather agent using Claude",
            instruction=ROOT_AGENT_INSTR,
            tools=[get_weather_stateful],
            sub_agents=[greeting_agent, farewell_agent],
            output_key="last_weather_report"
        )
        
        # Set up session service
        session_service = InMemorySessionService()
        
        # Define constants for identifying the interaction context
        APP_NAME = "weather_agent_multi_model_app"
        USER_ID = "user_1"
        
        # Test each agent
        agents = [
            {"agent": gemini_agent, "name": "Gemini", "session_id": "session_gemini"},
            {"agent": gpt_agent, "name": "GPT", "session_id": "session_gpt"},
            {"agent": claude_agent, "name": "Claude", "session_id": "session_claude"}
        ]
        
        for agent_info in agents:
            agent = agent_info["agent"]
            name = agent_info["name"]
            session_id = agent_info["session_id"]
            
            try:
                print(f"\n{'='*50}")
                print(f"Testing {name} Agent")
                print(f"{'='*50}")
                
                # Create session
                session = session_service.create_session(
                    app_name=APP_NAME,
                    user_id=USER_ID,
                    session_id=session_id,
                    state={"user_preference_temperature_unit": "Celsius"}
                )
                
                # Create runner
                runner = Runner(
                    agent=agent,
                    app_name=APP_NAME,
                    session_service=session_service
                )
                
                # Run a simple conversation
                await call_agent_async("Hello there!", runner, USER_ID, session_id)
                await call_agent_async("What's the weather in London?", runner, USER_ID, session_id)
                
            except Exception as e:
                print(f"Error testing {name} agent: {e}")
                print(f"This might be due to missing API keys or configuration issues.")
    
    except Exception as e:
        print(f"Error setting up agents: {e}")


if __name__ == "__main__":
    asyncio.run(run_multi_model_example())