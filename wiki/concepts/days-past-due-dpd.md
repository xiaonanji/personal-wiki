---
type: concept
title: Days Past Due (DPD)
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

# Days Past Due (DPD)

## Summary

- Credit risk metric tracking the number of days a payment obligation remains unpaid after its due date
- Used by financial institutions to categorize account delinquency and inform credit risk management decisions
- Can be implemented differently across products and for different reporting purposes (booking system vs regulatory reporting)

## Definitions

### Standard DPD

Tracks the cumulative number of calendar days that have elapsed since a payment became due and remains unpaid. Increases by 1 for each day past the due date.

### Product-Specific Variants

**Zip Money (ZM) DPD**:
- Booking system DPD: Standard daily increment
- Reporting DPD: Same as booking system DPD
- Due dates: Variable per account based on account opening

**Zip Pay/Plus DPD**:
- Booking system DPD: Standard daily increment
- Reporting DPD: Uses Months Past Due (MPD) - see [[concepts/months-past-due-mpd]]
- Due dates: Fixed end-of-month for all accounts

### DPD Bucketing

Common categorization ranges used in credit risk analysis:
- Current: `arrears_balance <= 0`
- Low arrears: `0 < arrears_balance <= $25`
- Early delinquency: 0-30 days
- Mid delinquency: 30-60, 60-90 days
- Late delinquency: 90-120, 120-150, 150-180 days
- Severe delinquency: 180+ days
- Write-off: Accounts charged off as uncollectible

## Supporting Evidence

### Implementation Details (from [[sources/dpd-definition-data-risk]])

- Data source: `prod_source.stg_batchoperations_account_daily_summary` table
- Key fields:
  - `arrears_date`: Snapshot date (represents end of previous day)
  - `arrears_days`: Number of days past due
  - `arrears_balance`: Outstanding overdue amount
  - `account_status`: Account state (5 = write-off, 4 = special status)
- Thresholds: $25 arrears balance used as minimum threshold for DPD bucketing

### Calculation Timing

DPD snapshots represent end-of-day state. To extract DPD for date X, filter by `arrears_date = X+1` since snapshot is as of end of previous day.

## Counterpoints

### Limitations of Standard DPD

- Does not account for payment cycle structure (monthly vs daily)
- Can misrepresent credit risk for products with monthly payment cycles
- May not align with regulatory reporting expectations for installment products

### MPD Alternative

For products with fixed monthly due dates, Months Past Due (MPD) may be more meaningful for:
- Risk reporting to regulators
- Internal credit risk assessment
- Customer communication about delinquency status

## Related Entities

- [[entities/zip-co]] - Financial services company using DPD metrics for credit risk management

## Related Concepts

- [[concepts/months-past-due-mpd]] - Alternative metric counting missed payment cycles
- [[concepts/arrears-balance]] - Amount of outstanding unpaid debt
- [[concepts/credit-risk-bucketing]] - Method of categorizing accounts by delinquency severity

## Related Analyses

- Potential analysis: Comparison of DPD vs MPD for predicting default risk
- Potential analysis: DPD bucket migration patterns over time
