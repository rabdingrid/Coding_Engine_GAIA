"""Pydantic models for request/response"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TestCase(BaseModel):
    id: str
    input: str
    expected_output: str

class RunRequest(BaseModel):
    """Request for /run endpoint - code + boilerplate + sample test cases"""
    language: str = Field(..., description="Programming language: python, java, cpp, javascript, csharp")
    code: str = Field(..., description="Complete code (user code + boilerplate merged)")
    sample_test_cases: List[TestCase] = Field(..., description="Sample test cases to run")
    user_id: Optional[str] = None
    question_id: Optional[str] = None
    timeout: Optional[int] = None

class RunAllRequest(BaseModel):
    """Request for /runall endpoint - code + boilerplate + all test cases (except sample)"""
    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="Complete code (user code + boilerplate merged)")
    test_cases: List[TestCase] = Field(..., description="All test cases (excluding sample)")
    sample_test_cases: List[TestCase] = Field(default=[], description="Sample test cases (for reference, not executed)")
    user_id: Optional[str] = None
    question_id: Optional[str] = None
    timeout: Optional[int] = None

class SubmitRequest(BaseModel):
    """Request for /submit endpoint - code + boilerplate + all test cases, saves to DB"""
    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="Complete code (user code + boilerplate merged)")
    test_cases: List[TestCase] = Field(..., description="All test cases")
    sample_test_cases: List[TestCase] = Field(default=[], description="Sample test cases (for reference)")
    user_id: str = Field(..., description="User/Candidate ID (required for submission)")
    question_id: str = Field(..., description="Question ID (required for submission)")
    candidate_id: Optional[str] = None
    timeout: Optional[int] = None

class TestResult(BaseModel):
    test_case_id: str
    test_case_number: int
    input: str
    expected_output: str
    actual_output: str
    error: Optional[str] = None
    status: str  # 'passed', 'failed', 'error', 'tle', 'mle', 'syntax_error'
    passed: bool
    execution_time_ms: int
    cpu_usage_percent: float
    memory_usage_bytes: int

class ExecutionResponse(BaseModel):
    execution_id: str
    summary: Dict[str, Any]
    test_results: List[TestResult]
    metadata: Dict[str, Any]
    timestamp: str

