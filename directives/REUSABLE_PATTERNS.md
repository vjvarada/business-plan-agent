# Reusable Patterns from RapidTools Business Plan Development

This document catalogs reusable code patterns extracted from temporary scripts created during the RapidTools business plan and financial model development. These patterns can be adapted for future business plan agents.

## 1. Sheet Linkage Analysis

**Purpose:** Find all formula references between sheets before restructuring  
**Source:** `.tmp/find_linkages.py`  
**Key Pattern:**

```python
def find_sheet_linkages(spreadsheet, source_sheet_name, target_sheet_name):
    """Find all cells in source_sheet referenced by formulas in target_sheet"""
    
    # Get formulas (not values)
    ranges = [f'{target_sheet_name}!A1:Z500']
    result = spreadsheet.values_batch_get(ranges, params={'valueRenderOption': 'FORMULA'})
    
    linked_cells = {}
    data = result['valueRanges'][0].get('values', [])
    
    for i, row in enumerate(data, 1):
        for j, cell in enumerate(row, 1):
            if cell and isinstance(cell, str):
                # Find references like 'Sources & References'!B46
                pattern = rf"''{source_sheet_name}''!([A-Z]+)(\d+)"
                matches = re.finditer(pattern, cell)
                
                for match in matches:
                    src_ref = f"{match.group(1)}{match.group(2)}"
                    if src_ref not in linked_cells:
                        linked_cells[src_ref] = []
                    linked_cells[src_ref].append(f"{target_sheet_name}!{col_letter}{i}")
    
    return linked_cells
```

**Use Case:** Before restructuring Sources & References sheet, we identified 26 critical cells in column B that Assumptions sheet referenced. This prevented breaking formulas.

---

## 2. Business Plan Credibility Audit

**Purpose:** Check business plan for math errors, unsourced claims, missing timeframes  
**Source:** `.tmp/audit_assumptions.py`  
**Key Patterns:**

### A. Math Validation
```python
def audit_math_calculations(doc_content):
    """Find calculation errors in business plan"""
    
    # Pattern: number  number = result
    calc_pattern = r'(\d+[,\d]*)\s*[x*]\s*(\d+[,\d]*)\s*=\s*\$?([,\d]+)'
    matches = re.findall(calc_pattern, doc_content)
    
    issues = []
    for num1_str, num2_str, result_str in matches:
        num1 = int(num1_str.replace(',', ''))
        num2 = int(num2_str.replace(',', ''))
        expected = num1 * num2
        actual = int(result_str.replace(',', ''))
        
        if expected != actual:
            issues.append({
                'type': 'MATH_ERROR',
                'calculation': f"{num1_str}  {num2_str} = {result_str}",
                'expected': f"${expected:,}",
                'actual': f"${actual:,}"
            })
    
    return issues
```

**Real Issue Found:** Consumables revenue was stated as $960K but correct calculation was 800 printers  60%  $1,200 = $576K, not $960K.

### B. Source Verification
```python
def check_sourced_claims(doc_content, research_data):
    """Verify TAM/SAM claims have sources"""
    
    # Find dollar amounts
    tam_matches = re.findall(r'TAM[:\s]+\$([0-9.]+)([BMK])', doc_content, re.I)
    
    unsourced = []
    for value, unit in tam_matches:
        # Check if value appears in research files
        found_source = False
        for research_file, data in research_data.items():
            for result in data.get('organic_results', []):
                snippet = result.get('snippet', '')
                if f"{value}{unit}" in snippet or value in snippet:
                    found_source = True
                    break
        
        if not found_source:
            unsourced.append({
                'value': f"${value}{unit}",
                'recommendation': 'Add source citation or change to range estimate'
            })
    
    return unsourced
```

**Real Issue Found:** Software TAM included "+$6B tooling-specific CAD" which was estimated, not sourced. Changed to range "$9-15B".

### C. Timeframe Labeling
```python
def check_timeframe_labels(doc_content):
    """Ensure projections have clear year labels"""
    
    # Find dollar amounts without year labels
    pattern = r'(\$[0-9.]+[BMK])(?!.*(?:20\d{2}|Year \d|by 20\d{2}))'
    matches = re.finditer(pattern, doc_content)
    
    missing_timeframes = []
    for match in matches:
        context = doc_content[max(0, match.start()-50):match.end()+50]
        if 'TAM' in context or 'SAM' in context:
            missing_timeframes.append({
                'value': match.group(1),
                'context': context,
                'recommendation': 'Add timeframe (e.g., "by 2030" or "(2035 projection)")'
            })
    
    return missing_timeframes
```

