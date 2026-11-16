# LAB 7 — Fuzz Testing with Hypothesis

## Overview

This lab uses property-based fuzz testing with Hypothesis to find and fix input-validation bugs in a Python ticketing utility. The utility validates promotional voucher codes, calculates seat prices by tier and row, and parses attendee badge data from CSV-style strings.

## Work completed

- Added Hypothesis tests that generate arbitrary text and `None` values for all three functions and check that they handle those inputs without crashing.
- Hardened voucher parsing to validate its format and discount percentage.
- Hardened seat pricing to validate the tier and row specification.
- Hardened badge parsing to validate the name, age, and seat fields.
- Added example tests for valid and invalid inputs.
- Saved screenshots of the application and pytest results before and after implementation.

## Files

| File or folder | Description |
|---|---|
| `processor.py` | Voucher, seat-price, and attendee-badge functions, plus an interactive `main()` demonstration. |
| `test_processor.py` | Hypothesis no-crash tests and example tests for valid and invalid inputs. |
| `Processor_before_implementation.png` | Screenshot of the application before the fix. |
| `Pytest_before_implementation.png` | Screenshot of failing tests before the fix. |
| `Pytest_after_implementing.png` | Screenshot of the test results after the fix. |

## Install dependencies

```bash
python -m pip install hypothesis pytest
```

## Run the application and tests

From this folder, run the interactive application:

```bash
python processor.py
```

Run the test suite:

```bash
python -m pytest -q test_processor.py
```
