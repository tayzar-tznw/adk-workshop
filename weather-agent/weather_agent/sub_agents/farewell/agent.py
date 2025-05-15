"""Farewell sub-agent for the Weather Agent."""

from google.adk.agents import Agent

from weather_agent.tools.conversation import say_goodbye


# Define the farewell agent
farewell_agent = Agent(
    model="gemini-2.0-flash",
    name="farewell_agent",
    instruction="""You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message.
Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation
(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you').
Do not perform any other actions.""",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)