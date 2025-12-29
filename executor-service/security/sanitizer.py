"""Code sanitization and validation"""
import re
from typing import Tuple
from executor_service.config import (
    BLOCKED_PATTERNS, BLOCKED_NETWORK_PATTERNS, 
    MAX_CODE_LENGTH, MAX_INPUT_SIZE, MAX_OUTPUT_SIZE
)
from executor_service.models import TestCase

def sanitize_code(code: str, language: str) -> Tuple[bool, str]:
    """Sanitize code to block dangerous operations"""
    if not code:
        return False, "Empty code"
    
    if len(code) > MAX_CODE_LENGTH:
        return False, f"Code too long (max {MAX_CODE_LENGTH} bytes)"
    
    patterns = BLOCKED_PATTERNS.get(language, [])
    for pattern in patterns:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return False, f"Blocked pattern detected: {pattern}"
    
    for pattern in BLOCKED_NETWORK_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return False, f"Network operations not allowed: {pattern}"
    
    return True, ""

def validate_test_case(test_case: TestCase) -> Tuple[bool, str]:
    """Validate test case input/output sizes - SECURITY FIX: Added input validation"""
    if len(test_case.input) > MAX_INPUT_SIZE:
        return False, f"Input too large (max {MAX_INPUT_SIZE} bytes)"
    if len(test_case.expected_output) > MAX_OUTPUT_SIZE:
        return False, f"Expected output too large (max {MAX_OUTPUT_SIZE} bytes)"
    return True, ""

