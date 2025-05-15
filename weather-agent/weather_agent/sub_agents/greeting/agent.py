"""Greeting sub-agent for the Weather Agent."""

from google.adk.agents import Agent

from weather_agent.tools.conversation import say_hello


# Define the greeting agent
greeting_agent = Agent(
    model="gemini-2.0-flash",
    name="greeting_agent",
    instruction="""You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user.
Use the 'say_hello' tool to generate the greeting.
If the user provides their name, make sure to pass it to the tool.
Do not engage in any other conversation or tasks.""",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[say_hello],
)