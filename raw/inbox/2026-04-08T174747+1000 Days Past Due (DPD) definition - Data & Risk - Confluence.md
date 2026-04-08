## Days Past Due (DPD) definition

The reporting Days Past Due and the booking system Days Past Due can be different according to different products. The following explains the difference in details.

## Zip Pay (ZP) and Zip Plus (Z+)

These products have same due day for all customers, which is always the last day of the month. The booking system (Tango) tracks DPD as normal: DPD increases by 1 on every day past due. The reporting DPD is tracking the number of due days customer missed and is termed MPD (Months Past Due).

For example, if a customer misses the ZP/Z+ due day of Jan 31, 2026, then on Feb 1, 2026, the booking system’s DPD is 1. The reporting DPD is 1MPD. On Feb 2, 2026, the booking system’s DPD becomes 2. The reporting DPD is still 1MPD. In fact, the reporting DPD remains 1MPD till the end of Feb. If customer misses the Feb 28, 2026 due day again, then on Mar 1, 2026, the booking system’s DPD becomes 29. The reporting DPD becomes 2MPD because the customer has missed two due days (Jan 31, 2026 and Feb 28, 2026).

## Coding logic to extract the booking system DPD:

`prod_source.stg_batchoperations_account_daily_summary` table is the best source to extract the booking system DPD. To extract the DPD on Jan 31, 2026, you would filter by `arrears_date = ‘2026-02-01` as the snapshot is always as of on end of previous day’s.

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

## Coding logic to extract the reporting DPD:

```sql
select 

    batch.*,

    case when batch.account_status = 5 then 'a.WO'

         when batch.account_status <> 4 and batch.arrears_balance <= 0 then 'b.Current'

         when batch.account_status <> 4 and (batch.arrears_balance > 0 and batch.arrears_balance <= 25) then 'c.Arrears_Balance<=25'

         when batch.account_status <> 4 and (batch.arrears_balance > 25 and batch.arrears_days <= 0) then 'd.DPD<=0&Arrears_Balance>25'

         when batch.account_status <> 4 and batch.arrears_balance > 25 and datediff('month', dateadd('day', -batch.arrears_days, batch.arrears_date), dateadd(day, -1, batch.arrears_date)) = 1 then 'f.1MPD' -- Need to compare the actual month-end date

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

## Zip Money (ZM)

ZM’s due day can be on any calendar day depending on when the account is registered and open. So one ZM account could be due on 15th of every month and another could be due on 23rd of every month. Given this fact, ZM’s booking system DPD and reporting DPD are the same: just tracking the number of days post due day.

## Coding logic to extract the DPD:

```
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