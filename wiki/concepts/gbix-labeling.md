---
type: concept
title: GBIX Labeling
status: active
created: 2026-04-29
updated: 2026-04-29
tags:
  - concept
  - credit-risk
  - modelling
  - classification
  - gbix
sources:
  - "[[sources/clv-b-score-gbix-definition]]"
---

# GBIX Labeling

## Summary

GBIX is an ordered modelling-label framework used in credit-risk sample construction. Each record is classified as one of:

- **G**: good
- **B**: bad
- **I**: indeterminate
- **X**: exclusion

The labels are not just descriptive buckets. They determine which observations are usable for model training or evaluation and how ambiguous outcomes are handled.

## Core Pattern

The source shows a common ordered pattern:

1. Identify exclusions first.
2. On the remaining qualified records, identify bad outcomes.
3. If not bad, identify indeterminate outcomes.
4. If neither bad nor indeterminate, classify as good.

This order matters because later categories are residual. Good means "did not meet exclusion, bad, or indeterminate rules," not simply "had positive behaviour."

## Grain

GBIX can be applied at different modelling grains:

- Account-level modelling: each sample row is an account, and the GBIX label belongs to the account.
- Customer-level modelling: each sample row is a customer, and the GBIX label is derived from the customer's holding accounts at the snapshot date.

In the CLV b-score source, the modelling grain is customer-level, but the bad and indeterminate logic is defined at account level and then rolled up.

## Customer-Level Roll-Up

For customer-level modelling, the source uses worst-qualified-account roll-up:

1. If any qualified holding account is bad, the customer is bad.
2. Else, if any qualified holding account is indeterminate, the customer is indeterminate.
3. Else, the customer is good.

Exclusion can occur before this roll-up if the customer hits customer-level exclusion rules, or after account-level exclusions if no qualified holding account remains.

## Why Indeterminate Exists

Indeterminate separates ambiguous or not-cleanly-modelled outcomes from both bad and good. In the CLV b-score source, examples include moderate delinquency (`3` to `90` DPD) and attributes such as deceased, bankruptcy, fraud, LOA, LTA, hardship, and NFD during the performance window.

This avoids forcing ambiguous, administrative, hardship, or incomplete-performance cases into the binary target.

## Relationship To Credit Risk Bucketing

GBIX is related to [[concepts/credit-risk-bucketing]], but it serves a different purpose:

- Credit risk bucketing groups accounts for reporting, monitoring, and operational interpretation.
- GBIX labeling constructs model-development samples and targets.

Both rely on ordered rules, account statuses, attributes, arrears or delinquency measures, and time windows.

## Related Pages

- [[sources/clv-b-score-gbix-definition]]
- [[concepts/clv-b-score-modeling-sample]]
- [[concepts/credit-risk-bucketing]]
- [[concepts/days-past-due-dpd]]
