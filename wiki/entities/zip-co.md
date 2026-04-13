---
type: entity
title: Zip Co
status: active
created: 2026-04-08
updated: 2026-04-13
tags:
  - entity
  - company
  - fintech
  - buy-now-pay-later
sources:
  - "[[sources/dpd-definition-data-risk]]"
  - "[[sources/zp-application-score-2022-bundle]]"
---

# Zip Co

## Summary

- Financial services company offering buy-now-pay-later (BNPL) products in Australia and other markets
- Operates multiple product lines with different payment structures and credit terms
- Uses sophisticated data systems to track payment performance and credit risk

## Key Facts

- **Product Portfolio**:
  - Zip Pay (ZP): Monthly payment product with end-of-month due date for all customers
  - Zip Plus (Z+): Monthly payment product with end-of-month due date for all customers
  - Zip Money (ZM): Product with variable due dates based on individual account opening dates
- **Market**: Australian market (AU) confirmed, likely operates in other regions
- **Technology Stack**:
  - Booking system: Tango
  - Data warehouse: Uses `prod_source` and `prod_prep` schemas
  - Key tracking table: `stg_batchoperations_account_daily_summary`
- **Credit Risk Modeling**:
  - Uses application scorecards for products such as Zip Pay
  - Internal monitoring tracks discrimination, calibration, and PSI over time
  - At least one scorecard branch shows model deterioration by 2025-Q2 and triggered a 2026 rebuild proposal

## Relationships

- Data & Risk team: Internal team responsible for credit risk metrics and data definitions
- Customers: Segment includes both end-of-month payment cycle users (ZP/Z+) and variable due date users (ZM)

## Timeline

- Specific founding date and company history not available from current sources
- 2026-04-08: Technical documentation on DPD calculation methods captured
- 2026-04-13: ZP Application Score 2022 bundle captured, including development notes, implementation logic, monitoring, and rebuild proposal

## Open Questions

- When was Zip Co founded?
- What is the company's market share in Australian BNPL sector?
- What other markets does Zip operate in beyond Australia?
- What is the total customer base and portfolio size?
- What regulatory framework governs Zip's operations?
- How many materially different internal scorecards are used across Zip products and geographies?
- Which monitoring thresholds or governance rules trigger scorecard rebuilds?

## Related Pages

- [[sources/dpd-definition-data-risk]] - Technical specification for DPD tracking across Zip products
- [[sources/zp-application-score-2022-bundle]] - Documentation bundle for Zip Pay application score development, implementation, monitoring, and proposed refresh
- [[concepts/days-past-due-dpd]] - Credit risk metric used to track Zip customer payment performance
- [[concepts/months-past-due-mpd]] - Reporting metric specific to Zip Pay and Zip Plus products
