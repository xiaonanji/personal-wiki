---
type: concept
title: Months Past Due (MPD)
status: active
created: 2026-04-08
updated: 2026-04-08
tags:
  - concept
  - credit-risk
  - finance
  - metrics
sources:
  - "[[sources/dpd-definition-data-risk]]"
---

# Months Past Due (MPD)

## Summary

- Variant of Days Past Due (DPD) that counts the number of monthly payment cycles missed rather than calendar days elapsed
- Specifically used for products with fixed monthly due dates where all customers share the same payment deadline
- Provides more meaningful risk assessment for monthly payment products compared to standard daily DPD tracking

## Definitions

### Core Concept

MPD increments by 1 each time a customer fails to make a required monthly payment by the due date, regardless of how many calendar days have passed.

### Zip Pay/Plus Implementation

For Zip Pay and Zip Plus products (fixed end-of-month due date):
- All customers have the same due date (last day of month)
- Booking system tracks standard DPD (daily increment)
- Reporting system tracks MPD (monthly increment)
- MPD only increments when a new monthly due date is missed

### Example Scenario

Customer misses Jan 31, 2026 payment:
- Feb 1, 2026: Booking DPD = 1, Reporting MPD = 1
- Feb 2-28, 2026: Booking DPD increases daily (2, 3, 4...), Reporting MPD remains at 1
- Mar 1, 2026 (if Feb 28 also missed): Booking DPD = 29, Reporting MPD = 2

This shows that by March 1, customer has missed two consecutive monthly obligations despite only 29 days having elapsed.

## Supporting Evidence

### Calculation Logic (from [[sources/dpd-definition-data-risk]])

SQL logic uses `datediff('month', ...)` to calculate the number of months between:
- Start date: Current date minus `arrears_days`
- End date: Current date minus 1 day

This calculates how many monthly due dates have been missed.

### MPD Buckets

- 1MPD: One monthly payment missed
- 2MPD: Two consecutive monthly payments missed
- 3MPD: Three consecutive monthly payments missed
- 4MPD, 5MPD, 6MPD: Progressive monthly misses
- 7+MPD: Seven or more monthly payments missed
- XMPD: Catch-all for edge cases where DPD exists but doesn't fit standard monthly pattern

## Counterpoints

### Product-Specific Applicability

- **Not suitable for variable due date products**: Zip Money uses individual due dates per account, making MPD calculation meaningless
- **Requires common due date**: Only applicable when all customers share the same payment cycle
- **More complex calculation**: Requires month-based date arithmetic vs simple daily increment

### Reconciliation Complexity

- Dual DPD systems (booking vs reporting) create reconciliation overhead
- Different stakeholders may reference different metrics for the same account
- Edge cases around month boundaries may need special handling (the "XMPD" bucket)

## Related Entities

- [[entities/zip-co]] - Implements MPD for Zip Pay and Zip Plus products

## Related Concepts

- [[concepts/days-past-due-dpd]] - Standard daily credit delinquency metric
- [[concepts/arrears-balance]] - Amount of outstanding debt associated with missed payments
- [[concepts/credit-risk-bucketing]] - Categorization of accounts by delinquency severity

## Related Analyses

- Potential analysis: MPD effectiveness for predicting default vs standard DPD
- Potential analysis: Optimal bucket definitions for monthly payment products
