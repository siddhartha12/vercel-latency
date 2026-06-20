```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"status": "alive"}

@app.options("/")
def options_root():
    return {}

class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: int

@app.post("/")
def analytics(req: AnalyticsRequest):
    return {
        "regions": req.regions,
        "threshold": req.threshold_ms
    }
```
