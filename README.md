# Academic Research Agent

A multi-agent application built with [Google ADK](https://github.com/google/adk-samples) that helps researchers analyze seminal papers, find related literature, and discover new research directions.

## What it does

Given a seminal paper (as a PDF, link, or text description), the agent:

1. **Analyzes** the paper's key contributions, methodology, and references
2. **Searches the web** for recent papers that cite or relate to the seminal work
3. **Suggests new research directions** based on the paper and current literature

## Architecture

The app uses a coordinator/sub-agent pattern:

- **academic_coordinator** — orchestrates the workflow, interacts with the user, and delegates tasks
- **academic_websearch_agent** — searches the web via Serper API for recent citing papers
- **academic_newresearch_agent** — generates proposals for new research directions

All agents use OpenAI GPT-4o via LiteLLM integration.

## Observability

Traces are exported to [Deepchecks](https://deepchecks.com/) via OpenTelemetry for monitoring agent performance, token usage, and session tracking.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file with:
   ```
   OPENAI_API_KEY="your-openai-key"
   SERPER_API_KEY="your-serper-key"
   DEEPCHECKS_HOST="https://your-instance.deepchecks.com/"
   DEEPCHECKS_API_KEY="your-deepchecks-key"
   DEEPCHECKS_APP_NAME="your-app-name"
   DEEPCHECKS_VERSION_NAME="v1"
   ```

3. Run the agent:
   ```bash
   uv run adk web
   ```
   Then open `http://localhost:8000` and select `academic_research` from the agent dropdown.
