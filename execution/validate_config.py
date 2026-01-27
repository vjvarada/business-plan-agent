#!/usr/bin/env python3
'''
Configuration Validator for Financial Models
=============================================
Validates config.json before creating financial models to prevent errors.

Usage:
    python validate_config.py --config config.json
    python validate_config.py --config config.json --strict

Checks:
    - Required fields exist
    - Value ranges are sensible (tax 0-100%, growth reasonable)
    - Revenue stream count <= 6 for template copy
    - Data types are correct (numbers vs strings)
    - Cross-references are consistent
    - Warns about potential issues

Exit Codes:
    0 = Valid config
    1 = Warnings (proceed with caution)
    2 = Errors (do not proceed)
'''

import argparse
import json
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ValidationLevel(Enum):
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'


@dataclass
class ValidationIssue:
    level: ValidationLevel
    field: str
    message: str
    suggestion: Optional[str] = None


class ConfigValidator:
    def __init__(self, config: Dict[str, Any], strict: bool = False):
        self.config = config
        self.strict = strict
        self.issues: List[ValidationIssue] = []
        
    def add_issue(self, level: ValidationLevel, field: str, message: str, suggestion: str = None):
        '''Add a validation issue'''
        self.issues.append(ValidationIssue(level, field, message, suggestion))
        
    def validate_all(self) -> bool:
        '''Run all validations. Returns True if config is usable.'''
        print('Validating configuration...\n')
        
        # Required field checks
        self.validate_required_fields()
        
        # General parameters
        self.validate_general_params()
        
        # Revenue streams
        self.validate_revenue_streams()
        
        # Fixed costs
        self.validate_fixed_costs()
        
        # Customer acquisition
        self.validate_customer_acquisition()
        
        # Market data
        self.validate_market_data()
        
        # Funding
        self.validate_funding()
        
        # Cross-validation
        self.validate_consistency()
        
        return self.print_results()
        
    def validate_required_fields(self):
        '''Check for required top-level fields'''
        required = ['company_name', 'tax_rate', 'starting_year']
        for field in required:
            if field not in self.config:
                self.add_issue(
                    ValidationLevel.ERROR,
                    field,
                    f'Required field \'{field}\' is missing',
                    f'Add \'{field}\' to config.json'
                )
                
    def validate_general_params(self):
        '''Validate general parameters'''
        # Tax rate
        tax_rate = self.config.get('tax_rate')
        if tax_rate is not None:
            if not isinstance(tax_rate, (int, float)):
                self.add_issue(
                    ValidationLevel.ERROR,
                    'tax_rate',
                    f'tax_rate must be a number, got {type(tax_rate).__name__}'
                )
            elif tax_rate < 0 or tax_rate > 1:
                self.add_issue(
                    ValidationLevel.ERROR,
                    'tax_rate',
                    f'tax_rate must be between 0 and 1 (0-100%), got {tax_rate}',
                    'Use 0.25 for 25% tax'
                )
                
        # Starting year
        starting_year = self.config.get('starting_year')
        if starting_year is not None:
            if not isinstance(starting_year, int):
                self.add_issue(
                    ValidationLevel.ERROR,
                    'starting_year',
                    f'starting_year must be an integer, got {type(starting_year).__name__}'
                )
            elif starting_year < 2020 or starting_year > 2030:
                self.add_issue(
                    ValidationLevel.WARNING,
                    'starting_year',
                    f'starting_year {starting_year} seems unusual (expected 2020-2030)'
                )
                
    def validate_revenue_streams(self):
        '''Validate revenue stream definitions'''
        revenue_streams = self.config.get('revenue_streams', [])
        
        if not revenue_streams:
            self.add_issue(
                ValidationLevel.ERROR,
                'revenue_streams',
                'No revenue streams defined',
                'Add at least one revenue stream'
            )
            return
            
        # Check count for template compatibility
        if len(revenue_streams) > 6:
            self.add_issue(
                ValidationLevel.WARNING,
                'revenue_streams',
                f'{len(revenue_streams)} revenue streams defined (template supports max 6)',
                'Use --build-from-scratch flag for >6 streams'
            )
            
        # Validate each stream
        for i, stream in enumerate(revenue_streams):
            prefix = f'revenue_streams[{i}]'
            
            # Required fields
            if 'name' not in stream:
                self.add_issue(
                    ValidationLevel.ERROR,
                    f'{prefix}.name',
                    'Revenue stream missing \'name\' field'
                )
                
            # Price validation
            price = stream.get('price')
            if price is not None:
                if not isinstance(price, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.price',
                        f'Price must be a number, got {type(price).__name__}'
                    )
                elif price < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.price',
                        f'Price cannot be negative: {price}'
                    )
                elif price == 0:
                    self.add_issue(
                        ValidationLevel.WARNING,
                        f'{prefix}.price',
                        'Price is zero - is this intentional?'
                    )
                    
            # Growth rate validation
            growth_rate = stream.get('growth_rate')
            if growth_rate is not None:
                if not isinstance(growth_rate, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.growth_rate',
                        f'Growth rate must be a number, got {type(growth_rate).__name__}'
                    )
                elif growth_rate < -0.5 or growth_rate > 10:
                    self.add_issue(
                        ValidationLevel.WARNING,
                        f'{prefix}.growth_rate',
                        f'Growth rate {growth_rate*100:.0f}% seems extreme (expected -50% to 1000%)'
                    )
                    
            # COGS validation
            cogs = stream.get('cogs_percentage')
            if cogs is not None:
                if not isinstance(cogs, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.cogs_percentage',
                        f'COGS percentage must be a number, got {type(cogs).__name__}'
                    )
                elif cogs < 0 or cogs > 1:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.cogs_percentage',
                        f'COGS percentage must be between 0 and 1 (0-100%), got {cogs}',
                        'Use 0.20 for 20% COGS'
                    )
                    
    def validate_fixed_costs(self):
        '''Validate fixed cost categories'''
        fixed_costs = self.config.get('fixed_costs', [])
        
        # Check count
        if len(fixed_costs) > 10:
            self.add_issue(
                ValidationLevel.WARNING,
                'fixed_costs',
                f'{len(fixed_costs)} fixed cost categories (template supports max 10)',
                'Consider consolidating or use --build-from-scratch'
            )
            
        # Validate each cost
        for i, cost in enumerate(fixed_costs):
            prefix = f'fixed_costs[{i}]'
            
            if 'category' not in cost:
                self.add_issue(
                    ValidationLevel.ERROR,
                    f'{prefix}.category',
                    'Fixed cost missing \'category\' field'
                )
                
            amount = cost.get('amount')
            if amount is not None:
                if not isinstance(amount, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.amount',
                        f'Amount must be a number, got {type(amount).__name__}'
                    )
                elif amount < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.amount',
                        f'Amount cannot be negative: {amount}'
                    )
                    
    def validate_customer_acquisition(self):
        '''Validate CAC and customer metrics'''
        cac = self.config.get('cac_per_customer')
        if cac is not None:
            if not isinstance(cac, (int, float)):
                self.add_issue(
                    ValidationLevel.ERROR,
                    'cac_per_customer',
                    f'CAC must be a number, got {type(cac).__name__}'
                )
            elif cac < 0:
                self.add_issue(
                    ValidationLevel.ERROR,
                    'cac_per_customer',
                    f'CAC cannot be negative: {cac}'
                )
            elif cac == 0:
                self.add_issue(
                    ValidationLevel.WARNING,
                    'cac_per_customer',
                    'CAC is zero - organic growth only?'
                )
                
        # Churn rate
        churn = self.config.get('churn_rate')
        if churn is not None:
            if not isinstance(churn, (int, float)):
                self.add_issue(
                    ValidationLevel.ERROR,
                    'churn_rate',
                    f'Churn rate must be a number, got {type(churn).__name__}'
                )
            elif churn < 0 or churn > 1:
                self.add_issue(
                    ValidationLevel.ERROR,
                    'churn_rate',
                    f'Churn rate must be between 0 and 1 (0-100%), got {churn}',
                    'Use 0.05 for 5% monthly churn'
                )
            elif churn > 0.15:
                self.add_issue(
                    ValidationLevel.WARNING,
                    'churn_rate',
                    f'Churn rate {churn*100:.1f}% is very high (>15%/month)',
                    'Industry average for B2B SaaS is 3.5-10%/month'
                )
                
    def validate_market_data(self):
        '''Validate TAM/SAM/SOM values'''
        tam = self.config.get('tam')
        sam = self.config.get('sam')
        som = self.config.get('som')
        
        # Type checks
        for field, value in [('tam', tam), ('sam', sam), ('som', som)]:
            if value is not None and not isinstance(value, (int, float)):
                self.add_issue(
                    ValidationLevel.ERROR,
                    field,
                    f'{field.upper()} must be a number, got {type(value).__name__}'
                )
                
        # Logical consistency (if all present)
        if all(v is not None for v in [tam, sam, som]):
            if not (som <= sam <= tam):
                self.add_issue(
                    ValidationLevel.ERROR,
                    'market_data',
                    f'Market sizing must satisfy SOM <= SAM <= TAM, got TAM={tam}, SAM={sam}, SOM={som}',
                    'SOM is your realistic target, SAM is addressable, TAM is total market'
                )
                
    def validate_funding(self):
        '''Validate funding rounds'''
        funding_rounds = self.config.get('funding_rounds', [])
        
        for i, round_data in enumerate(funding_rounds):
            prefix = f'funding_rounds[{i}]'
            
            amount = round_data.get('amount')
            if amount is not None:
                if not isinstance(amount, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.amount',
                        f'Funding amount must be a number, got {type(amount).__name__}'
                    )
                elif amount < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f'{prefix}.amount',
                        f'Funding amount cannot be negative: {amount}'
                    )
                    
            year = round_data.get('year')
            if year is not None and not isinstance(year, int):
                self.add_issue(
                    ValidationLevel.ERROR,
                    f'{prefix}.year',
                    f'Funding year must be an integer, got {type(year).__name__}'
                )
                
    def validate_consistency(self):
        '''Cross-field validation checks'''
        # Check if starting_year aligns with funding years
        starting_year = self.config.get('starting_year')
        funding_rounds = self.config.get('funding_rounds', [])
        
        if starting_year:
            for i, round_data in enumerate(funding_rounds):
                year = round_data.get('year')
                # Only compare if year is an integer (already validated in validate_funding)
                if year and isinstance(year, int) and isinstance(starting_year, int):
                    if year < starting_year:
                        self.add_issue(
                            ValidationLevel.WARNING,
                            f'funding_rounds[{i}].year',
                            f'Funding year {year} is before starting_year {starting_year}'
                        )
                    elif year > starting_year + 10:
                        self.add_issue(
                        ValidationLevel.WARNING,
                        f'funding_rounds[{i}].year',
                        f'Funding year {year} is >10 years after start (year {starting_year})'
                    )
                    
    def print_results(self) -> bool:
        '''Print validation results and return True if config is usable'''
        errors = [i for i in self.issues if i.level == ValidationLevel.ERROR]
        warnings = [i for i in self.issues if i.level == ValidationLevel.WARNING]
        infos = [i for i in self.issues if i.level == ValidationLevel.INFO]
        
        # Print errors
        if errors:
            print('\n ERRORS (must fix):')
            for issue in errors:
                print(f'  [{issue.field}] {issue.message}')
                if issue.suggestion:
                    print(f'     {issue.suggestion}')
                    
        # Print warnings
        if warnings:
            print('\n  WARNINGS (review carefully):')
            for issue in warnings:
                print(f'  [{issue.field}] {issue.message}')
                if issue.suggestion:
                    print(f'     {issue.suggestion}')
                    
        # Print info
        if infos:
            print('\nℹ  INFO:')
            for issue in infos:
                print(f'  [{issue.field}] {issue.message}')
                
        # Summary
        print('\n' + '='*60)
        if not errors and not warnings:
            print(' Configuration is VALID - ready to create financial model')
            print('='*60)
            return True
        elif not errors:
            print(f'  Configuration has {len(warnings)} WARNING(S)')
            print('   You can proceed, but review warnings carefully')
            print('='*60)
            return True
        else:
            print(f' Configuration has {len(errors)} ERROR(S)')
            print('   Fix errors before creating financial model')
            print('='*60)
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Validate financial model configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--config', required=True, help='Path to config.json file')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    
    args = parser.parse_args()
    
    # Load config
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f' ERROR: Config file not found: {args.config}')
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f' ERROR: Invalid JSON in config file: {e}')
        sys.exit(2)
        
    # Validate
    validator = ConfigValidator(config, strict=args.strict)
    is_valid = validator.validate_all()
    
    # Exit codes
    errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR]
    warnings = [i for i in validator.issues if i.level == ValidationLevel.WARNING]
    
    if errors:
        sys.exit(2)  # Errors - do not proceed
    elif warnings and args.strict:
        sys.exit(1)  # Warnings in strict mode
    elif warnings:
        sys.exit(1)  # Warnings - proceed with caution
    else:
        sys.exit(0)  # All good


if __name__ == '__main__':
    main()
