---
type: source
title: Days Past Due (DPD) Definition - Data & Risk
status: active
created: 2026-04-08
updated: 2026-04-08
tags:
  - source
  - finance
  - credit-risk
  - data-definition
raw_source: raw/inbox/2026-04-08T174747+1000 Days Past Due (DPD) definition - Data & Risk - Confluence.md
---

# Days Past Due (DPD) Definition - Data & Risk

## Source Details

- Type: Technical documentation (Confluence)
- Author: Data & Risk team
- Date: 2026-04-08
- Raw path: `raw/inbox/2026-04-08T174747+1000 Days Past Due (DPD) definition - Data & Risk - Confluence.md`

## Summary

Technical specification document explaining how Days Past Due (DPD) is calculated differently across Zip products (Zip Pay, Zip Plus, and Zip Money) for both booking system and reporting purposes. The document provides SQL code examples for extracting DPD metrics from the booking system database.

## Key Claims

- **Product-specific DPD tracking**: Different Zip products have different DPD calculation methods based on their payment structures
- **Dual DPD systems**: Booking system DPD and reporting DPD can differ for the same account
- **Zip Pay/Plus use MPD (Months Past Due)**: For reporting purposes, these products track missed monthly due dates rather than daily arrears
- **Zip Money uses standard DPD**: Both booking and reporting systems track daily arrears for Zip Money
- **Common due date for ZP/Z+**: All Zip Pay and Zip Plus customers share the same due date (last day of month)
- **Variable due dates for ZM**: Zip Money accounts have individual due dates based on account opening

## Notable Evidence

### Zip Pay/Plus DPD Example

If a customer misses Jan 31, 2026 due date:
- Feb 1, 2026: Booking DPD = 1, Reporting DPD = 1MPD
- Feb 2, 2026: Booking DPD = 2, Reporting DPD = 1MPD (remains)
- If Feb 28 also missed, Mar 1: Booking DPD = 29, Reporting DPD = 2MPD

### Data Source

Best source for booking system DPD: `prod_source.stg_batchoperations_account_daily_summary` table
- Note: `arrears_date` snapshot is end of previous day

### DPD Bucket Definitions

Standard buckets used across all products:
- Write-off (WO): `account_status = 5`
- Current: `arrears_balance <= 0`
- Arrears Balance ≤25: `0 < arrears_balance <= 25`
- Various DPD ranges: (0,30), [30,60), [60,90), [90,120), [120,150), [150,180), ≥180

### SQL Implementation Examples

**Booking System DPD (All Products)**

```sql
select
    batch.*,
    case when batch.account_status = 5 then 'a.WO'
         when batch.account_status <> 4 and batch.arrears_balance <= 0 then 'b.Current'
         when batch.account_status <> 4 and (batch.arrears_balance > 0 and batch.arrears_balance <= 25) then 'c.Arrears_Balance<=25'
         when batch.account_status <> 4 and (batch.arrears_balance > 25 and batch.arrears_days <= 0) then 'd.DPD<=0&Arrears_Balance>25'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days > 0 and batch.arrears_days < 30 then 'f.(0,30)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 30 and batch.arrears_days < 60 then 'g.[30,60)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 60 and batch.arrears_days < 90 then 'h.[60,90)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 90 and batch.arrears_days < 120 then 'i.[90,120)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 120 and batch.arrears_days < 150 then 'j.[120,150)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 150 and batch.arrears_days < 180 then 'k.[150,180)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 180 then 'l.>=180DPD'
    end as dpd_bucket
from prod_source.stg_batchoperations_account_daily_summary batch
```

**Reporting DPD for Zip Pay/Plus (MPD-based)**