**Real Issue Found:** TAM values shown as "$292B" without clarifying it's 2030 projection. Added "(2023-2030 combined)".

---

## 3. Sheet Restructuring with Formula Preservation

**Purpose:** Restructure sheet layout while preserving downstream formulas  
**Source:** `.tmp/update_sources_sheet.py`  
**Key Pattern:**

```python
def restructure_sheet_preserve_formulas(sheet, new_data, critical_cells):
    """
    Restructure sheet while keeping critical cells in same positions
    
    Args:
        sheet: gspread worksheet object
        new_data: List of rows with new structure
        critical_cells: Dict mapping row numbers to labels (e.g., {46: 'Y0 Customers'})
    """
    
    # Step 1: Clear sheet
    sheet.clear()
    sheet.clear_basic_filter()  # Remove filters that prevent cell merging
    
    time.sleep(2)  # Avoid rate limits
    
    # Step 2: Build new data ensuring critical cells stay in same rows
    data = []
    
    # ... populate data array ...
    
    # CRITICAL: Keep linkable values in same column & row numbers
    # Example: If Assumptions references 'Sources & References'!B46,
    # ensure row 46 column B still has the customer count value
    
    for row_num, label in critical_cells.items():
        # Ensure row exists
        while len(data) < row_num:
            data.append([""] * 6)  # Add empty rows
        
        # Populate with correct value at exact position
        data[row_num - 1] = [label, value, unit, source, url, notes]
    
    # Step 3: Write all data at once
    sheet.update(range_name='A1:F200', values=data)
    
    time.sleep(2)
    
    # Step 4: Apply formatting in batch to avoid rate limits
    requests = []
    
    # Add formatting requests (colors, fonts, etc.)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": sheet.id, "startRowIndex": 0, "endRowIndex": 1},
            "cell": {"userEnteredFormat": {...}},
            "fields": "userEnteredFormat"
        }
    })
    
    # Execute all formatting at once
    spreadsheet.batch_update({"requests": requests})
```

**Real Application:** Sources & References restructure changed from 2-section layout (Section A + Section B) to unified inline format, but kept all 26 linkable values in column B at same row numbers.

---

## 4. Market Research Consolidation

**Purpose:** Aggregate multiple SERP API research files into structured summary  
**Source:** `.tmp/market_research_*.json` processing  
**Key Pattern:**

```python
def consolidate_market_research(research_dir):
    """Aggregate all market_research_*.json files"""
    
    from collections import defaultdict
    
    consolidated = {
        'tam_data': defaultdict(list),
        'competitors': defaultdict(list),
        'sources': defaultdict(list)
    }
    
    for filename in os.listdir(research_dir):
        if filename.startswith('market_research_') and filename.endswith('.json'):
            with open(os.path.join(research_dir, filename)) as f:
                data = json.load(f)
            
            # Extract category from filename
            category = filename.replace('market_research_', '').replace('.json', '')
            
            for result in data.get('organic_results', []):
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                link = result.get('link', '')
                
                # Extract market sizes using regex
                market_sizes = re.findall(
                    r'\$([0-9.]+)\s*(billion|million|B|M)(?:\s+by\s+(20\d{2}))?',
                    snippet,
                    re.IGNORECASE
                )
                
                for size, unit, year in market_sizes:
                    consolidated['tam_data'][category].append({
                        'value': f"${size}{unit}",
                        'year': year or 'current',
                        'source': title,
                        'url': link
                    })
                
                # Store all sources
                consolidated['sources'][category].append({
                    'title': title,
                    'snippet': snippet[:200],
                    'url': link
                })
    
    return consolidated
```

**Real Application:** Consolidated 10 market research files (jigs, vacuum casting, sand casting, etc.) to build comprehensive $35B-$146B TAM calculation.

---

## 5. Google Docs Batch Update Pattern

**Purpose:** Fix multiple issues in business plan document efficiently  
**Source:** `.tmp/fix_credibility_issues.py`  
**Key Pattern:**

