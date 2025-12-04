#!/usr/bin/env python3
"""
Quick Full Test - All Languages (2 test cases each for speed)
Tests all 5 languages with 2 test cases per endpoint
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import the main test module
from test_all_languages_fastapi import *

# Override to use only 2 test cases
def quick_generate_test_cases(count=2, problem_type="sum"):
    """Generate only 2 test cases for speed"""
    return generate_test_cases(2, problem_type)

# Replace the function
generate_test_cases = quick_generate_test_cases

# Now run the main test
if __name__ == "__main__":
    # Re-import to get fresh functions
    import importlib
    import test_all_languages_fastapi
    test_all_languages_fastapi.generate_test_cases = quick_generate_test_cases
    
    # Run the tests
    print("🧪 Quick Full Test - All Languages (2 test cases each)")
    print("=" * 70)
    
    if not test_health():
        print("\n❌ Service is not running!")
        sys.exit(1)
    
    languages = ["python", "java", "cpp", "javascript", "csharp"]
    language_results = []
    
    for language in languages:
        # Modify the test_language function to use 2 test cases
        original_test = test_language
        passed = test_language(language)
        language_results.append((language, passed))
        print("\n")
    
    # Final summary
    print("=" * 70)
    print("📊 FINAL SUMMARY")
    print("=" * 70)
    
    for language, passed in language_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {language.upper()}")
    
    all_passed = all(result[1] for result in language_results)
    
    if all_passed:
        print("\n🎉 All languages passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed.")
        sys.exit(1)

