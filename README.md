### Sample Automated PR Workflow
Demonstrates a simple workflow from ingestion to PR using Agent Development Kit (ADK).

### Features
* A fastapi webhook endpoint to receive Github Issues.
* Implements an In-memory `TaskQueue` & an async background worker loop.
* Uses Google Agent Development Kit for routing agent LLM logic.
* Tool Calling & Multi Agent Delegation (LiteLLM & Groq for diverse model access).

### System Design
```mermaid
graph TD
    GH[GitHub Webhook: Issue Event] -->|POST /webhookpr| API[FastAPI App]
    API -->|Add Task| Q[In-Memory TaskQueue]
    
    subgraph Background Process
        Worker[Async Worker Loop]
        Q -->|Dequeue| Worker
        Worker -->|Run Async| Root[Root Agent: CapaRuleGenerator]
    end
    
    subgraph Google ADK Ecosystem
        Root -->|Tool| ReadFmt[read_format.py]
        Root -->|Sub-Agent| Search[SearchToolAgent: Gemini]
        Root -->|Tool| PR[make_pr.py]
    end
    
    PR -->|Automated PR| GH_PR[GitHub: capa-rules Repo]

### CICD Workflow Deployment