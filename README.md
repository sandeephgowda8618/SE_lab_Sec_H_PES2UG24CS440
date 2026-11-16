# Software Engineering Lab Work

This repository contains the completed work for all five software engineering labs.

## LAB_1 - Requirements Engineering
- Requirement specification for the Alumni Mentorship & Mock Interview Platform.
- Functional and non-functional requirements covering mentor matching, mock interview scheduling, profile management, feedback, notifications, and system security.
- Includes acceptance criteria and rationale for each requirement.

## LAB_2 - Agile Project Management (Jira)
- Created a Jira project space for the Alumni Mentorship & Mock Interview Platform.
- Defined an epic, user stories, sprint planning, task tracking, and review states.
- Included active sprint management and final burn-down charts/graphs.

## LAB_3 - System Architecture Design
- Designed the platform architecture using client apps, API gateway, and microservices.
- Covered authentication, profile management, mentor matching, booking, meeting integration, recording/feedback, review, and databases.
- Included interaction with external video conferencing and notification services.

## LAB_4 - Game Development
- Built and improved a Pygame-based Coin Collector game.
- Focused on player movement, coin collection, score logic, multiple coin types, obstacles, lives, timed rounds, and game restart flow.
- Included debugging and feature enhancement using iterative development.

## LAB_5 - Static Code Analysis
- Worked on an IT Helpdesk Ticket Allocator application.
- Ran Pylint, Flake8, and Bandit to identify quality and security issues.
- Fixed major issues, documented findings, and improved the overall code quality and reliability.


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