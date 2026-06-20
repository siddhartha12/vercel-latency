from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import json
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

with open("q-vercel-latency.json", "r") as f:
    telemetry = json.load(f)

class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: int

@app.post("/")
def analytics(req: AnalyticsRequest):

    result = {}

    for region in req.regions:

        rows = [
            row
            for row in telemetry
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

        result[region] = {
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
                1
                for x in latencies
                if x > req.threshold_ms
            )
        }

    return result