from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from tools import read_format, make_pr

MODEL_GROQ_OPENAI = "groq/openai/gpt-oss-120b"
MODEL_GROQ_KIMI = "groq/moonshotai/kimi-k2-instruct-0905"


root_agent = Agent(
    model=LiteLlm(model=MODEL_GROQ_OPENAI),
    name="CapaRuleGenerator",
    description="An expert malware analyst making capa-rules",
    instruction="You are an expert malware analyst and also possess highly accurate skills in making capa-rules."
    "When given a github issue for a capa-rule, use 'read_format_md' tool to understand the YAML schema and rule information."
    "format.md file is only to understand each and every rule definition and how its used. It is just a REFERENCE for you to make a valid yml rule"
    "Understanding the github issue is important, and then generate yml rule file after relying on your internal knowledge and the context gathered from the issue and any links. "
    "IMPORTANT: Always generate a safe, lowercase branch name without spaces, and ensure the file name ends in .yml. "
    "Then, generate the appropriate rule and use 'make_pr' to make a PR with the appropriate file name (DO NOT ASK PERMISSIONS)",    
    tools=[read_format.read_format_md, make_pr.post_pr]
)