```python
def batch_update_document(doc_id, replacements):
    """Apply multiple text replacements to Google Doc in one API call"""
    
    creds = Credentials.from_authorized_user_file("token.json", 
        scopes=["https://www.googleapis.com/auth/documents"])
    
    docs_service = build('docs', 'v1', credentials=creds)
    
    requests = []
    
    for old_text, new_text in replacements:
        requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': old_text,
                    'matchCase': True
                },
                'replaceText': new_text
            }
        })
    
    # Single API call for all replacements
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
```

**Real Application:** Fixed 5 credibility issues (math errors, timeframe labels, unsourced estimates) in single batch update.

---

## 6. Formula Verification After Restructure

**Purpose:** Verify all formulas still work after sheet restructuring  
**Source:** `.tmp/verify_linkages.py`  
**Key Pattern:**

```python
def verify_formulas_still_work(spreadsheet_id, critical_linkages):
    """
    Verify that formulas calculate correctly after restructuring
    
    Args:
        critical_linkages: Dict mapping cell refs to expected values
        Example: {'Sources & References!B46': {'label': 'Y0 Customers', 'value': 10}}
    """
    
    creds = Credentials.from_authorized_user_file("token.json", 
        scopes=["https://www.googleapis.com/auth/spreadsheets"])
    
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    issues = []
    
    for cell_ref, expected in critical_linkages.items():
        sheet_name, cell = cell_ref.split('!')
        sheet = spreadsheet.worksheet(sheet_name)
        
        # Get actual value
        actual_value = sheet.acell(cell).value
        
        # Get label from column A
        row_num = int(re.search(r'\d+', cell).group())
        label_cell = f"A{row_num}"
        actual_label = sheet.acell(label_cell).value
        
        # Verify
        if expected['label'] not in actual_label:
            issues.append({
                'cell': cell_ref,
                'expected_label': expected['label'],
                'actual_label': actual_label,
                'severity': 'CRITICAL'
            })
        
        if 'value' in expected and str(actual_value) != str(expected['value']):
            issues.append({
                'cell': cell_ref,
                'expected_value': expected['value'],
                'actual_value': actual_value,
                'severity': 'HIGH'
            })
    
    # Also check for formula errors
    for sheet in spreadsheet.worksheets():
        # Get formulas
        result = spreadsheet.values_batch_get(
            [f'{sheet.title}!A1:Z500'],
            params={'valueRenderOption': 'FORMULA'}
        )
        
        formula_data = result['valueRanges'][0].get('values', [])
        value_data = sheet.get_all_values()
        
        for i, row in enumerate(formula_data):
            for j, cell in enumerate(row):
                if cell and isinstance(cell, str) and cell.startswith('='):
                    # Check if calculated value is error
                    calc_value = value_data[i][j] if i < len(value_data) else ''
                    
                    if calc_value in ['#ERROR!', '#REF!', '#VALUE!', '#DIV/0!']:
                        issues.append({
                            'sheet': sheet.title,
                            'cell': f"{chr(65+j)}{i+1}",
                            'formula': cell,
                            'error': calc_value,
                            'severity': 'CRITICAL'
                        })
    
    return issues
```

**Real Application:** After restructuring Sources & References, verified all 26 critical cells still had correct values and Assumptions formulas calculated without errors.

---

## 7. Rate Limit Handling for Google Sheets API

**Purpose:** Avoid 429 "Quota exceeded" errors when updating sheets  
**Source:** Multiple `.tmp/fix_*.py` scripts  
**Key Pattern:**

```python
import time

def batch_format_with_rate_limiting(sheet, formatting_operations):
    """Apply formatting in batches with delays to avoid rate limits"""
    
    # Group operations into batches of 10
    batch_size = 10
    
    for i in range(0, len(formatting_operations), batch_size):
        batch = formatting_operations[i:i+batch_size]
        
        # Build batch request
        requests = []
        for op in batch:
            requests.append({
                "repeatCell": {
                    "range": op['range'],
                    "cell": {"userEnteredFormat": op['format']},
                    "fields": "userEnteredFormat"
                }
            })
        
        # Execute batch
        sheet.spreadsheet.batch_update({"requests": requests})
        
        # Wait between batches
        time.sleep(2)
    
    print(f" Applied {len(formatting_operations)} formatting operations")
```

**Common Issue:** Individual format_cell_range() calls hit write quota (60 requests/min). Solution: Batch into batch_update() calls with 2-3 second delays.

