# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_websearch_agent for finding research papers using search tools."""

import json
import os

import requests
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool

from . import prompt

MODEL = LiteLlm(model="openai/gpt-4o")


def web_search(query: str) -> str:
    """Search the web using Serper API and return results.

    Args:
        query: The search query string.

    Returns:
        A JSON string containing search results with title, link, and snippet.
    """
    api_key = os.environ.get("SERPER_API_KEY", "")
    if not api_key:
        return json.dumps({"error": "SERPER_API_KEY must be set in .env"})

    resp = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={"q": query, "num": 10},
        timeout=15,
    )
    resp.raise_for_status()
    items = resp.json().get("organic", [])
    results = [{"title": i["title"], "link": i["link"], "snippet": i.get("snippet", "")} for i in items]
    return json.dumps(results)


academic_websearch_agent = Agent(
    model=MODEL,
    name="academic_websearch_agent",
    instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT,
    output_key="recent_citing_papers",
    tools=[FunctionTool(web_search)],
)
