---
type: concept
title: Credit Risk Bucketing
status: active
created: 2026-04-12
updated: 2026-04-12
tags:
  - concept
  - credit-risk
  - finance
  - classification
sources:
  - "[[sources/dpd-definition-data-risk]]"
---

# Credit Risk Bucketing

## Summary

- Credit risk bucketing is the practice of grouping accounts into discrete delinquency or risk bands for reporting, monitoring, and decision-making.
- In the current wiki, the main example comes from Zip's DPD and MPD logic, where arrears amount, days or months past due, and account status jointly determine the bucket.

## Definitions

- Status bucket: category determined by non-time states such as write-off.
- Amount threshold bucket: category determined by arrears amount, such as "arrears balance <= $25."
- Time-severity bucket: category determined by how long an obligation has remained unpaid, for example 0-30 DPD or 2MPD.

## Supporting Evidence

- [[sources/dpd-definition-data-risk]] shows a production-style bucketing scheme with ordered case logic.
- The same source combines three dimensions:
  - `account_status` for write-off handling
  - `arrears_balance` for materiality thresholds
  - `arrears_days` or month-difference logic for delinquency severity
- The source also shows that bucket definitions can vary by product because the underlying delinquency metric changes from DPD to MPD.

## Counterpoints

- Fixed buckets are easy to report but can hide important variation within each band.
- Threshold choices such as `$25` are policy decisions and may not generalize across products, markets, or time periods.
- Using different time metrics across products improves fit to payment structure but makes cross-product comparison less direct.

## Related Entities

- [[entities/zip-co]]

## Related Concepts

- [[concepts/days-past-due-dpd]]
- [[concepts/months-past-due-mpd]]
- [[concepts/arrears-balance]]

## Related Analyses

- Potential analysis: compare static buckets with model-based delinquency scores