---

## 8. Standardized Color Palette

**Purpose:** Maintain consistent formatting across all sheets  
**Source:** `execution/format_sheets.py`  
**Reusable Class:**

```python
class Colors:
    """Standard color palette for business plan financial models"""
    TITLE_BLUE = (0.20, 0.30, 0.50)      # #335080 - Main titles
    DARK_BLUE = (0.20, 0.40, 0.60)       # #336699 - Section headers
    MEDIUM_BLUE = (0.40, 0.60, 0.80)     # #6699CC - Category headers
    SECTION_A_CAT = (0.30, 0.50, 0.70)   # #4D80B3 - Section A categories
    LIGHT_BLUE = (0.85, 0.92, 0.98)      # #D8EAF9 - Zebra stripe rows
    LIGHT_GRAY = (0.95, 0.95, 0.95)      # #F2F2F2 - Column headers
    URL_BLUE = (0.10, 0.30, 0.70)        # #1A4CB3 - Hyperlinks
    GREEN = (0.90, 0.97, 0.90)           # #E5F8E5 - Total/summary rows
    WHITE = (1.0, 1.0, 1.0)              # #FFFFFF - Data rows

def apply_standard_formatting(sheet):
    """Apply standard color scheme"""
    from gspread_formatting import cellFormat, color, format_cell_range
    
    # Title row
    format_cell_range(sheet, 'A1:F1', cellFormat(
        backgroundColor=color(*Colors.TITLE_BLUE),
        textFormat=textFormat(bold=True, foregroundColor=color(*Colors.WHITE), fontSize=14)
    ))
    
    # Section headers
    format_cell_range(sheet, 'A5:F5', cellFormat(
        backgroundColor=color(*Colors.SECTION_A_CAT),
        textFormat=textFormat(bold=True, foregroundColor=color(*Colors.WHITE))
    ))
    
    # Zebra striping
    for row in range(7, 100, 2):  # Every other row
        format_cell_range(sheet, f'A{row}:F{row}', cellFormat(
            backgroundColor=color(*Colors.LIGHT_BLUE)
        ))
```

---

## 9. Temporary File Management

**Best Practice:** Keep intermediates in `.tmp/`, deliverables in cloud  
**Pattern from:** Overall project structure

```
project/
 .tmp/                          # All temporary files (gitignored)
    market_research_*.json     # SERP API results
    *.py                       # One-off scripts
    *.txt                      # Cached data
 execution/                     # Reusable tools
    serp_market_research.py
    create_financial_model.py
    format_sheets.py
 directives/                    # SOPs
     business_planning.md

Deliverables (Cloud):
- Google Docs: Business Plan Document
- Google Sheets: Financial Model
- Google Slides: Pitch Deck
```

**Key Insight:** Don't create local Word/Excel files. Use cloud APIs directly so user can access deliverables immediately.

---

## 10. Self-Annealing: Learning from Errors

**Pattern:** When scripts fail, capture the fix as a reusable pattern

### Example: Percentage Formatting Bug
**Original Issue:** Percentages showed as decimals (0.1 instead of 10%)

**Debug Script:**
```python
# .tmp/check_formatting.py - identified the issue
sources_sheet.format('B70', {'numberFormat': {'type': 'NUMBER'}})  # WRONG
```

**Fix:**
```python
# Correct approach
sources_sheet.format('B70', {'numberFormat': {'type': 'PERCENT', 'pattern': '0.00%'}})
```

**Annealed Knowledge:** Added to `execution/format_sheets.py` as standard:
```python
def format_percentage_cells(sheet, cell_ranges):
    """Apply percentage formatting to multiple ranges"""
    for cell_range in cell_ranges:
        sheet.format(cell_range, {
            'numberFormat': {'type': 'PERCENT', 'pattern': '0.00%'}
        })
```

---

## Summary: Top 5 Reusable Functions

1. **find_sheet_linkages()** - Before restructuring, map all formula dependencies
2. **audit_math_calculations()** - Validate business plan calculations
3. **batch_update_with_rate_limiting()** - Avoid Google API quotas
4. **verify_formulas_still_work()** - After restructure, confirm no broken formulas
5. **consolidate_market_research()** - Aggregate SERP data into structured TAM/SAM

All patterns tested on real RapidTools business plan (35 sources, $35B-$146B TAM, 8-module product suite).