```sql
select
    batch.*,
    case when batch.account_status = 5 then 'a.WO'
         when batch.account_status <> 4 and batch.arrears_balance <= 0 then 'b.Current'
         when batch.account_status <> 4 and (batch.arrears_balance > 0 and batch.arrears_balance <= 25) then 'c.Arrears_Balance<=25'
         when batch.account_status <> 4 and (batch.arrears_balance > 25 and batch.arrears_days <= 0) then 'd.DPD<=0&Arrears_Balance>25'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and datediff('month', dateadd('day', -batch.arrears_days, batch.arrears_date), dateadd(day, -1, batch.arrears_date)) = 1 then 'f.1MPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and datediff('month', dateadd('day', -batch.arrears_days, batch.arrears_date), dateadd(day, -1, batch.arrears_date)) = 2 then 'g.2MPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and datediff('month', dateadd('day', -batch.arrears_days, batch.arrears_date), dateadd(day, -1, batch.arrears_date)) = 3 then 'h.3MPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and datediff('month', dateadd('day', -batch.arrears_days, batch.arrears_date), dateadd(day, -1, batch.arrears_date)) = 4 then 'i.4MPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and datediff('month', dateadd('day', -batch.arrears_days, batch.arrears_date), dateadd(day, -1, batch.arrears_date)) = 5 then 'j.5MPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and datediff('month', dateadd('day', -batch.arrears_days, batch.arrears_date), dateadd(day, -1, batch.arrears_date)) = 6 then 'k.6MPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and datediff('month', dateadd('day', -batch.arrears_days, batch.arrears_date), dateadd(day, -1, batch.arrears_date)) >= 7 then 'l.>=7MPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days > 0 then 'e.XMPD'
    end as dpd_bucket
from prod_source.stg_batchoperations_account_daily_summary batch
join prod_prep.dim_account acct on batch.account_id = acct.account_id
where acct.product in ('Zip Pay','Zip Plus') and acct.product_country = 'AU';
```

**Reporting DPD for Zip Money (Standard DPD)**

```sql
select
    batch.*,
    case when batch.account_status = 5 then 'a.WO'
         when batch.account_status <> 4 and batch.arrears_balance <= 0 then 'b.Current'
         when batch.account_status <> 4 and (batch.arrears_balance > 0 and batch.arrears_balance <= 25) then 'c.Arrears_Balance<=25'
         when batch.account_status <> 4 and (batch.arrears_balance > 25 and batch.arrears_days <= 0) then 'd.DPD<=0&Arrears_Balance>25'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days > 0 and batch.arrears_days < 30 then 'f.(0,30)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 30 and batch.arrears_days < 60 then 'g.[30,60)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 60 and batch.arrears_days < 90 then 'h.[60,90)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 90 and batch.arrears_days < 120 then 'i.[90,120)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 120 and batch.arrears_days < 150 then 'j.[120,150)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 150 and batch.arrears_days < 180 then 'k.[150,180)DPD'
         when batch.account_status <> 4 and batch.arrears_balance > 25 and batch.arrears_days >= 180 then 'l.>=180DPD'
    end as dpd_bucket
from prod_source.stg_batchoperations_account_daily_summary batch
join prod_prep.dim_account acct on batch.account_id = acct.account_id
where acct.product = 'Zip Money' and acct.product_country = 'AU';
```

## Connections

- Related entities: [[entities/zip-co]] (financial services company, products include Zip Pay, Zip Plus, Zip Money)
- Related concepts:
  - [[concepts/days-past-due-dpd]] (credit risk metric tracking payment delinquency)
  - [[concepts/months-past-due-mpd]] (variant DPD metric counting missed payment cycles)
  - [[concepts/arrears-balance]] (outstanding unpaid amount past due)
- Related analyses: Potential analysis on credit risk bucketing strategies

## Contradictions Or Tensions

None identified in this source. The document is internally consistent technical specification.

## Follow-Up Questions

- What business logic drove the decision to use MPD for Zip Pay/Plus reporting vs standard DPD?
- How do regulatory reporting requirements differ between MPD and DPD approaches?
- What is the historical default rate correlation with MPD vs DPD metrics?
- Are there edge cases where the `arrears_date` snapshot timing creates data quality issues?
