"""Health-check / root endpoint for the Vercel deployment."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/api")
async def root() -> JSONResponse:
    return JSONResponse(
        content={
            "service": "academic-research",
            "status": "ok",
            "endpoints": {
                "POST /api/deepchecks_webhook": "Receive Deepchecks webhook data",
                "GET  /api/deepchecks_webhook": "View latest Deepchecks payload",
            },
        }
    )
