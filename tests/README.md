# Test Suite Documentation

Automated tests for the Business Planning Agent.

## Test Files

### test_validate_config.py
Tests configuration validation logic.

**Coverage:**
- Valid configuration acceptance
- Missing required fields detection
- Invalid value ranges (tax rate, growth rates, churn)
- Revenue stream validation
- Template compatibility warnings (>6 streams)
- Market sizing consistency (TAM >= SAM >= SOM)
- Funding round validation
- CLI exit codes

**Run:**
```bash
python tests/test_validate_config.py
```

### test_template_copy.py
Tests template copy verification functionality.

**Coverage:**
- Perfect template match verification
- Missing sheets detection
- Extra sheets detection
- Wrong sheet order detection
- Formula error detection (#REF!, #VALUE!)
- Sheet structure validation

**Run:**
```bash
python tests/test_template_copy.py
```

### test_local_first.py
Tests Local-First workflow (CSV snapshot editing).

**Coverage:**
- Snapshot directory structure
- CSV formatting (values vs formulas)
- Formula syntax validation
- Balance sheet equation validation
- Batch update logic
- Formula vs value handling

**Run:**
```bash
python tests/test_local_first.py
```

## Running Tests

### Run All Tests
```bash
python tests/run_all_tests.py
python tests/run_all_tests.py --verbose
```

### Run Individual Test File
```bash
python tests/test_validate_config.py
python tests/test_template_copy.py
python tests/test_local_first.py
```

### Run with pytest (if installed)
```bash
pytest tests/ -v
pytest tests/test_validate_config.py -v
```

## Exit Codes

- **0** = All tests passed
- **1** = Some tests failed

## Test Statistics

Current test count: **20+ test cases** across 3 test files

**Breakdown:**
- Config validation: 10 test cases
- Template verification: 6 test cases
- Local-First workflow: 5 test cases

## Adding New Tests

1. Create 	ests/test_<feature>.py
2. Import unittest: import unittest
3. Create test class: class TestFeature(unittest.TestCase):
4. Add test methods: def test_something(self):
5. Add run_tests() function (see existing files)
6. Test will be auto-discovered by run_all_tests.py

## Best Practices

- Test names should be descriptive: 	est_invalid_tax_rate_detection
- Use assertions with messages: self.assertEqual(x, y, 'Should detect...')
- Mock external dependencies (Google API calls)
- Test both success and failure cases
- Document what each test validates

## Continuous Integration

To integrate with CI/CD:

```yaml
# GitHub Actions example
- name: Run tests
  run: python tests/run_all_tests.py
```

## Dependencies

Tests use Python's built-in unittest module - no external dependencies required.

Optional: Install pytest for better output:
```bash
pip install pytest
pytest tests/ -v
```
