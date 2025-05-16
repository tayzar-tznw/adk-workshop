"""Weather tools for the Weather Agent."""

from google.adk.tools.tool_context import ToolContext


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather called for city: {city} ---")  # Log tool execution
    city_normalized = city.lower().replace(" ", "")  # Basic normalization

    # Mock weather data
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}


def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather, converts temp unit based on session state.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").
        tool_context (ToolContext): The ADK tool context providing access to session state.

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather_stateful called for {city} ---")

    # --- Read preference from state ---
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius")  # Default to Celsius
    print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    city_normalized = city.lower().replace(" ", "")

    # Mock weather data (always stored in Celsius internally)
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }

    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # Format temperature based on state preference
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32  # Calculate Fahrenheit
            temp_unit = "°F"
        else:  # Default to Celsius
            temp_value = temp_c
            temp_unit = "°C"

        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        result = {"status": "success", "report": report}
        print(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")

        # Example of writing back to state (optional for this tool)
        tool_context.state["last_city_checked_stateful"] = city
        print(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")

        return result
    else:
        # Handle city not found
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        print(f"--- Tool: City '{city}' not found. ---")
        return {"status": "error", "error_message": error_msg}


def set_temperature_preference(unit: str, tool_context: ToolContext) -> dict:
    """Sets the user's preferred temperature unit (Celsius or Fahrenheit).

    Args:
        unit (str): The preferred temperature unit ("Celsius" or "Fahrenheit").
        tool_context (ToolContext): The ADK tool context providing access to session state.

    Returns:
        dict: A dictionary confirming the action or reporting an error.
    """
    print(f"--- Tool: set_temperature_preference called with unit: {unit} ---")
    normalized_unit = unit.strip().capitalize()

    if normalized_unit in ["Celsius", "Fahrenheit"]:
        tool_context.state["user_preference_temperature_unit"] = normalized_unit
        print(f"--- Tool: Updated state 'user_preference_temperature_unit': {normalized_unit} ---")
        return {"status": "success", "message": f"Temperature preference set to {normalized_unit}."}
    else:
        error_msg = f"Invalid temperature unit '{unit}'. Please specify 'Celsius' or 'Fahrenheit'."
        print(f"--- Tool: Invalid unit provided: {unit} ---")
        return {"status": "error", "error_message": error_msg}