from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import numpy as np
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Access-Control-Allow-Origin"],
)

json_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "q-vercel-latency.json"
)

with open(json_path, "r") as f:
    telemetry = json.load(f)


class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: int


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*"
}


@app.get("/")
def health():
    return JSONResponse(
        content={"status": "ok"},
        headers=CORS_HEADERS
    )


@app.options("/")
def options_handler():
    return JSONResponse(
        content={},
        headers=CORS_HEADERS
    )


@app.post("/")
def analytics(req: AnalyticsRequest):

    result = {"regions": {}}

    for region in req.regions:

        rows = [
            row for row in telemetry
            if row["region"] == region
        ]

        latencies = [
            row["latency_ms"]
            for row in rows
        ]

        uptimes = [
            row["uptime_pct"]
            for row in rows
        ]

        rresult["regions"][region] = {
            "avg_latency": round(
                sum(latencies) / len(latencies),
                2
            ),
            "p95_latency": round(
                float(np.percentile(latencies, 95)),
                2
            ),
            "avg_uptime": round(
                sum(uptimes) / len(uptimes),
                2
            ),
            "breaches": sum(
                1 for x in latencies
                if x > req.threshold_ms
            )
        }

    return JSONResponse(
        content=result,
        headers=CORS_HEADERS
    )
