---
type: entity
title: Zip Co
status: active
created: 2026-04-08
updated: 2026-04-08
tags:
  - entity
  - company
  - fintech
  - buy-now-pay-later
sources:
  - "[[sources/dpd-definition-data-risk]]"
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

## Relationships

- Data & Risk team: Internal team responsible for credit risk metrics and data definitions
- Customers: Segment includes both end-of-month payment cycle users (ZP/Z+) and variable due date users (ZM)

## Timeline

- Specific founding date and company history not available from current sources
- 2026-04-08: Technical documentation on DPD calculation methods captured

## Open Questions

- When was Zip Co founded?
- What is the company's market share in Australian BNPL sector?
- What other markets does Zip operate in beyond Australia?
- What is the total customer base and portfolio size?
- What regulatory framework governs Zip's operations?

## Related Pages

- [[sources/dpd-definition-data-risk]] - Technical specification for DPD tracking across Zip products
- [[concepts/days-past-due-dpd]] - Credit risk metric used to track Zip customer payment performance
- [[concepts/months-past-due-mpd]] - Reporting metric specific to Zip Pay and Zip Plus products
