---
type: concept
title: CLV b-score Modeling Sample
status: active
created: 2026-04-29
updated: 2026-04-29
tags:
  - concept
  - credit-risk
  - modelling
  - clv
  - gbix
sources:
  - "[[sources/clv-b-score-gbix-definition]]"
---

# CLV b-score Modeling Sample

## Summary

The CLV b-score modelling sample is a customer-level credit-risk modelling sample built from account holdings at a snapshot date. The source does not define the full model, feature set, or target variable beyond its GBIX labels, but it does define the sample-selection and outcome-label logic.

The sample is designed to use only customers and accounts with enough behavioural history to support modelling, while removing excluded, ambiguous, or insufficient-history cases from the clean good/bad target.

## Snapshot-Based Construction

The workflow starts with a snapshot date. Customers are initially selected if they hold at least one account that is:

- Active, with `account_status` equal to `1` or `2`
- Not in arrears
- Not written off
- Not closed

The selected customer's non-closed accounts are then gathered to derive the customer-level [[concepts/gbix-labeling|GBIX]] label.

## Exclusion Philosophy

The CLV b-score source has two layers of exclusions:

- Customer-level exclusions remove the whole customer if any holding account has a disqualifying snapshot-date condition.
- Account-level exclusions remove individual accounts from the qualified account set before outcome labels and features are derived.

The source's stated rationale is modelling feature quality: accounts with insufficient behavioural history should not be mixed into derived features.

## Customer-Level Exclusion Triggers

The customer is excluded if any holding account has:

- A snapshot-date or historical consumer attribute trigger, such as written-off, deceased, bankruptcy, Part IX, Part X, LOA, LTA, fraud, suspected fraud, uncontactable, NFD, hardship, hardship pending, AFCA, or AFCA collections.
- Any arrears on the snapshot date.

The source distinguishes "spot" attributes, which must be active on the snapshot date, from "ever" attributes, which only need to have existed by the snapshot date.

## Account-Level Qualification

Accounts are removed from the qualified holding-account set if they are closed, never transacted, dormant over the previous six months, or part of a customer relationship where all holding accounts first transacted within the previous six months.

Important nuance: if the customer has any account older than six months, then recent-transacting accounts are not excluded merely for being recent.

## Outcome Window

The bad and indeterminate outcome rules use the next 12 months after the snapshot date.

Bad account outcomes:

- Written off during the next 12 months
- Ever `91+ DPD` during the next 12 months

Indeterminate account outcomes:

- Deceased, bankruptcy, fraud, LOA, LTA, hardship, hardship pending, or NFD during the next 12 months
- Ever `3` to `90` DPD during the next 12 months

If neither bad nor indeterminate applies, the account is good.

## Open Scope Boundaries

The current source does not yet define:

- The exact CLV target or how CLV is combined with the b-score.
- Whether "b-score" formally means behavioural score.
- Product inclusion rules.
- Source tables or production SQL.
- Which DPD field should be used for products with both booking and reporting delinquency measures.

## Related Pages

- [[sources/clv-b-score-gbix-definition]]
- [[concepts/gbix-labeling]]
- [[concepts/days-past-due-dpd]]
- [[entities/zip-co]]
