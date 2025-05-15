"""Main agent definition for the Weather Agent."""

from google.adk.agents import Agent

from weather_agent.prompt import ROOT_AGENT_INSTR
from weather_agent.shared_libraries.callbacks import block_keyword_guardrail
from weather_agent.sub_agents.greeting.agent import greeting_agent
from weather_agent.sub_agents.farewell.agent import farewell_agent
from weather_agent.tools.weather import get_weather_stateful, set_temperature_preference


# Define the root agent
root_agent = Agent(
    model="gemini-2.0-flash",
    name="weather_agent",
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction=ROOT_AGENT_INSTR,
    tools=[get_weather_stateful, set_temperature_preference],
    sub_agents=[greeting_agent, farewell_agent],
    before_model_callback=block_keyword_guardrail,
    output_key="last_weather_report"
)