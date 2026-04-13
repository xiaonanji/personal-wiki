---
type: analysis
title: ZP App Score Redevelopment Options
status: active
created: 2026-04-13
updated: 2026-04-13
tags:
  - analysis
  - finance
  - credit-risk
  - scorecard
  - model-redevelopment
sources:
  - "[[sources/zp-application-score-2022-bundle]]"
---

# ZP App Score Redevelopment Options

## Question

- Given the current ZP App Score deterioration, the availability of newer application features only in later cohorts, and the existing 9-month bad definition, what redevelopment paths are available and what are their tradeoffs?

## Current Constraints

- The current scorecard is monitored as amber on discrimination and calibration.
- The current redevelopment direction wants to consider newer application features such as employment status, time with current employer, and residential status.
- The current source bundle does not explicitly prove exactly when each new feature began populating, but the working assumption is that some of them only become available in the post-June-2025 cohort.
- The current underwriting-style target uses a 9-month performance window.
- As of 2026-04-13, a same-target redevelopment that relies on post-rollout application fields has only about 1 to 1.5 months of mature post-rollout applications if the new fields start appearing in June 2025.
- Waiting until May 2026 would likely increase that to roughly 2.5 months of mature post-rollout applications, which is still constrained but better than 1 to 1.5 months.

## Core Tension

- There is a tradeoff between target maturity and feature richness.
- Keeping the current 9-month bad definition preserves comparability with the old scorecard, but it sharply limits how much mature sample is available for newer features.
- Shortening the window to 6 months would create more sample sooner, but it would also make the target less mature and less comparable to the current underwriting score.

## Assessment Of A 6-Month Target

- The current 9-month target is already short relative to common acquisition-scorecard practice, where 12 months is often closer to the conventional window.
- Moving from 9 months to 6 months would likely capture more early-stage delinquency noise and less fully matured bad behavior.
- A shorter-window redevelopment may become better at predicting short-term payment friction rather than longer-horizon underwriting risk.
- If the bad definition also changes, for example from 61+ DPD in 9 months to a looser or earlier threshold in 6 months, then the redevelopment is no longer a like-for-like replacement of the current model.
- Conclusion: a 6-month target may still be useful for exploration or challenger work, but it is methodologically weaker as a direct replacement underwriting scorecard.

## Options

### Option 1

- Keep the current bad definition and redevelopment timing, ignore the new features, and redevelop using the stable feature set already available across the broader mature sample.

Why it helps:
- Preserves target comparability.
- Uses more mature performance data.
- Avoids rollout-driven missingness.

Main limitation:
- Cannot test or exploit the newer application features in the main redevelopment.

### Option 2

- Wait until May 2026 or later, keep the same bad definition, and redevelop using the post-rollout sample so the new features can be included.

Why it helps:
- Preserves the existing target.
- Allows direct testing of the richer application feature set.

Main limitation:
- The matured post-rollout window is still likely to be only around 2.5 months by May 2026, which may still be sample-constrained.

### Option 3

- Redevelop now but shorten the performance window, for example to 6 months, and potentially adjust the bad definition so that enough bads can be captured in the shorter horizon.

Why it helps:
- Makes more recent samples available sooner.
- Allows earlier use of newer features.

Main limitation:
- Introduces a less mature and noisier target.
- Reduces comparability with the current scorecard.

### Option 4

- Run a dual-track strategy: redevelop now with the stable feature set and current 9-month bad definition, while also building a later-cohort challenger that uses the new application features.

Why it helps:
- Keeps progress moving on a clean replacement path.
- Separately tests whether the new features are worth waiting for.
- Avoids forcing one model design to answer both the production and exploration questions.

Main limitation:
- Requires parallel model-development effort and clear governance around which track is exploratory versus production-replacement.

### Option 5

- Use a hybrid or segmented architecture: keep the main redevelopment on stable features, but add a separate model, overlay, or segment-specific challenger for cohorts where the new features are available and trusted.

Why it helps:
- Uses richer features where they exist without contaminating the broader redevelopment sample.
- Can act as an operational bridge until enough mature post-rollout data exists.

Main limitation:
- Adds operational and governance complexity.
- May be harder to explain and maintain than a single scorecard.

## Working View

- Option 1 is the cleanest immediate replacement path.
- Option 2 is the cleanest richer-feature redevelopment path, but it may still suffer from thin sample volume even after waiting.
- Option 3 is the fastest way to use the new features, but it is the weakest path if the goal is a robust like-for-like underwriting replacement.
- Option 4 is a strong compromise because it separates the production replacement question from the richer-feature learning question.
- Option 5 is most attractive when the business wants to start using new information sooner without fully committing to a thin-sample redevelopment.

## Practical Implications

- Any redevelopment using post-rollout features should be evaluated not just in months of sample, but in:
  - total applications
  - bad counts
  - exclusions-adjusted usable sample
  - stability of binning and validation
- Any shortened-window challenger should be labeled as an early-performance or exploratory model unless governance explicitly accepts it as a replacement target.
- A critical unresolved dependency is still the exact rollout timing and availability profile of the candidate new features.

## Follow-Up

- Confirm exactly which candidate features started populating after June 2025 and whether any were backfilled.
- Quantify how many usable applications and bads are available under:
  - current 9-month target now
  - current 9-month target in May 2026
  - any candidate 6-month target
- Decide whether the business needs a clean production replacement first, or whether learning the value of the new features is the more urgent question.
