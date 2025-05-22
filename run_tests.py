#!/usr/bin/env python3
"""
Test runner for EMS Analysis Pipeline.

This script runs all unit tests and generates a test report.
"""

import unittest
import sys
import os
from pathlib import Path
import time

def main():
    """Run all tests and generate report."""
    print("=" * 60)
    print("EMS ANALYSIS PIPELINE - TEST SUITE")
    print("=" * 60)
    
    # Add src directory to path
    project_root = Path(__file__).parent
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = project_root / "tests"
    
    if not start_dir.exists():
        print(f"ERROR: Tests directory not found at {start_dir}")
        return False
    
    print(f"Discovering tests in: {start_dir}")
    suite = loader.discover(str(start_dir), pattern='test_*.py')
    
    # Count total tests
    test_count = suite.countTestCases()
    print(f"Found {test_count} test cases")
    print("-" * 60)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True,
        descriptions=True
    )
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    
    # Print failure details if any
    if result.failures:
        print("\n" + "-" * 60)
        print("FAILURES:")
        print("-" * 60)
        for test, traceback in result.failures:
            print(f"\nFAILED: {test}")
            print(traceback)
    
    # Print error details if any
    if result.errors:
        print("\n" + "-" * 60)
        print("ERRORS:")
        print("-" * 60)
        for test, traceback in result.errors:
            print(f"\nERROR: {test}")
            print(traceback)
    
    # Return success status
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n❌ {len(result.failures) + len(result.errors)} TESTS FAILED")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)