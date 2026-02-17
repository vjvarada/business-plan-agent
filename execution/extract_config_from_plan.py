#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract Financial Model Configuration from Business Plan Sections

This script parses business plan markdown sections to extract:
- TAM/SAM/SOM from 02_TAM_SAM_SOM_Calculation.md
- Revenue streams and pricing from 07_Revenue_Model.md
- Team/headcount from 08_Team_Organization_Fixed_Costs.md
- Funding rounds from 09_Fundraising_Strategy.md
- Financial projections from 10_Financial_Projections.md

Usage:
    python extract_config_from_plan.py --sections-dir .tmp/myproject/business_plan/sections
    python extract_config_from_plan.py --sections-dir .tmp/myproject/business_plan/sections --output .tmp/myproject/config/config.json

Output: JSON configuration file for build_financial_model.py
"""

import os
import re
import json
import argparse
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path


def parse_currency(text: str) -> Optional[float]:
    """Parse currency values like $1.5M, $25B, ₹100Cr, etc."""
    if not text:
        return None
    
    # Clean up
    text = text.strip().replace(',', '').replace(' ', '')
    
    # Multipliers
    multipliers = {
        'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3,
        'Cr': 1e7, 'Lakh': 1e5, 'L': 1e5,
        'trillion': 1e12, 'billion': 1e9, 'million': 1e6,
    }
    
    # Pattern: optional currency symbol, number, optional multiplier
    pattern = r'[\$₹€£]?(\d+\.?\d*)\s*(T|B|M|K|Cr|Lakh|L|trillion|billion|million)?'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        value = float(match.group(1))
        suffix = match.group(2)
        if suffix:
            for key, mult in multipliers.items():
                if suffix.lower() == key.lower():
                    value *= mult
                    break
        return value
    
    return None


def parse_percentage(text: str) -> Optional[float]:
    """Parse percentage values like 25%, 0.25, etc."""
    if not text:
        return None
    
    text = text.strip()
    
    # If it contains %, parse as percentage
    if '%' in text:
        match = re.search(r'(\d+\.?\d*)%', text)
        if match:
            return float(match.group(1)) / 100
    
    # Otherwise check if it's a decimal < 1
    try:
        value = float(text)
        if 0 <= value <= 1:
            return value
        elif value > 1:
            return value / 100  # Assume it's a percentage without %
    except ValueError:
        pass
    
    return None


def extract_table_data(content: str, table_name: str) -> List[Dict[str, str]]:
    """Extract data from a markdown table by searching for table headers."""
    lines = content.split('\n')
    rows = []
    headers = None
    in_table = False
    
    for i, line in enumerate(lines):
        # Check if this line contains a table header
        if '|' in line and not in_table:
            # Check if next line is separator (---)
            if i + 1 < len(lines) and '---' in lines[i + 1] and '|' in lines[i + 1]:
                headers = [h.strip() for h in line.split('|') if h.strip()]
                in_table = True
                continue
        
        if in_table:
            if '---' in line:
                continue
            if '|' in line:
                values = [v.strip() for v in line.split('|') if v.strip()]
                if len(values) >= len(headers):
                    row = {headers[j]: values[j] for j in range(len(headers))}
                    rows.append(row)
            else:
                # End of table
                if rows:  # Only break if we found data
                    break
    
    return rows


def extract_tam_sam_som(filepath: str) -> Dict[str, Any]:
    """Extract TAM/SAM/SOM data from 02_TAM_SAM_SOM_Calculation.md"""
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found")
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'tam': {},
        'sam': {},
        'som': {}
    }
    
    # Look for TAM values
    tam_patterns = [
        (r'Software\s*TAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'software'),
        (r'Hardware\s*TAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'hardware'),
        (r'Services\s*TAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'services'),
        (r'Consumables?\s*TAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'consumables'),
        (r'Total\s*TAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'total'),
    ]
    
    for pattern, key in tam_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            suffix = match.group(2).upper()
            mult = {'T': 1000000, 'B': 1000, 'M': 1}.get(suffix, 1)
            result['tam'][key] = value * mult  # In millions
    
    # Look for SAM values
    sam_patterns = [
        (r'India\s*SAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'india'),
        (r'SE\s*Asia\s*SAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'se_asia'),
        (r'Southeast\s*Asia\s*SAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'se_asia'),
        (r'Total\s*SAM[:\s]+\$?(\d+\.?\d*)\s*([BMT])', 'total'),
    ]
    
    for pattern, key in sam_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            suffix = match.group(2).upper()
            mult = {'T': 1000000, 'B': 1000, 'M': 1}.get(suffix, 1)
            result['sam'][key] = value * mult
    
    # Look for SOM / Year 8 revenue target
    som_patterns = [
        r'Year\s*8\s*Revenue[:\s]+\$?(\d+\.?\d*)\s*([BMT])?',
        r'SOM[:\s]+\$?(\d+\.?\d*)\s*([BMT])?',
        r'Year\s*8[:\s]+\$?(\d+\.?\d*)\s*([BMT])?.*?revenue',
    ]
    
    for pattern in som_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            suffix = match.group(2).upper() if match.group(2) else 'M'
            mult = {'T': 1000000, 'B': 1000, 'M': 1}.get(suffix, 1)
            result['som']['year8_revenue'] = value * mult
            break
    
    return result


def extract_revenue_model(filepath: str) -> Dict[str, Any]:
    """Extract revenue streams and pricing from 07_Revenue_Model.md"""
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found")
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'revenue_streams': []
    }
    
    # Look for revenue stream patterns
    # Pattern: Stream name with price, volume, growth
    stream_patterns = [
        # Try to find table-formatted data
        r'\|\s*(Software|Hardware|Services|Consumables)\s*\|.*?\$?(\d+,?\d*)\s*\|',
    ]
    
    # Common revenue stream names
    stream_names = ['Software', 'Hardware', 'Services', 'Consumables', 'Subscription', 'Licensing']
    
    for name in stream_names:
        stream = {'name': name}
        
        # Look for price
        price_pattern = rf'{name}.*?price[:\s]+\$?(\d+,?\d*)'
        match = re.search(price_pattern, content, re.IGNORECASE)
        if match:
            stream['price'] = int(match.group(1).replace(',', ''))
        
        # Look for COGS %
        cogs_pattern = rf'{name}.*?COGS[:\s]+(\d+\.?\d*)%?'
        match = re.search(cogs_pattern, content, re.IGNORECASE)
        if match:
            cogs = float(match.group(1))
            stream['cogs_pct'] = cogs / 100 if cogs > 1 else cogs
        
        # Look for growth rate
        growth_pattern = rf'{name}.*?growth[:\s]+(\d+\.?\d*)%?'
        match = re.search(growth_pattern, content, re.IGNORECASE)
        if match:
            growth = float(match.group(1))
            stream['growth'] = growth / 100 if growth > 1 else growth
        
        # Only add if we found at least a price
        if 'price' in stream:
            # Set defaults
            stream.setdefault('volume', 10)
            stream.setdefault('growth', 0.25)
            stream.setdefault('cogs_pct', 0.30)
            result['revenue_streams'].append(stream)
    
    return result


def extract_team_costs(filepath: str) -> Dict[str, Any]:
    """Extract headcount and fixed costs from 08_Team_Organization_Fixed_Costs.md"""
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found")
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'headcount': {},
        'fixed_costs': {}
    }
    
    # Look for department patterns
    dept_patterns = [
        (r'Engineering[:\s]+(\d+)\s*FTE', 'engineering_y0'),
        (r'Sales[:\s]+(\d+)\s*FTE', 'sales_y0'),
        (r'Operations[:\s]+(\d+)\s*FTE', 'ops_y0'),
        (r'G&A[:\s]+(\d+)\s*FTE', 'ga_y0'),
    ]
    
    for pattern, key in dept_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            result['headcount'][key] = int(match.group(1))
    
    # Look for salary patterns
    salary_patterns = [
        (r'Engineering.*?salary[:\s]+\$?(\d+,?\d*)', 'engineering_salary'),
        (r'Sales.*?salary[:\s]+\$?(\d+,?\d*)', 'sales_salary'),
        (r'Operations.*?salary[:\s]+\$?(\d+,?\d*)', 'ops_salary'),
        (r'G&A.*?salary[:\s]+\$?(\d+,?\d*)', 'ga_salary'),
    ]
    
    for pattern, key in salary_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            result['headcount'][key] = int(match.group(1).replace(',', ''))
    
    # Look for fixed costs
    cost_patterns = [
        (r'Office.*?\$?(\d+,?\d*)', 'Office & Utilities'),
        (r'Marketing.*?\$?(\d+,?\d*)', 'Marketing'),
        (r'R&D.*?\$?(\d+,?\d*)', 'R&D'),
        (r'Legal.*?\$?(\d+,?\d*)', 'Legal & Compliance'),
        (r'Insurance.*?\$?(\d+,?\d*)', 'Insurance'),
    ]
    
    for pattern, name in cost_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            result['fixed_costs'][name] = int(match.group(1).replace(',', ''))
    
    return result


def extract_fundraising(filepath: str) -> Dict[str, Any]:
    """Extract funding rounds from 09_Fundraising_Strategy.md"""
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found")
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'funding': {}
    }
    
    # Look for funding round patterns
    funding_patterns = [
        (r'Seed[:\s]+\$?(\d+\.?\d*)\s*([MBK])', 'seed', 'seed_pre'),
        (r'Series\s*A[:\s]+\$?(\d+\.?\d*)\s*([MBK])', 'series_a', 'series_a_pre'),
        (r'Series\s*B[:\s]+\$?(\d+\.?\d*)\s*([MBK])', 'series_b', 'series_b_pre'),
    ]
    
    multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    
    for pattern, key, pre_key in funding_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            suffix = match.group(2).upper()
            result['funding'][key] = int(value * multipliers.get(suffix, 1))
    
    # Look for timing
    timing_patterns = [
        (r'Seed.*?Year\s*(\d+)', 'seed_year'),
        (r'Series\s*A.*?Year\s*(\d+)', 'series_a_year'),
        (r'Series\s*B.*?Year\s*(\d+)', 'series_b_year'),
    ]
    
    for pattern, key in timing_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            result['funding'][key] = int(match.group(1))
    
    # Look for pre-money valuations
    valuation_patterns = [
        (r'Seed.*?pre-money[:\s]+\$?(\d+\.?\d*)\s*([MBK])', 'seed_pre'),
        (r'Series\s*A.*?pre-money[:\s]+\$?(\d+\.?\d*)\s*([MBK])', 'series_a_pre'),
        (r'Series\s*B.*?pre-money[:\s]+\$?(\d+\.?\d*)\s*([MBK])', 'series_b_pre'),
    ]
    
    for pattern, key in valuation_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            suffix = match.group(2).upper()
            result['funding'][key] = int(value * multipliers.get(suffix, 1))
    
    return result


def extract_general_params(filepath: str) -> Dict[str, Any]:
    """Extract general parameters from 10_Financial_Projections.md"""
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found")
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'general': {}
    }
    
    # Tax rate
    match = re.search(r'Tax\s*Rate[:\s]+(\d+\.?\d*)%?', content, re.IGNORECASE)
    if match:
        rate = float(match.group(1))
        result['general']['tax_rate'] = rate / 100 if rate > 1 else rate
    
    # CapEx
    match = re.search(r'CapEx.*?Year\s*0[:\s]+\$?(\d+,?\d*)', content, re.IGNORECASE)
    if match:
        result['general']['capex_y0'] = int(match.group(1).replace(',', ''))
    
    match = re.search(r'Annual\s*CapEx[:\s]+\$?(\d+,?\d*)', content, re.IGNORECASE)
    if match:
        result['general']['capex_annual'] = int(match.group(1).replace(',', ''))
    
    # Depreciation
    match = re.search(r'Depreciation.*?(\d+)\s*years?', content, re.IGNORECASE)
    if match:
        result['general']['depreciation_years'] = int(match.group(1))
    
    # Working capital
    match = re.search(r'Debtor\s*Days[:\s]+(\d+)', content, re.IGNORECASE)
    if match:
        result['general']['debtor_days'] = int(match.group(1))
    
    match = re.search(r'Creditor\s*Days[:\s]+(\d+)', content, re.IGNORECASE)
    if match:
        result['general']['creditor_days'] = int(match.group(1))
    
    return result


def merge_configs(*configs) -> Dict[str, Any]:
    """Merge multiple config dictionaries."""
    result = {}
    for config in configs:
        for key, value in config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key].update(value)
            elif key in result and isinstance(result[key], list) and isinstance(value, list):
                result[key].extend(value)
            else:
                result[key] = value
    return result


def create_default_config(company: str = 'Company') -> Dict[str, Any]:
    """Create default config with placeholder values."""
    return {
        'company': company,
        'general': {
            'tax_rate': 0.25,
            'capex_y0': 150000,
            'capex_annual': 50000,
            'depreciation_years': 5,
            'debtor_days': 45,
            'creditor_days': 30,
            'interest_rate': 0.10,
            'cost_inflation': 0.05
        },
        'revenue_streams': [
            {'name': 'Software', 'price': 2500, 'volume': 25, 'growth': 0.50, 'cogs_pct': 0.15},
            {'name': 'Hardware', 'price': 5000, 'volume': 15, 'growth': 0.35, 'cogs_pct': 0.60},
            {'name': 'Services', 'price': 10000, 'volume': 5, 'growth': 0.40, 'cogs_pct': 0.45},
        ],
        'fixed_costs': {
            'Office & Utilities': 36000,
            'Marketing': 60000,
            'R&D': 72000,
            'Legal & Compliance': 24000,
            'Insurance': 12000,
        },
        'headcount': {
            'engineering_salary': 80000, 'engineering_y0': 5,
            'sales_salary': 60000, 'sales_y0': 3,
            'ops_salary': 50000, 'ops_y0': 2,
            'ga_salary': 70000, 'ga_y0': 2,
        },
        'funding': {
            'seed': 3000000, 'seed_year': 0, 'seed_pre': 10000000,
            'series_a': 10000000, 'series_a_year': 2, 'series_a_pre': 30000000,
            'series_b': 25000000, 'series_b_year': 4, 'series_b_pre': 75000000,
        },
        'tam': {'software': 10000, 'hardware': 4000, 'consumables': 8000, 'services': 20000},
        'sam': {'india': 1800, 'se_asia': 1080},
        'som': {'year8_revenue': 104},
    }


def main():
    parser = argparse.ArgumentParser(
        description='Extract financial model config from business plan sections',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python extract_config_from_plan.py --sections-dir .tmp/myproject/business_plan/sections
  python extract_config_from_plan.py --sections-dir .tmp/myproject/business_plan/sections --output .tmp/myproject/config/config.json
  python extract_config_from_plan.py --company "MyCompany" --create-default

Extracts from these sections:
  02_TAM_SAM_SOM_Calculation.md     → tam, sam, som
  07_Revenue_Model.md               → revenue_streams
  08_Team_Organization_Fixed_Costs.md → headcount, fixed_costs
  09_Fundraising_Strategy.md        → funding
  10_Financial_Projections.md       → general parameters
        '''
    )
    parser.add_argument('--sections-dir', '-d', help='Directory containing business plan sections')
    parser.add_argument('--output', '-o', help='Output JSON config file')
    parser.add_argument('--company', help='Company name')
    parser.add_argument('--create-default', action='store_true', help='Create default config if no sections found')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Determine company name
    company = args.company or 'Company'
    
    # Start with defaults
    config = create_default_config(company)
    
    if args.sections_dir and os.path.exists(args.sections_dir):
        print(f"Extracting config from: {args.sections_dir}")
        print("=" * 60)
        
        # Define section mappings
        section_files = {
            '02_TAM_SAM_SOM_Calculation.md': extract_tam_sam_som,
            '07_Revenue_Model.md': extract_revenue_model,
            '08_Team_Organization_Fixed_Costs.md': extract_team_costs,
            '09_Fundraising_Strategy.md': extract_fundraising,
            '10_Financial_Projections.md': extract_general_params,
        }
        
        # Extract from each section
        for filename, extractor in section_files.items():
            filepath = os.path.join(args.sections_dir, filename)
            print(f"  Processing: {filename}")
            
            extracted = extractor(filepath)
            if extracted:
                config = merge_configs(config, extracted)
                if args.verbose:
                    print(f"    → Extracted: {list(extracted.keys())}")
            else:
                print(f"    → No data found or file missing")
        
        print("=" * 60)
    elif args.create_default:
        print(f"Creating default config for {company}")
    else:
        print("ERROR: Provide --sections-dir or --create-default")
        return 1
    
    # Set company name
    config['company'] = company
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        os.makedirs('.tmp', exist_ok=True)
        output_path = f'.tmp/{company.replace(" ", "_")}_config.json'
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # Save config
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Config saved: {output_path}")
    
    # Print summary
    print("\nConfiguration Summary:")
    print(f"  Company: {config['company']}")
    print(f"  TAM: {config.get('tam', {})}")
    print(f"  SAM: {config.get('sam', {})}")
    print(f"  SOM: {config.get('som', {})}")
    print(f"  Revenue Streams: {len(config.get('revenue_streams', []))}")
    print(f"  Funding: {config.get('funding', {})}")
    
    print(f"\nNext steps:")
    print(f"  1. Review and edit: {output_path}")
    print(f"  2. Build model:")
    print(f"     python execution/build_financial_model.py --config {output_path}")
    
    return 0


if __name__ == '__main__':
    exit(main())
