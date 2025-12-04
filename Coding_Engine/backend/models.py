from pydantic import BaseModel
from typing import List, Optional

class File(BaseModel):
    content: str

class ExecuteRequest(BaseModel):
    language: str
    version: str
    files: List[File]
    stdin: Optional[str] = ""
    args: Optional[List[str]] = []
    compile_timeout: Optional[int] = 10000
    run_timeout: Optional[int] = 3000
    compile_memory_limit: Optional[int] = -1
    run_memory_limit: Optional[int] = -1

class ExecuteResponse(BaseModel):
    run: dict
    compile: Optional[dict] = None
    language: str
    version: str
