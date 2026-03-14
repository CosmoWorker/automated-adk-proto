from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from typing import Optional
from google.adk.tools import ToolContext

MODEL_GROQ_OPENAI = "groq/openai/gpt-oss-120b"
MODEL_GROQ_KIMI = "groq/moonshotai/kimi-k2-instruct-0905"


def get_normalized_weather(city: str, tool_context: ToolContext) -> dict:
    preferred_unit = tool_context.state.get("user_preferred_temp_unit", "Celsius")
    normalized_city = city.lower().replace(" ", "")
    mock_weather = {
        "newyork": {"condition": "dark", "temp": 6},
        "london": {"condition": "sunny", "temp": 18},
        "tokyo": {"condition": "cloudy", "temp": 26},
    }

    if normalized_city in mock_weather:
        info = mock_weather[normalized_city]
        if preferred_unit == "fahrenheit":
            temp_val = (info["temp"] * (9 / 5)) + 32
            temp_unit = "°F"
        else:
            temp_val = info["temp"]
            temp_unit = "°C"

        report = f"The weather in {city} is {info['condition']} with a temperature of {temp_val}{temp_unit}"
        res_report = {"status": "success", "report": report}

        return res_report
    else:
        return {
            "status": "error",
            "report": f"sorry, I don't have weather information for {city}",
        }


def get_current_time(city: str) -> dict:
    return {"city": city, "time": "20:30 PM"}


def set_temp_unit(unit: str, tool_context: ToolContext):
    tool_context.state["user_preferred_temp_unit"] = unit

    return {"status": "success", "data": f"Temperature unit set to {unit}"}


def greet_hello(name: Optional[str]) -> str:
    if name:
        greeting = f"Hello, {name}"
    else:
        greeting = "Hello there!"

    return greeting


def greet_farewell() -> str:
    return "Goodbye! Have a great day"


hello_agent = Agent(
    model=LiteLlm(model=MODEL_GROQ_KIMI),
    name="hello_agent",
    description="Handles simple greetings by saying hello using 'greet_hello' tool",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
    "Use the 'greet_hello' tool to generate the greeting. "
    "If the user provides their name, **make sure you to pass it to the tool.** "
    "Do not engage in any other conversation or tasks.",
    tools=[greet_hello],
)


farewell_agent = Agent(
    model=LiteLlm(model=MODEL_GROQ_KIMI),
    name="farewell_agent",
    description="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
    "Use the 'greet_farewell' tool when the user indicates they are leaving or ending the conversation "
    "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you', etc.). "
    "Do not perform any other actions.",
    instruction="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[greet_farewell],
)

root_agent = Agent(
    model=LiteLlm(model=MODEL_GROQ_OPENAI),
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Your helpful assistant answering user queries"
    "When the user asks for the weather in a specific city"
    "use 'get_normalized_weather' tool to find the weather info, use 'set_temp_unit' to set user preference early on if user prefers a particular temperature unit"
    "If the user asks about time use 'get_current_time' tool"
    "Delegate simple greetings to 'hello_agent' and farewells to 'farewell_agent'"
    "If the tool is returns error, inform accordingly"
    "If tool is successfuly, report it accordingly",
    sub_agents=[hello_agent, farewell_agent],
    tools=[get_current_time, get_normalized_weather, set_temp_unit],
    output_key="last_weather_report",
)
