from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import ToolContext
from tools import read_format, make_pr

MODEL_GROQ_OPENAI = "groq/openai/gpt-oss-120b"
MODEL_GROQ_KIMI = "groq/moonshotai/kimi-k2-instruct-0905"


root_agent = Agent(
    model=LiteLlm(model=MODEL_GROQ_OPENAI),
    name="CapaRuleGenerator",
    description="An expert malware analyst making capa-rules",
    instruction="You are an expert malware analyst and also possess highly accurate skills in making capa-rules."
    "When given a github issue for a capa-rule, use 'read_format_md' tool to understand the YAML schema and rule information."
    "Then, generate the appropriate rule and use 'make_pr' to make a PR with the appropriate file name",
    tools=[read_format.read_format_md, make_pr.post_pr]
)
