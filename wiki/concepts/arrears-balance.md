---
type: concept
title: Arrears Balance
status: active
created: 2026-04-08
updated: 2026-04-08
tags:
  - concept
  - credit-risk
  - finance
  - accounting
sources:
  - "[[sources/dpd-definition-data-risk]]"
---

# Arrears Balance

## Summary

- The monetary amount of debt that remains unpaid after the payment due date has passed
- Distinct from Days Past Due (DPD), which measures time elapsed rather than amount owed
- Used as a threshold criterion in credit risk bucketing alongside DPD metrics

## Definitions

### Core Concept

Arrears balance represents the dollar value of obligations that are overdue. An account can have:
- **Zero arrears balance**: All payments current or ahead of schedule
- **Positive arrears balance**: Outstanding amount past due
- **Different arrears balance vs total balance**: Arrears is specifically the overdue portion

### Threshold Usage

In Zip's credit risk framework (from [[sources/dpd-definition-data-risk]]):
- **$25 threshold**: Key breakpoint in bucketing logic
- Accounts with `arrears_balance <= $25` are treated differently than those above $25
- Even with positive DPD, accounts under $25 arrears may receive special treatment

## Supporting Evidence

### Risk Bucketing Logic

Credit risk categories from Zip implementation:
1. **Current**: `arrears_balance <= 0` (no overdue amount)
2. **Low arrears**: `0 < arrears_balance <= $25` (small overdue amount)
3. **Arrears above $25 with no DPD**: `arrears_balance > $25 AND arrears_days <= 0` (unusual state)
4. **Standard DPD buckets**: `arrears_balance > $25 AND arrears_days > 0` (normal delinquency progression)

### Combined Metrics

Arrears balance is used in conjunction with:
- `arrears_days`: DPD or MPD time metric
- `account_status`: Account state flags (write-off, closed, etc.)
- Product type: Different thresholds may apply to different products

## Counterpoints

### Limitations

- **Dollar value can be misleading**: $100 arrears may be significant for small credit limits but trivial for large ones
- **Does not capture payment history**: A customer who frequently goes into arrears but pays quickly has the same arrears balance as one who never pays
- **Currency and jurisdiction dependent**: $25 threshold makes sense in AU context but may not translate to other markets

### Relative vs Absolute Metrics

- Absolute dollar thresholds ($25) are simpler to implement
- Relative metrics (% of credit limit or % of balance) might be more risk-predictive
- Fixed thresholds may need periodic adjustment for inflation

## Related Entities

- [[entities/zip-co]] - Uses arrears balance thresholds in credit risk bucketing

## Related Concepts

- [[concepts/days-past-due-dpd]] - Time-based delinquency metric used alongside arrears balance
- [[concepts/months-past-due-mpd]] - Alternative time metric for monthly payment products
- [[concepts/credit-risk-bucketing]] - Categorization framework using both time and amount thresholds

## Related Analyses

- Potential analysis: Optimal arrears balance thresholds for different credit products
- Potential analysis: Correlation between arrears balance and eventual default rates
