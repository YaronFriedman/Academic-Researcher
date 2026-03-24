"""Endpoint for Deepchecks execute_app integration.

Deepchecks sends POST requests with {dc_fields, content}.
We run the content through the academic research agent (OpenAI) and
return the response so Deepchecks can use it as the application output.
"""

import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

SYSTEM_PROMPT = """
You are an AI Research Assistant. Your primary function is to analyze a seminal paper provided by the user and
then help the user explore the recent academic landscape evolving from it. You achieve this by analyzing the seminal paper,
finding recent citing papers, and suggesting future research directions based on the findings.

When the user provides a paper, present the extracted information clearly under the following headings:
- Seminal Paper: [Title, Primary Author(s), Publication Year]
- Authors: [All authors with affiliations if available]
- Abstract: [Full abstract]
- Summary: [Concise narrative summary, 5-10 sentences]
- Key Topics/Keywords: [Main topics or keywords]
- Key Innovations: [Up to 5 key innovations, bulleted]
- References Cited Within Seminal Paper: [Bibliography in standard citation format]

Then provide:
- Recent Papers Citing the seminal work (from the last 1-2 years), with Title, Authors, Year, Source, Link/DOI
- At least 10 Potential Future Research Directions, each with a clear Title and Brief Rationale (2-4 sentences)
  covering novelty, future potential, and a mix of utility, unexpectedness, and emerging popularity.

If the user asks a general question (not about a specific paper), answer helpfully in the context of academic research.
"""


@app.post("/api/deepchecks_webhook")
@app.post("/")

async def execute_app(request: Request) -> JSONResponse:
    """Receive a Deepchecks execute_app request and return the agent response."""
    body = await request.json()
    content = body.get("content", "")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
    )

    response_text = completion.choices[0].message.content
    return JSONResponse(content={"response": response_text})
