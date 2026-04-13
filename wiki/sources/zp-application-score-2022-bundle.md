---
type: source
title: ZP Application Score 2022 Bundle
status: active
created: 2026-04-13
updated: 2026-04-13
tags:
  - source
  - finance
  - credit-risk
  - model-monitoring
  - scorecard
raw_sources:
  - raw/inbox/2026-04-13T110111+1000 ZP Application Score 2022 - Data & Risk.md
  - raw/inbox/2026-04-13T110005+1000 ZP Application Score 2022 implementation notes - Data & Risk.md
  - raw/inbox/2026-04-13T105942+1000 ZP App score monitoring report (2026-03-13) - Data & Risk.md
  - raw/inbox/2026-04-13T105829+1000 ZP App score performance deterioration fix - 2026.04 - Data & Risk.md
---

# ZP Application Score 2022 Bundle

## Source Details

- Type: Internal model documentation bundle
- Source system: Confluence clips
- Author: Data & Risk team
- Date range visible in bundle: 2022 to 2026-04
- Raw paths:
  - `raw/inbox/2026-04-13T110111+1000 ZP Application Score 2022 - Data & Risk.md`
  - `raw/inbox/2026-04-13T110005+1000 ZP Application Score 2022 implementation notes - Data & Risk.md`
  - `raw/inbox/2026-04-13T105942+1000 ZP App score monitoring report (2026-03-13) - Data & Risk.md`
  - `raw/inbox/2026-04-13T105829+1000 ZP App score performance deterioration fix - 2026.04 - Data & Risk.md`
- Clip quality note: the refreshed clips are much richer than the earlier extraction and now preserve Confluence metadata, links, attachment references, and many more rendered sections. They are still DOM-heavy clips rather than clean source exports, so they should be treated as better but not necessarily perfect captures.

## Summary

This source bundle documents the lifecycle of Zip Pay's 2022 application scorecard: original model design, implementation logic and binning, 2026 monitoring results, and an initial rebuild proposal. Together the files show a scorecard built on 2020-2021 applications, implemented as an explainable logistic regression over declared application and bureau variables, then later monitored as having weakened discrimination and calibration by 2025-Q2. The refreshed Confluence clips also preserve more exact dates, attachment references, and source links than the earlier extraction.

## Key Claims

- **Model purpose**: The score predicts likelihood of default at application time using declared customer data plus bureau variables.
- **Development window**: The original development sample uses applications from April 2020 to March 2021 with a 9-month performance window.
- **Bad definition**: The model treats 2+ MPD, bankruptcy, hardship, Part IX, Part X, LOA, or LTA as bad outcomes.
- **Outcome framework is three-way before exclusions**: the original document explicitly distinguishes bad, indeterminate, and good before applying exclusions.
- **Implementation is explicit**: The implementation notes preserve feature logic, bin definitions, DBT column mappings, and coefficient-level score contributions.
- **Monitoring shows deterioration**: The 2026-03-13 monitoring report rates discrimination and calibration as amber for ZP App Score 2022.
- **Distribution shift looks limited**: PSI is reported as 0.02635, which remains green under the monitoring thresholds.
- **Rebuild direction is recency plus feature transfer**: The deterioration note proposes retraining on Jan 2025 to Jun 2025 applications and exploring selected ZM app-model features for ZP.
- **Post-June-2025 feature-availability issue is not explicit in the clipped docs**: the rebuild note names candidate new features, but the current source bundle does not explicitly say which of them only began populating after June 2025.

## Notable Evidence

### Original model structure

- Model type: logistic regression chosen for explainability.
- Variable families include applicant age, application timing, direct vs merchant flag, time at address, time at employer, bureau enquiries, defaults, and judgements.
- The raw source includes coefficient and observed/expected bad-rate tables for the binned variables.

### Original model sample and labels

- Sample window: applications between April 2020 and March 2021.
- Performance window: outcomes assessed 9 months after application date.
- Bad definition: 2+ MPD, bankruptcy, hardship, Part IX, Part X, LOA, or LTA.
- Indeterminate definition: 1+ MPD, no transactions, or no transactions within 2 months after registration.
- Good definition: transacted and never delinquent.
- Exclusions: declined, approved but not registered, fraud, Veda score missing, or Veda score below 350.

