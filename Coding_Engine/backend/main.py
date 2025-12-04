from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ExecuteRequest, ExecuteResponse
from executor import execute_code_in_session
import os

app = FastAPI(title="Coding Engine Backend")

# CORS Configuration
# Allow all origins for now to support local dev and various deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Azure Dynamic Sessions Backend"}

@app.get("/api/v2/runtimes")
def get_runtimes():
    """
    Mock Piston endpoint to return supported languages.
    For Dynamic Sessions (Python), we return Python.
    """
    return [
        {
            "language": "python",
            "version": "3.11",
            "aliases": ["py", "python3"],
            "runtime": "cpython"
        }
    ]

@app.post("/api/v2/execute", response_model=ExecuteResponse)
def execute_code(request: ExecuteRequest):
    """
    Executes code via Azure Dynamic Sessions.
    """
    return execute_code_in_session(request)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
