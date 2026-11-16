# LAB 6 — Code and Branch Coverage

## Overview

This lab applies pytest coverage techniques to an event ticket processing program. The program calculates ticket revenue for VIP, Premium, and General tiers; applies promotional discounts, bulk-order discounts, service tax, and an optional lounge fee; flags batches with too many rejected orders; and monitors turnstile flow for congestion.

## Work completed

- Added pytest cases for valid and invalid ticket manifests, ticket tiers, order quantities, promotions, taxes, lounge fees, audit rejection, and gate-flow outcomes.
- Created separate test suites for line coverage and branch coverage.
- Captured screenshots showing coverage before and after adding tests, along with a full pytest run.

## Files

| File or folder | Description |
|---|---|
| `event_ticket_tier.py` | Ticket revenue and gate-flow functions under test. |
| `CodeCoverageTest_event_ticket_tier.py` | Tests for normal and edge-case behavior to exercise code lines. |
| `BranchCoverageTest_event_ticket_tier.py` | Tests that exercise decision branches, including discounts, fraud handling, and congestion detection. |
| `ScreenShots/` | Before-and-after line and branch coverage screenshots, plus the full pytest result. |
| `PES2UG24CS440_LAB_06.pdf` | Lab handout/reference document. |

## Run the tests

From this folder, run:

```bash
python -m pytest
```

Run an individual suite with:

```bash
python -m pytest CodeCoverageTest_event_ticket_tier.py
python -m pytest BranchCoverageTest_event_ticket_tier.py
```