### Features visible in the original scorecard

- `app_age`
- `app_AppTime_hour`
- `app_Flag_Direct`
- `veda_time_at_address`
- `veda_time_at_employer`
- `veda_tot_no_non_tlu_enquiries_01`
- `veda_tot_no_non_tlu_enquiries_12`
- `veda_Num_Payday_Enq_12`
- `veda_Flag_Enquiry_Real_Estate_Mortgage`
- `veda_time_since_last_default`
- `veda_total_value_outstanding_non_tlu_defaults`
- `veda_total_value_outstanding_tlu_defaults`
- `veda_judgements`

### Implementation detail preserved in raw source

- `app_age` is derived from application timestamp minus date of birth.
- `app_time` is bucketed as `"Night"` when the application hour is before 5 AM, otherwise `"Other"`.
- `ZP_APP_2022_*` DBT column names are mapped to each engineered feature and bin set in the implementation note.

```python
app_time = datetime.strptime(data_df["application_createdTimestamp"][0], "%Y-%m-%d %H:%M:%S").date()
dob = datetime.strptime(data_df["applicant_dateOfBirth"][0], "%Y-%m-%d").date()
application_features["app_age"] = (app_time - dob).days / 365.25
```

```python
"Night" if datetime.strptime(x, "%Y-%m-%d %H:%M:%S").hour < 5 else "Other"
```

### Monitoring snapshot

- Full performance sample period: 2024-06-13 to 2025-06-13, labeled as 2024-Q2 to 2025-Q2.
- Full performance bad definition: 61+ DPD or bankruptcy / Part IX / Part X / hardship / LTA / LOA in the next 9 months.
- Early performance sample period: 2025-09-13 to 2025-12-13.
- Early performance bad definition: 61+ DPD or bad attributes in the next 3 months.
- PSI baseline sample period: 2023-04-01 to 2023-06-30.
- Most recent 3 months for PSI: 2025-12-13 to 2026-03-13.
- Latest monitored AUC for 2025-Q2: `0.6502` versus development benchmark `0.75`, rated amber.
- Latest calibration ratio for 2025-Q2: `63.16%`, rated amber.
- PSI for recent 3 months vs base: `0.02635`, rated green.
- Monitoring note referenced by the deterioration document says 7 of 13 variables have become unpredictable.
- The monitoring page also notes: `Dev training data is Nov 2019 - Oct 2020`.

### Proposed refresh direction

- Development sample recency is the first stated problem: April 2020 to March 2021 is described as outdated.
- Rebuild proposal keeps the same GBIX but moves the sample window to Jan 2025 to Jun 2025 with performance observed up to 2026-03-31.
- Candidate feature imports from ZM include employment status, time with current employer, residential status, and bureau-file age.
- Based on the clip alone, these candidate features are visible, but the exact rollout timing or population-start date for each field is not yet stated explicitly.

## Connections To Existing Pages

- Related entity: [[entities/zip-co]]
- Related concepts:
  - [[concepts/days-past-due-dpd]]
  - [[concepts/months-past-due-mpd]]
- Related analysis:
  - [[analyses/zp-app-score-redevelopment-options]]

## Contradictions Or Tensions

- The original model documentation presents the 2022 scorecard as well-calibrated and monotonic in development, but the later monitoring document shows weaker discrimination and calibration by 2025-Q2. This is not a direct contradiction, but it is an important temporal deterioration that should shape future synthesis.
- The source bundle contains a date tension: the original model page describes a sample window of April 2020 to March 2021, while the monitoring page separately notes `Dev training data is Nov 2019 - Oct 2020`. This may reflect a distinction between training data and the broader modeling/evaluation sample, but the current clips do not explain it directly.
- The rebuild page names candidate additional features, but the refreshed clips still do not explicitly document which ones only became available after June 2025.

## Follow-Up Questions

- What exactly are the 7 of 13 variables now considered unpredictable, and by which stability metric?
- How much of the deterioration comes from population drift versus changing underwriting or customer behavior?
- Was the proposed 2026 rebuild ever implemented, and if so how did it compare with the 2022 score?
- Which of the candidate added features were only populated after June 2025, and were any of them backfilled?
- Should this wiki add a dedicated concept page for application scorecards or score monitoring in the Zip/Data & Risk branch?
