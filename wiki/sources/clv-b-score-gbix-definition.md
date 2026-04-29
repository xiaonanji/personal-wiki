---
type: source
title: CLV b-score GBIX Definition
status: active
created: 2026-04-29
updated: 2026-04-29
tags:
  - source
  - finance
  - credit-risk
  - modelling
  - gbix
raw_sources:
  - raw/inbox/2026-04-29T105837+1000 CLV b-score GBIX definition - for AI to read - Data & Risk.md
---

# CLV b-score GBIX Definition

## Source Details

- Type: Internal Data & Risk model-label definition
- Source system: Confluence clip
- Source URL: `https://zip-co.atlassian.net/wiki/spaces/DATARISK/pages/4747329574/CLV+b-score+GBIX+definition+-+for+AI+to+read`
- Clipped: 2026-04-29
- Raw path: `raw/inbox/2026-04-29T105837+1000 CLV b-score GBIX definition - for AI to read - Data & Risk.md`
- Clip quality note: the raw file is a DOM-heavy Confluence clip. The substantive text is visible, but renderer markup and encoding artifacts are present in the raw source.

## Summary

This source defines the ordered GBIX labelling rules for a customer-level CLV b-score modelling sample. It explains how to pick candidate customers at a snapshot date, remove customer-level and account-level exclusions, assign account-level bad or indeterminate outcomes over a 12-month performance window, and roll account labels up to a customer-level GBIX label.

GBIX means:

- **G**: good
- **B**: bad
- **I**: indeterminate
- **X**: exclusion

The source frames GBIX as a credit-risk modelling label: for account-level modelling, each sample row represents an account; for customer-level modelling, each sample row represents a customer and the GBIX label is usually derived from all accounts held by that customer at the snapshot date.

## Overall Workflow

1. Pick a snapshot date.
2. Select customers that hold at least one active, non-arrears account on the snapshot date.
3. Gather all non-closed accounts held by those selected customers.
4. Apply customer-level exclusions.
5. Apply account-level exclusions to remove accounts from the qualified holding-account set.
6. If no qualified account remains, classify the customer as exclusion.
7. Assign account-level bad, indeterminate, or good labels using ordered 12-month outcome rules.
8. Roll account-level labels up to the customer by taking the worst qualified account label.

## Candidate Customer Selection

The initial customer selection keeps customers with at least one account that is:

- Active by account status, with `account_status` equal to `1` or `2`
- Not in arrears at the snapshot date
- Not written off at the snapshot date
- Not closed at the snapshot date

The source says this initial filter reduces data volume by removing closed, written-off, or delinquent customers before later filtering.

## Customer-Level Exclusions

A customer is classified as exclusion if any holding account has a triggering condition at the snapshot date.

### Consumer-Attribute Exclusions

The source distinguishes:

- **Spot**: the attribute is active on the snapshot date.
- **Ever**: the attribute can be active or inactive on the snapshot date, as long as it existed by the snapshot date and was not placed on the account after the snapshot date.

Customer-level exclusion attributes:

| Rule | Attribute ID(s) | Timing |
|---|---:|---|
| Written off | `203`, `7` | Spot |
| Deceased | `6` | Spot |
| Bankruptcy | `3` | Ever |
| Part IX | `4` | Ever |
| Part X | `214` | Ever |
| LOA | `5` | Spot |
| LTA | `232` | Spot |
| Fraud | `229`, `1` | Spot |
| Suspected fraud | `2`, `200` | Spot |
| Uncontactable | `9` | Spot |
| NFD | `10` | Spot |
| Hardship | `8` | Spot |
| Hardship pending | `213` | Spot |
| AFCA | `104` | Spot |
| AFCA collections | `255` | Spot |

### Arrears Exclusion

- If any holding account is in arrears on the snapshot date, the customer is classified as exclusion.

## Account-Level Exclusions

Some account-level rules remove accounts from the qualified holding-account set before bad, indeterminate, and good are derived.

Exclude an account from the qualified set if:

- The account is closed on the snapshot date, with `account_status = 4`.
- The account never transacted before the snapshot date.
- The account was dormant throughout the six months before the snapshot date, defined as `net balance <= 0` and `total repayment <= 0`.
- All of the customer's holding accounts had their first transaction within the six months before the snapshot date.

The source adds one important nuance: if the customer has any holding account older than six months, then recent-transacting accounts are not excluded merely for being recent.

The stated reason for account-level exclusions is feature quality: accounts without sufficient behavioural history should not influence derived modelling features by being mixed with more mature accounts.

## Bad, Indeterminate, And Good Ordering

After exclusions, account labels are assigned in order:

1. If an account hits any bad rule, label it **B**.
2. Otherwise, if it hits any indeterminate rule, label it **I**.
3. Otherwise, label it **G**.

Customer-level labels are then rolled up from account-level labels by worst qualified account:

1. If any qualified account is **B**, the customer is **B**.
2. Else, if any qualified account is **I**, the customer is **I**.
3. Else, the customer is **G**.

## Bad Cases

Bad cases are evaluated on each account over the next 12 months after the snapshot date:

1. Written off: the account is ever flagged as written off, with `account_status = 5`.
2. Severe delinquency: the account is ever `91+ DPD`.

## Indeterminate Cases

Indeterminate cases are evaluated on each account over the next 12 months after the snapshot date:

1. Deceased, with `attribute_id = 6`.
2. Bankruptcy, with `attribute_id = 3`.
3. Fraud, with `attribute_id` in `1`, `229`.
4. LOA or LTA, with `attribute_id` in `5`, `232`.
5. Ever `3` to `90` DPD.
6. Hardship or hardship pending, with `attribute_id` in `8`, `213`.
7. NFD, with `attribute_id = 10`.

## Good Case

An account is good if it does not hit any bad or indeterminate case after exclusions.

## Connections To Existing Pages

- Related entity: [[entities/zip-co]]
- Related concepts:
  - [[concepts/gbix-labeling]]
  - [[concepts/clv-b-score-modeling-sample]]
  - [[concepts/credit-risk-bucketing]]
  - [[concepts/days-past-due-dpd]]
- Related analysis:
  - [[analyses/clv-b-score-gbix-implementation-checklist]]

## Contradictions Or Tensions

- No direct contradiction with existing wiki material was found during ingest.
- The CLV b-score GBIX labels differ from the [[sources/zp-application-score-2022-bundle]] bad/indeterminate definitions. This appears to be a model-scope difference rather than a conflict: the CLV b-score source uses a customer-level behavioural sample with a 12-month window, while the ZP application score branch documents application-time scorecards and separate performance windows.

## Follow-Up Questions

- What exactly does "b-score" expand to in this context, and is it formally a behavioural score?
- Which products and geographies are included in the CLV b-score sample?
- What source tables implement the customer, account, attribute, arrears, and transaction-history rules?
- How is `account_status = 4` interpreted here, given other sources associate different account-status values with product-specific reporting logic?
- Is `91+ DPD` based on booking DPD, reporting DPD, or a product-specific delinquency field?
- Are the account-level dormant and recent-transacting rules implemented before or after feature derivation in the production pipeline?
