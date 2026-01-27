#!/usr/bin/env python3
'''
Test Suite for validate_config.py
==================================
Tests configuration validation logic for financial models.

Usage:
    python -m pytest tests/test_validate_config.py -v
    python tests/test_validate_config.py  # Run without pytest
'''

import json
import os
import sys
import tempfile
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'execution'))

from validate_config import ConfigValidator, ValidationLevel


class TestConfigValidator(unittest.TestCase):
    '''Test configuration validation logic'''
    
    def test_valid_config(self):
        '''Test that a valid config passes all checks'''
        config = {
            'company_name': 'TestCo',
            'tax_rate': 0.25,
            'starting_year': 2026,
            'revenue_streams': [
                {
                    'name': 'Product A',
                    'price': 1000,
                    'growth_rate': 0.5,
                    'cogs_percentage': 0.2
                }
            ],
            'fixed_costs': [
                {
                    'category': 'Rent',
                    'amount': 5000
                }
            ],
            'cac_per_customer': 500,
            'churn_rate': 0.05,
            'tam': 1000000,
            'sam': 500000,
            'som': 100000
        }
        
        validator = ConfigValidator(config)
        validator.validate_all()
        
        errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR]
        self.assertEqual(len(errors), 0, 'Valid config should have no errors')
    
    def test_missing_required_fields(self):
        '''Test detection of missing required fields'''
        config = {
            # Missing company_name, tax_rate, starting_year
            'revenue_streams': []
        }
        
        validator = ConfigValidator(config)
        validator.validate_all()
        
        errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR]
        self.assertGreater(len(errors), 0, 'Should detect missing required fields')
        
        error_fields = [i.field for i in errors]
        self.assertIn('company_name', error_fields)
        self.assertIn('tax_rate', error_fields)
        self.assertIn('starting_year', error_fields)
    
    def test_invalid_tax_rate(self):
        '''Test validation of tax_rate range'''
        # Tax rate > 1
        config = {
            'company_name': 'TestCo',
            'tax_rate': 25,  # Should be 0.25, not 25
            'starting_year': 2026
        }
        
        validator = ConfigValidator(config)
        validator.validate_all()
        
        errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR and i.field == 'tax_rate']
        self.assertEqual(len(errors), 1, 'Should detect tax_rate > 1')
        
        # Tax rate < 0
        config['tax_rate'] = -0.1
        validator = ConfigValidator(config)
        validator.validate_all()
        
        errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR and i.field == 'tax_rate']
        self.assertEqual(len(errors), 1, 'Should detect tax_rate < 0')
    
    def test_revenue_stream_validation(self):
        '''Test revenue stream parameter validation'''
        config = {
            'company_name': 'TestCo',
            'tax_rate': 0.25,
            'starting_year': 2026,
            'revenue_streams': [
                {
                    # Missing 'name' field
                    'price': -100,  # Negative price
                    'cogs_percentage': 1.5  # > 100%
                }
            ]
        }
        
        validator = ConfigValidator(config)
        validator.validate_all()
        
        errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR]
        error_messages = [i.message for i in errors]
        
        # Should detect missing name, negative price, invalid COGS
        self.assertTrue(any('name' in msg for msg in error_messages))
        self.assertTrue(any('negative' in msg.lower() for msg in error_messages))
        self.assertTrue(any('cogs' in msg.lower() for msg in error_messages))
    
    def test_template_compatibility_warning(self):
        '''Test warning for >6 revenue streams (template limit)'''
        config = {
            'company_name': 'TestCo',
            'tax_rate': 0.25,
            'starting_year': 2026,
            'revenue_streams': [
                {'name': f'Stream {i}', 'price': 100} 
                for i in range(1, 8)  # 7 streams
            ]
        }
        
        validator = ConfigValidator(config)
        validator.validate_all()
        
        warnings = [i for i in validator.issues if i.level == ValidationLevel.WARNING]
        stream_warnings = [i for i in warnings if 'revenue_streams' in i.field]
        
        self.assertEqual(len(stream_warnings), 1, 'Should warn about >6 streams')
        self.assertIn('build-from-scratch', stream_warnings[0].suggestion.lower())
    
    def test_churn_rate_validation(self):
        '''Test churn rate validation'''
        # Invalid range (> 1)
        config = {
            'company_name': 'TestCo',
            'tax_rate': 0.25,
            'starting_year': 2026,
            'churn_rate': 5  # Should be 0.05, not 5
        }
        
        validator = ConfigValidator(config)
        validator.validate_all()
        
        errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR and 'churn_rate' in i.field]
        self.assertEqual(len(errors), 1, 'Should detect churn_rate > 1')
        
        # Warning for very high churn
        config['churn_rate'] = 0.20  # 20% churn
        validator = ConfigValidator(config)
        validator.validate_all()
        
        warnings = [i for i in validator.issues if i.level == ValidationLevel.WARNING and 'churn_rate' in i.field]
        self.assertEqual(len(warnings), 1, 'Should warn about very high churn')
    
    def test_market_sizing_consistency(self):
        '''Test TAM >= SAM >= SOM validation'''
        config = {
            'company_name': 'TestCo',
            'tax_rate': 0.25,
            'starting_year': 2026,
            'tam': 100000,
            'sam': 500000,  # SAM > TAM (invalid)
            'som': 200000
        }
        
        validator = ConfigValidator(config)
        validator.validate_all()
        
        errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR and 'market_data' in i.field]
        self.assertEqual(len(errors), 1, 'Should detect SAM > TAM')
    
    def test_funding_validation(self):
        '''Test funding round validation'''
        config = {
            'company_name': 'TestCo',
            'tax_rate': 0.25,
            'starting_year': 2026,
            'funding_rounds': [
                {
                    'amount': -1000000,  # Negative amount
                    'year': '2027'  # Should be int, not string
                }
            ]
        }
        
        validator = ConfigValidator(config)
        validator.validate_all()
        
        errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR]
        error_messages = [i.message for i in errors]
        
        self.assertTrue(any('negative' in msg.lower() for msg in error_messages))
        self.assertTrue(any('integer' in msg.lower() for msg in error_messages))


class TestConfigValidatorCLI(unittest.TestCase):
    '''Test CLI functionality'''
    
    def test_valid_config_file(self):
        '''Test CLI with valid config file'''
        config = {
            'company_name': 'TestCo',
            'tax_rate': 0.25,
            'starting_year': 2026,
            'revenue_streams': [{'name': 'Product', 'price': 100}]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            # Run validation
            exit_code = os.system(f'python execution/validate_config.py --config {temp_path}')
            self.assertEqual(exit_code, 0, 'Valid config should return exit code 0')
        finally:
            os.unlink(temp_path)
    
    def test_invalid_config_file(self):
        '''Test CLI with invalid config file'''
        config = {
            # Missing required fields
            'revenue_streams': []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            # Run validation
            exit_code = os.system(f'python execution/validate_config.py --config {temp_path}')
            self.assertNotEqual(exit_code, 0, 'Invalid config should return non-zero exit code')
        finally:
            os.unlink(temp_path)


def run_tests():
    '''Run tests without pytest'''
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
