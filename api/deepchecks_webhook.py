"""Endpoint to receive POST requests from Deepchecks."""

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# In-memory storage for the latest Deepchecks payload.
# NOTE: Vercel serverless functions are stateless — this variable resets
# between cold starts. For persistent storage, use Vercel KV, Redis, or
# a database. For demo / webhook-inspection purposes this is sufficient.
deepchecks_data: dict[str, Any] = {
    "last_received_at": None,
    "payload": None,
}


@app.post("/api/deepchecks_webhook")
async def receive_deepchecks(request: Request) -> JSONResponse:
    """Receive a POST request from Deepchecks and store the payload."""
    body = await request.json()
    deepchecks_data["payload"] = body
    deepchecks_data["last_received_at"] = datetime.now(timezone.utc).isoformat()
    return JSONResponse(
        content={"status": "ok", "received_at": deepchecks_data["last_received_at"]},
        status_code=200,
    )


@app.get("/api/deepchecks_webhook")
async def get_deepchecks_data() -> JSONResponse:
    """Return the latest stored Deepchecks payload (for debugging)."""
    return JSONResponse(content=deepchecks_data)
