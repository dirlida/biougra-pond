from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import os, json

app = FastAPI(title="fly-witness")

CHAIN_PATH = os.path.join(os.path.dirname(__file__), "chain.json")

@app.get("/")
def root():
    return {"status": "witness live", "chain": os.path.exists(CHAIN_PATH)}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/chain")
def chain():
    if not os.path.exists(CHAIN_PATH):
        return JSONResponse({"error": "chain.json not found"}, status_code=404)
    return FileResponse(CHAIN_PATH)

@app.get("/chain.json")
def chain_json():
    return chain()

@app.get("/stats")
def stats():
    if not os.path.exists(CHAIN_PATH):
        return {"size": 0}
    try:
        with open(CHAIN_PATH) as f:
            data = json.load(f)
        return {"entries": len(data) if isinstance(data, list) else 1, "size_bytes": os.path.getsize(CHAIN_PATH)}
    except:
        return {"size_bytes": os.path.getsize(CHAIN_PATH)}
