#!/usr/bin/env python3
"""
Session Pool Code Execution Test Suite

Tests the complete flow: Backend API → Azure Session Pool → Code Execution → Response

Usage:
    # Local testing (fallback mode)
    USE_LOCAL_EXECUTOR=true python test_session_pool.py

    # Test against deployed backend
    python test_session_pool.py --endpoint http://localhost:8000

    # Full test suite with all test cases
    python test_session_pool.py --full
"""

import requests
import json
import time
import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Test configuration
TEST_CASES_DIR = Path(__file__).parent / "test_cases"
DEFAULT_ENDPOINT = "http://localhost:8000"
TIMEOUT = 30  # seconds

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class TestResult:
    """Represents the result of a single test"""
    def __init__(self, name: str, passed: bool, message: str = "", duration: float = 0.0):
        self.name = name
        self.passed = passed
        self.message = message
        self.duration = duration

class SessionPoolTester:
    """Test suite for session pool code execution"""
    
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT):
        self.endpoint = endpoint.rstrip('/')
        self.results: List[TestResult] = []
        
    def print_header(self, text: str):
        """Print a formatted header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    def print_test(self, name: str, status: str, message: str = "", duration: float = 0.0):
        """Print test result"""
        status_color = Colors.GREEN if status == "PASS" else Colors.RED
        status_symbol = "✓" if status == "PASS" else "✗"
        duration_str = f" ({duration:.2f}s)" if duration > 0 else ""
        
        print(f"{status_color}{status_symbol} {name}{duration_str}{Colors.RESET}")
        if message:
            print(f"   {message}")
    
    def execute_code(self, code: str, language: str = "python", version: str = "3.11", 
                     stdin: str = "") -> Dict:
        """Execute code via the backend API"""
        url = f"{self.endpoint}/api/v2/execute"
        
        payload = {
            "language": language,
            "version": version,
            "files": [{"content": code}],
            "stdin": stdin,
            "args": [],
            "compile_timeout": 10000,
            "run_timeout": 3000
        }
        
        try:
            response = requests.post(url, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "run": {
                    "stdout": "",
                    "stderr": f"Request failed: {str(e)}",
                    "code": 1
                }
            }
    
    def test_basic_execution(self) -> List[TestResult]:
        """Test 1: Basic code execution"""
        self.print_header("Test 1: Basic Code Execution")
        results = []
        
        # Test 1.1: Simple print
        start = time.time()
        response = self.execute_code('print("Hello, World!")')
        duration = time.time() - start
        
        passed = (
            response.get("run", {}).get("stdout", "").strip() == "Hello, World!" and
            response.get("run", {}).get("code", 1) == 0
        )
        results.append(TestResult("1.1: Simple print", passed, 
                                 f"Output: {response.get('run', {}).get('stdout', '')}", duration))
        self.print_test("1.1: Simple print", "PASS" if passed else "FAIL",
                       response.get("run", {}).get("stdout", ""), duration)
        
        # Test 1.2: Arithmetic
        start = time.time()
        response = self.execute_code('print(2 + 2)')
        duration = time.time() - start
        
        passed = (
            response.get("run", {}).get("stdout", "").strip() == "4" and
            response.get("run", {}).get("code", 1) == 0
        )
        results.append(TestResult("1.2: Arithmetic", passed,
                                 f"Output: {response.get('run', {}).get('stdout', '')}", duration))
        self.print_test("1.2: Arithmetic", "PASS" if passed else "FAIL",
                       response.get("run", {}).get("stdout", ""), duration)
        
        # Test 1.3: Variables
        start = time.time()
        response = self.execute_code('x = 10; print(x * 2)')
        duration = time.time() - start
        
        passed = (
            response.get("run", {}).get("stdout", "").strip() == "20" and
            response.get("run", {}).get("code", 1) == 0
        )
        results.append(TestResult("1.3: Variables", passed,
                                 f"Output: {response.get('run', {}).get('stdout', '')}", duration))
        self.print_test("1.3: Variables", "PASS" if passed else "FAIL",
                       response.get("run", {}).get("stdout", ""), duration)
        
        return results
    
    def test_input_output(self) -> List[TestResult]:
        """Test 2: Input/Output handling"""
        self.print_header("Test 2: Input/Output Handling")
        results = []
        
        # Test 2.1: Single input
        start = time.time()
        code = 'name = input(); print(f"Hello, {name}")'
        response = self.execute_code(code, stdin="Alice")
        duration = time.time() - start
        
        passed = (
            "Hello, Alice" in response.get("run", {}).get("stdout", "") and
            response.get("run", {}).get("code", 1) == 0
        )
        results.append(TestResult("2.1: Single input", passed,
                                 f"Output: {response.get('run', {}).get('stdout', '')}", duration))
        self.print_test("2.1: Single input", "PASS" if passed else "FAIL",
                       response.get("run", {}).get("stdout", ""), duration)
        
        # Test 2.2: Multiple inputs
        start = time.time()
        code = 'a = int(input()); b = int(input()); print(a + b)'
        response = self.execute_code(code, stdin="5\n3")
        duration = time.time() - start
        
        passed = (
            response.get("run", {}).get("stdout", "").strip() == "8" and
            response.get("run", {}).get("code", 1) == 0
        )
        results.append(TestResult("2.2: Multiple inputs", passed,
                                 f"Output: {response.get('run', {}).get('stdout', '')}", duration))
        self.print_test("2.2: Multiple inputs", "PASS" if passed else "FAIL",
                       response.get("run", {}).get("stdout", ""), duration)
        
        # Test 2.3: Test case format (Hello N times)
        if TEST_CASES_DIR.exists():
            try:
                with open(TEST_CASES_DIR / "input1.txt") as f:
                    n = int(f.read().strip())
                with open(TEST_CASES_DIR / "output1.txt") as f:
                    expected = f.read().strip()
                
                start = time.time()
                code = f'n = int(input()); [print("Hello") for _ in range(n)]'
                response = self.execute_code(code, stdin=str(n))
                duration = time.time() - start
                
                actual = response.get("run", {}).get("stdout", "").strip()
                passed = actual == expected and response.get("run", {}).get("code", 1) == 0
                results.append(TestResult("2.3: Test case format", passed,
                                         f"Expected {len(expected.split())} lines, got {len(actual.split())}", duration))
                self.print_test("2.3: Test case format", "PASS" if passed else "FAIL",
                               f"Expected: {len(expected.split())} lines, Got: {len(actual.split())}", duration)
            except Exception as e:
                results.append(TestResult("2.3: Test case format", False, f"Error: {str(e)}"))
                self.print_test("2.3: Test case format", "FAIL", f"Error: {str(e)}")
        
        return results
    
    def test_error_handling(self) -> List[TestResult]:
        """Test 3: Error handling"""
        self.print_header("Test 3: Error Handling")
        results = []
        
        # Test 3.1: Syntax error
        start = time.time()
        response = self.execute_code('print("unclosed string')
        duration = time.time() - start
        
        passed = (
            response.get("run", {}).get("code", 0) != 0 and
            len(response.get("run", {}).get("stderr", "")) > 0
        )
        results.append(TestResult("3.1: Syntax error", passed,
                                 f"Exit code: {response.get('run', {}).get('code', 0)}", duration))
        self.print_test("3.1: Syntax error", "PASS" if passed else "FAIL",
                       f"Exit code: {response.get('run', {}).get('code', 0)}", duration)
        
        # Test 3.2: Runtime error
        start = time.time()
        response = self.execute_code('x = 1 / 0')
        duration = time.time() - start
        
        passed = (
            response.get("run", {}).get("code", 0) != 0 and
            ("ZeroDivisionError" in response.get("run", {}).get("stderr", "") or
             "division" in response.get("run", {}).get("stderr", "").lower())
        )
        results.append(TestResult("3.2: Runtime error", passed,
                                 f"Exit code: {response.get('run', {}).get('code', 0)}", duration))
        self.print_test("3.2: Runtime error", "PASS" if passed else "FAIL",
                       f"Exit code: {response.get('run', {}).get('code', 0)}", duration)
        
        # Test 3.3: Import error
        start = time.time()
        response = self.execute_code('import nonexistent_module_12345')
        duration = time.time() - start
        
        passed = (
            response.get("run", {}).get("code", 0) != 0 and
            ("ModuleNotFoundError" in response.get("run", {}).get("stderr", "") or
             "ImportError" in response.get("run", {}).get("stderr", ""))
        )
        results.append(TestResult("3.3: Import error", passed,
                                 f"Exit code: {response.get('run', {}).get('code', 0)}", duration))
        self.print_test("3.3: Import error", "PASS" if passed else "FAIL",
                       f"Exit code: {response.get('run', {}).get('code', 0)}", duration)
        
        return results
    
    def test_concurrency(self) -> List[TestResult]:
        """Test 4: Concurrency handling"""
        self.print_header("Test 4: Concurrency Tests")
        results = []
        
        # Test 4.1: Sequential requests
        print(f"{Colors.YELLOW}Running 5 sequential requests...{Colors.RESET}")
        sequential_times = []
        all_passed = True
        
        for i in range(5):
            start = time.time()
            response = self.execute_code(f'print({i * 2})')
            duration = time.time() - start
            sequential_times.append(duration)
            
            passed = response.get("run", {}).get("code", 1) == 0
            if not passed:
                all_passed = False
        
        avg_time = sum(sequential_times) / len(sequential_times)
        results.append(TestResult("4.1: Sequential requests", all_passed,
                                 f"Avg time: {avg_time:.2f}s", sum(sequential_times)))
        self.print_test("4.1: Sequential requests", "PASS" if all_passed else "FAIL",
                       f"Average: {avg_time:.2f}s", sum(sequential_times))
        
        # Test 4.2: Concurrent requests
        print(f"{Colors.YELLOW}Running 10 concurrent requests...{Colors.RESET}")
        concurrent_start = time.time()
        concurrent_results = []
        
        def run_concurrent_test(i):
            return self.execute_code(f'import time; time.sleep(0.1); print({i})')
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(run_concurrent_test, i) for i in range(10)]
            for future in as_completed(futures):
                concurrent_results.append(future.result())
        
        concurrent_duration = time.time() - concurrent_start
        all_passed = all(r.get("run", {}).get("code", 0) == 0 for r in concurrent_results)
        
        results.append(TestResult("4.2: Concurrent requests", all_passed,
                                 f"10 requests in {concurrent_duration:.2f}s", concurrent_duration))
        self.print_test("4.2: Concurrent requests", "PASS" if all_passed else "FAIL",
                       f"10 requests completed in {concurrent_duration:.2f}s", concurrent_duration)
        
        return results
    
    def test_integration(self) -> List[TestResult]:
        """Test 5: Integration tests"""
        self.print_header("Test 5: Integration Tests")
        results = []
        
        # Test 5.1: Response format
        start = time.time()
        response = self.execute_code('print("test")')
        duration = time.time() - start
        
        required_fields = ["run", "language", "version"]
        has_fields = all(field in response for field in required_fields)
        has_run_fields = all(field in response.get("run", {}) for field in ["stdout", "stderr", "code"])
        
        passed = has_fields and has_run_fields
        results.append(TestResult("5.1: Response format", passed,
                                 f"Has all required fields: {has_fields and has_run_fields}", duration))
        self.print_test("5.1: Response format", "PASS" if passed else "FAIL",
                       f"Fields present: {has_fields and has_run_fields}", duration)
        
        # Test 5.2: Test cases from directory
        if TEST_CASES_DIR.exists():
            print(f"{Colors.YELLOW}Running test cases from {TEST_CASES_DIR}...{Colors.RESET}")
            test_case_results = []
            
            # Find all input files
            input_files = sorted(TEST_CASES_DIR.glob("input*.txt"))
            
            for input_file in input_files[:5]:  # Test first 5 to avoid too long execution
                test_num = input_file.stem.replace("input", "")
                output_file = TEST_CASES_DIR / f"output{test_num}.txt"
                
                if not output_file.exists():
                    continue
                
                try:
                    with open(input_file) as f:
                        n = int(f.read().strip())
                    with open(output_file) as f:
                        expected = f.read().strip()
                    
                    start = time.time()
                    code = f'n = int(input()); [print("Hello") for _ in range(n)]'
                    response = self.execute_code(code, stdin=str(n))
                    duration = time.time() - start
                    
                    actual = response.get("run", {}).get("stdout", "").strip()
                    passed = actual == expected and response.get("run", {}).get("code", 1) == 0
                    test_case_results.append(passed)
                    
                    status = "PASS" if passed else "FAIL"
                    self.print_test(f"5.2.{test_num}: Test case {test_num}", status,
                                   f"Expected {len(expected.split())} lines", duration)
                    
                except Exception as e:
                    test_case_results.append(False)
                    self.print_test(f"5.2.{test_num}: Test case {test_num}", "FAIL", str(e))
            
            all_passed = all(test_case_results) if test_case_results else False
            passed_count = sum(test_case_results)
            results.append(TestResult("5.2: Test cases", all_passed,
                                     f"{passed_count}/{len(test_case_results)} passed", 0))
        
        return results
    
    def check_backend_health(self) -> bool:
        """Check if backend is accessible"""
        try:
            response = requests.get(f"{self.endpoint}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run_all_tests(self, full: bool = False):
        """Run all test suites"""
        self.print_header("Session Pool Code Execution Test Suite")
        
        # Check backend health
        print(f"{Colors.YELLOW}Checking backend health at {self.endpoint}...{Colors.RESET}")
        if not self.check_backend_health():
            print(f"{Colors.RED}✗ Backend is not accessible at {self.endpoint}{Colors.RESET}")
            print(f"{Colors.YELLOW}Make sure the backend is running or use --endpoint to specify the URL{Colors.RESET}")
            return
        
        print(f"{Colors.GREEN}✓ Backend is accessible{Colors.RESET}\n")
        
        # Run test suites
        all_results = []
        all_results.extend(self.test_basic_execution())
        all_results.extend(self.test_input_output())
        all_results.extend(self.test_error_handling())
        all_results.extend(self.test_concurrency())
        all_results.extend(self.test_integration())
        
        if full and TEST_CASES_DIR.exists():
            # Run all test cases
            print(f"\n{Colors.YELLOW}Running full test case suite...{Colors.RESET}")
            input_files = sorted(TEST_CASES_DIR.glob("input*.txt"))
            for input_file in input_files:
                test_num = input_file.stem.replace("input", "")
                output_file = TEST_CASES_DIR / f"output{test_num}.txt"
                
                if not output_file.exists():
                    continue
                
                try:
                    with open(input_file) as f:
                        n = int(f.read().strip())
                    with open(output_file) as f:
                        expected = f.read().strip()
                    
                    response = self.execute_code(
                        f'n = int(input()); [print("Hello") for _ in range(n)]',
                        stdin=str(n)
                    )
                    
                    actual = response.get("run", {}).get("stdout", "").strip()
                    passed = actual == expected and response.get("run", {}).get("code", 1) == 0
                    all_results.append(TestResult(f"Full.{test_num}", passed, f"Test case {test_num}"))
                    
                except Exception as e:
                    all_results.append(TestResult(f"Full.{test_num}", False, str(e)))
        
        # Print summary
        self.print_summary(all_results)
        
        self.results = all_results
        return all_results
    
    def print_summary(self, results: List[TestResult]):
        """Print test summary"""
        self.print_header("Test Summary")
        
        passed = sum(1 for r in results if r.passed)
        total = len(results)
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
        if failed > 0:
            print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
        
        if failed > 0:
            print(f"\n{Colors.RED}Failed Tests:{Colors.RESET}")
            for result in results:
                if not result.passed:
                    print(f"  ✗ {result.name}: {result.message}")
        
        success_rate = (passed / total * 100) if total > 0 else 0
        print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.RESET}")
        
        if success_rate == 100:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed!{Colors.RESET}")
        elif success_rate >= 80:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Most tests passed, but some issues detected{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ Many tests failed. Please check the implementation{Colors.RESET}")

def main():
    parser = argparse.ArgumentParser(description="Test session pool code execution")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT,
                       help=f"Backend API endpoint (default: {DEFAULT_ENDPOINT})")
    parser.add_argument("--full", action="store_true",
                       help="Run full test suite including all test cases")
    
    args = parser.parse_args()
    
    tester = SessionPoolTester(endpoint=args.endpoint)
    tester.run_all_tests(full=args.full)
    
    # Exit with appropriate code
    failed_count = sum(1 for r in tester.results if not r.passed)
    exit(0 if failed_count == 0 else 1)

if __name__ == "__main__":
    main()


