---
type: analysis
title: CLV b-score GBIX Implementation Checklist
status: active
created: 2026-04-29
updated: 2026-04-29
tags:
  - analysis
  - credit-risk
  - modelling
  - gbix
sources:
  - "[[sources/clv-b-score-gbix-definition]]"
---

# CLV b-score GBIX Implementation Checklist

## Purpose

This checklist converts the CLV b-score GBIX definition into an implementation-oriented sequence. It should be used as a review aid when writing SQL, dbt models, notebooks, or validation tests for the sample.

## Inputs To Confirm

- Snapshot date
- Customer-account relationship table
- Account status field and valid values
- Arrears flag or DPD/arrears-balance fields at snapshot date
- Consumer attribute history table with active dates and placement dates
- Transaction history fields for first transaction, net balance, and repayments
- Performance-window account status, DPD, and attribute history for the next 12 months

## Ordered Build Steps

1. Define the snapshot cohort.
2. Select customers with at least one active, non-arrears, non-written-off, non-closed account on the snapshot date.
3. Pull all non-closed holding accounts for those customers at the snapshot date.
4. Apply customer-level exclusions from snapshot-date arrears and consumer attributes.
5. Remove account-level exclusions from the remaining holding-account set.
6. Exclude customers that have no qualified account after account-level exclusions.
7. Evaluate account-level bad cases over the next 12 months.
8. Evaluate account-level indeterminate cases over the next 12 months only for accounts not already bad.
9. Label remaining accounts good.
10. Roll account labels to customer labels by worst qualified account.

## Customer-Level Exclusion Tests

For each customer, test whether any holding account has:

- Spot written-off attribute: `203`, `7`
- Spot deceased attribute: `6`
- Ever bankruptcy attribute: `3`
- Ever Part IX attribute: `4`
- Ever Part X attribute: `214`
- Spot LOA attribute: `5`
- Spot LTA attribute: `232`
- Spot fraud attribute: `229`, `1`
- Spot suspected fraud attribute: `2`, `200`
- Spot uncontactable attribute: `9`
- Spot NFD attribute: `10`
- Spot hardship attribute: `8`
- Spot hardship pending attribute: `213`
- Spot AFCA attribute: `104`
- Spot AFCA collections attribute: `255`
- Any arrears on the snapshot date

## Account-Level Exclusion Tests

For each holding account, remove it from the qualified set when:

- `account_status = 4` on the snapshot date.
- The account never transacted before the snapshot date.
- The account was dormant for the six months before the snapshot date, with `net balance <= 0` and `total repayment <= 0`.
- All holding accounts for the customer first transacted within the six months before the snapshot date.

Do not remove recent-transacting accounts merely for being recent if the same customer has at least one holding account older than six months.

## Account-Level Outcome Tests

Bad, in order:

1. Account is written off during the next 12 months, with `account_status = 5`.
2. Account is ever `91+ DPD` during the next 12 months.

Indeterminate, in order:

1. Deceased attribute `6` during the next 12 months.
2. Bankruptcy attribute `3` during the next 12 months.
3. Fraud attribute `1` or `229` during the next 12 months.
4. LOA or LTA attribute `5` or `232` during the next 12 months.
5. Ever `3` to `90` DPD during the next 12 months.
6. Hardship or hardship pending attribute `8` or `213` during the next 12 months.
7. NFD attribute `10` during the next 12 months.

Good:

- Assign good only when none of the bad or indeterminate rules fire.

## Customer-Level Roll-Up Tests

For each customer after account-level exclusions:

- If any qualified account is bad, customer GBIX is `B`.
- Else, if any qualified account is indeterminate, customer GBIX is `I`.
- Else, customer GBIX is `G`.
- If zero qualified accounts remain, customer GBIX is `X`.

## Validation Checks

- Count customers after each exclusion step.
- Count accounts removed by each account-level exclusion rule.
- Verify no customer labelled `G`, `B`, or `I` has zero qualified accounts.
- Verify bad rules dominate indeterminate rules when both occur.
- Verify indeterminate rules dominate good labels.
- Reconcile customer-level `B` counts against accounts with written-off or `91+ DPD` outcomes.
- Reconcile customer-level `I` counts against accounts with `3` to `90` DPD or qualifying next-12-month attributes, excluding accounts already labelled bad.
- Test the six-month recency nuance with customers that have both old and recent accounts.
- Confirm which DPD field is used when product logic supports multiple DPD measures.

## Related Pages

- [[sources/clv-b-score-gbix-definition]]
- [[concepts/gbix-labeling]]
- [[concepts/clv-b-score-modeling-sample]]
- [[concepts/days-past-due-dpd]]
