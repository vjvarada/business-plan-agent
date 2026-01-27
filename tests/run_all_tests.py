#!/usr/bin/env python3
'''
Test Runner - Run all tests
============================
Runs all test suites for the business planning agent.

Usage:
    python tests/run_all_tests.py
    python tests/run_all_tests.py --verbose
'''

import sys
import unittest
import argparse
from pathlib import Path

# Add parent directory to path
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def discover_and_run_tests(verbose=False):
    '''Discover and run all tests'''
    
    # Get the tests directory
    tests_dir = Path(__file__).parent
    
    # Discover all test files
    loader = unittest.TestLoader()
    suite = loader.discover(str(tests_dir), pattern='test_*.py')
    
    # Run tests
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    print('\n' + '='*60)
    print('TEST SUMMARY')
    print('='*60)
    print(f'Tests run: {result.testsRun}')
    print(f'Successes: {result.testsRun - len(result.failures) - len(result.errors)}')
    print(f'Failures: {len(result.failures)}')
    print(f'Errors: {len(result.errors)}')
    print('='*60)
    
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(
        description='Run all test suites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    print('Business Planning Agent - Test Suite')
    print('='*60)
    print('Running all tests...\n')
    
    exit_code = discover_and_run_tests(verbose=args.verbose)
    
    if exit_code == 0:
        print('\n All tests PASSED')
    else:
        print('\n Some tests FAILED')
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
