#!/usr/bin/env python3
'''
Test Suite for verify_template_copy.py
=======================================
Tests template verification functionality.

Usage:
    python -m pytest tests/test_template_copy.py -v
    python tests/test_template_copy.py  # Run without pytest
'''

import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'execution'))

from verify_template_copy import verify_sheet_structure, EXPECTED_SHEETS


class TestTemplateVerification(unittest.TestCase):
    '''Test template verification logic'''
    
    def test_verify_perfect_match(self):
        '''Test verification of perfect template match'''
        # Mock spreadsheet with all correct sheets in correct order
        mock_spreadsheet = Mock()
        mock_worksheets = [Mock(title=name) for name in EXPECTED_SHEETS]
        mock_spreadsheet.worksheets.return_value = mock_worksheets
        
        result = verify_sheet_structure(mock_spreadsheet)
        
        self.assertEqual(len(result['missing_sheets']), 0, 'Should have no missing sheets')
        self.assertEqual(len(result['extra_sheets']), 0, 'Should have no extra sheets')
        self.assertEqual(len(result['order_issues']), 0, 'Should have no order issues')
        
        errors = [i for i in result['issues'] if i[0] == 'ERROR']
        self.assertEqual(len(errors), 0, 'Should have no errors')
    
    def test_verify_missing_sheets(self):
        '''Test detection of missing sheets'''
        # Mock spreadsheet missing 2 sheets
        mock_spreadsheet = Mock()
        incomplete_sheets = EXPECTED_SHEETS[:12]  # Missing last 2 sheets
        mock_worksheets = [Mock(title=name) for name in incomplete_sheets]
        mock_spreadsheet.worksheets.return_value = mock_worksheets
        
        result = verify_sheet_structure(mock_spreadsheet)
        
        self.assertEqual(len(result['missing_sheets']), 2, 'Should detect 2 missing sheets')
        self.assertIn('Funding Cap Table', result['missing_sheets'])
        self.assertIn('Charts Data', result['missing_sheets'])
        
        errors = [i for i in result['issues'] if i[0] == 'ERROR']
        self.assertEqual(len(errors), 2, 'Should have 2 errors for missing sheets')
    
    def test_verify_extra_sheets(self):
        '''Test detection of extra sheets'''
        # Mock spreadsheet with extra sheets
        mock_spreadsheet = Mock()
        sheets_with_extras = EXPECTED_SHEETS + ['Extra Sheet', 'Debug Sheet']
        mock_worksheets = [Mock(title=name) for name in sheets_with_extras]
        mock_spreadsheet.worksheets.return_value = mock_worksheets
        
        result = verify_sheet_structure(mock_spreadsheet)
        
        self.assertEqual(len(result['extra_sheets']), 2, 'Should detect 2 extra sheets')
        self.assertIn('Extra Sheet', result['extra_sheets'])
        self.assertIn('Debug Sheet', result['extra_sheets'])
        
        warnings = [i for i in result['issues'] if i[0] == 'WARNING']
        self.assertEqual(len(warnings), 2, 'Should have 2 warnings for extra sheets')
    
    def test_verify_wrong_order(self):
        '''Test detection of wrong sheet order'''
        # Mock spreadsheet with sheets in wrong order
        mock_spreadsheet = Mock()
        wrong_order_sheets = [
            'Assumptions',  # Should be 2nd, but is 1st
            'Sources & References',  # Should be 1st, but is 2nd
        ] + EXPECTED_SHEETS[2:]
        mock_worksheets = [Mock(title=name) for name in wrong_order_sheets]
        mock_spreadsheet.worksheets.return_value = mock_worksheets
        
        result = verify_sheet_structure(mock_spreadsheet)
        
        self.assertGreater(len(result['order_issues']), 0, 'Should detect order issues')
        
        warnings = [i for i in result['issues'] if i[0] == 'WARNING' and 'order' in i[1].lower()]
        self.assertGreater(len(warnings), 0, 'Should have warnings for order issues')
    
    def test_expected_sheets_count(self):
        '''Test that we expect exactly 14 sheets'''
        self.assertEqual(len(EXPECTED_SHEETS), 14, 'Should expect 14 sheets (RapidTools template)')
    
    def test_expected_sheets_names(self):
        '''Test specific sheet names are in expected list'''
        critical_sheets = [
            'Sources & References',
            'Assumptions',
            'Headcount Plan',
            'Revenue',
            'P&L',
            'Cash Flow',
            'Balance Sheet',
            'Charts Data'
        ]
        
        for sheet in critical_sheets:
            self.assertIn(sheet, EXPECTED_SHEETS, f'{sheet} should be in expected sheets')


class TestSheetErrorDetection(unittest.TestCase):
    '''Test error detection in sheets'''
    
    def test_formula_error_detection(self):
        '''Test detection of formula errors like #REF!, #VALUE!'''
        from verify_template_copy import check_for_errors
        
        # Mock worksheet with errors
        mock_worksheet = Mock()
        mock_worksheet.get_all_values.return_value = [
            ['Name', 'Value', 'Formula'],
            ['Item 1', '100', '=A2*B2'],
            ['Item 2', '#REF!', '=A3*B3'],  # Error
            ['Item 3', '300', '=A4*B4'],
            ['Item 4', '#VALUE!', '=A5/0']  # Error
        ]
        
        errors = check_for_errors(mock_worksheet)
        
        self.assertEqual(len(errors), 2, 'Should detect 2 formula errors')
        self.assertTrue(any('#REF!' in err for err in errors), 'Should detect #REF! error')
        self.assertTrue(any('#VALUE!' in err for err in errors), 'Should detect #VALUE! error')


def run_tests():
    '''Run tests without pytest'''
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
