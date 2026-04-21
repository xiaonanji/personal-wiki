---
type: meta
title: Log
status: active
created: 2026-04-06
updated: 2026-04-21
---

# Log

Append-only record of major wiki operations.

## [2026-04-06] bootstrap | Initialize LLM wiki scaffold

- Created the base repository structure for raw sources, wiki pages, templates, and scripts.
- Added `AGENTS.md` to define ingest, query, and lint workflows.
- Added starter pages for index, home, logging, contradictions, and open questions.

## [2026-04-06] ingest | The 2028 Global Intelligence Crisis

- Ingested the translated clip in `raw/inbox/` and mapped it into one source page, four concept pages, and two entity pages.
- Captured the source's core mechanisms: AI efficiency paradox, ghost GDP, agentic disintermediation, and the intelligence displacement spiral.
- Added reliability notes because the source is explicitly a thought experiment but presents hypothetical datapoints in a reporting style.
- Pages touched: `wiki/sources/2028-global-intelligence-crisis.md`, `wiki/concepts/ai-efficiency-paradox.md`, `wiki/concepts/ghost-gdp.md`, `wiki/concepts/agentic-disintermediation.md`, `wiki/concepts/intelligence-displacement-spiral.md`, `wiki/entities/alap-shah.md`, `wiki/entities/citrini-research.md`, `wiki/index.md`, `wiki/home.md`, `wiki/meta/open-questions.md`, `wiki/meta/contradictions.md`.
- Follow-ups: locate the original English source and test this scenario against more empirical labor, software, and housing evidence.

## [2026-04-06] ingest | Stable Performance Is Key to Winning

- Ingested the second clip in `raw/inbox/` and filed it as a performance/decision-making source rather than merging it into the AI macro branch.
- Created concept pages for small-edge compounding and point-by-point reset, plus an entity page for Roger Federer as the source's anchor example.
- Updated the index, home page, and open questions to reflect the new performance branch.
- Pages touched: `wiki/sources/stable-performance-is-key-to-winning.md`, `wiki/concepts/small-edge-compounding.md`, `wiki/concepts/point-by-point-reset.md`, `wiki/entities/roger-federer.md`, `wiki/index.md`, `wiki/home.md`, `wiki/meta/open-questions.md`.
- Follow-ups: verify the original Federer quote/statistic and test whether more sources should grow this into a larger personal-performance cluster.

## [2026-04-06] ingest | Agent Skills Sources

- Ingested two skill-related inbox sources: one conceptual overview of skills and one implementation guide for adding skill support to an agent.
- Created source pages, concept pages for agent skills and progressive disclosure, and a durable implementation checklist under analyses.
- Updated the index, home page, and open questions to reflect a new agent-skills branch in the wiki.
- Pages touched: `wiki/sources/what-are-skills.md`, `wiki/sources/adding-skills-support-to-an-agent.md`, `wiki/concepts/agent-skills.md`, `wiki/concepts/progressive-disclosure-for-skills.md`, `wiki/concepts/skill-support-integration.md`, `wiki/analyses/agent-skills-support-checklist.md`, `wiki/index.md`, `wiki/home.md`, `wiki/meta/open-questions.md`.
- Follow-ups: decide whether this repo should capture concrete skill-client design choices and which trust/discovery rules matter for future implementations.

## [2026-04-06] ingest | Titanic Dataset

- Ingested a compact dataset-description source for the Titanic survival prediction task and filed it as a new machine-learning dataset branch.
- Created a source page, a lightweight RMS Titanic entity page, a concept page for the prediction task, and a reusable feature-summary analysis.
- Updated the index, home page, and open questions to reflect the new dataset branch.
- Pages touched: `wiki/sources/titanic-dataset.md`, `wiki/entities/rms-titanic.md`, `wiki/concepts/titanic-survival-prediction-task.md`, `wiki/analyses/titanic-dataset-feature-summary.md`, `wiki/index.md`, `wiki/home.md`, `wiki/meta/open-questions.md`.
- Follow-ups: retrieve the full Kaggle schema and decide whether more ML/dataset sources justify a larger branch.

## [2026-04-06] ingest | Titanic Dataset (updated source)

- Re-ingested the modified Titanic raw source and updated the existing Titanic pages in place rather than creating duplicates.
- Captured two newly visible fields in the raw source: `Cabin` and embarkation port (`Embarked`, spelled `Emarked` in the clip).
- Narrowed the old uncertainty from "confirm which columns are omitted" to "confirm whether any important columns are still omitted."
- Pages touched: `wiki/sources/titanic-dataset.md`, `wiki/concepts/titanic-survival-prediction-task.md`, `wiki/analyses/titanic-dataset-feature-summary.md`, `wiki/meta/open-questions.md`.

## [2026-04-08] ingest | Days Past Due (DPD) Definition - Data & Risk

- Ingested technical Confluence documentation on DPD calculation methodology for Zip products.
- Created a new fintech/credit-risk branch in the wiki with focus on payment delinquency metrics.
- Created one source page, one entity page (Zip Co), and three concept pages (DPD, MPD, Arrears Balance).
- Key insight: Zip uses dual DPD systems - booking system (daily) vs reporting system (monthly for some products).
- Documented product-specific differences: Zip Pay/Plus use MPD for reporting, Zip Money uses standard DPD.
- Captured SQL implementation logic and bucketing thresholds ($25 arrears balance, various DPD ranges).
- Pages touched: `wiki/sources/dpd-definition-data-risk.md`, `wiki/entities/zip-co.md`, `wiki/concepts/days-past-due-dpd.md`, `wiki/concepts/months-past-due-mpd.md`, `wiki/concepts/arrears-balance.md`, `wiki/index.md`, `wiki/log.md`.
- Follow-ups: investigate business rationale for MPD vs DPD choice, compare default prediction performance between metrics, understand regulatory reporting requirements.

## [2026-04-12] ingest | Context Management for Deep Agents

- Ingested the newest unfiled inbox source, an engineering note about context compression in LangChain's Deep Agents SDK.
- Created a new source page, a product entity page for Deep Agents SDK, a concept page for agent context compression, and a reusable evaluation checklist.
- Updated the existing agent-skills branch so "context maintenance" now points to concrete offloading and summarization patterns rather than staying abstract.
- Updated the home page, index, and open questions to reflect a new long-running-agent context-management branch.
- Pages touched: `wiki/sources/context-management-for-deep-agents.md`, `wiki/entities/deep-agents-sdk.md`, `wiki/concepts/agent-context-compression.md`, `wiki/concepts/skill-support-integration.md`, `wiki/analyses/agent-context-compression-evaluation-checklist.md`, `wiki/analyses/agent-skills-support-checklist.md`, `wiki/home.md`, `wiki/index.md`, `wiki/meta/open-questions.md`.
- Follow-ups: compare filesystem-backed compression with other memory patterns, and decide which context-compression guarantees should become baseline expectations for future agent implementations in this wiki.

## [2026-04-12] lint | Fix broken credit-risk bucketing links

- Ran the repo lint during ingest verification and found three broken links to `[[concepts/credit-risk-bucketing]]`.
- Added the missing concept page and updated the index so the existing credit-risk pages now resolve cleanly.
- Pages touched: `wiki/concepts/credit-risk-bucketing.md`, `wiki/index.md`.
- Follow-ups: run broader wiki health checks periodically so small structural gaps do not accumulate between ingests.

## [2026-04-12] query | Compression vs Intelligence in Agents

- Filed a durable analysis in response to the distinction between context preservation and actual intelligence formation.
- Argued that offloading and summarization support continuity, while stronger abstraction-oriented compression is needed to convert history into reusable knowledge or policy.
- Pages touched: `wiki/analyses/compression-vs-intelligence-in-agents.md`, `wiki/index.md`.
- Follow-ups: compare transcript summaries with stronger compression targets such as task-state objects, knowledge graphs, and distilled playbooks.

## [2026-04-12] query | Personal Small Model Plus Cloud Frontier Model

- Filed a durable analysis for the proposed architecture where each user has a local small model that compresses personal history and collaborates with a cloud frontier model.
- Framed the pattern as a division of labor: local compression, privacy, and preference modeling plus cloud-scale reasoning and world knowledge.
- Pages touched: `wiki/analyses/personal-small-model-plus-cloud-frontier-model.md`, `wiki/index.md`.
- Follow-ups: define which user data should remain raw memory versus distilled model state, and compare parameter-based personalization against structured non-parametric memory systems.

## [2026-04-12] ingest | LangChain MCP Adapters

- Ingested documentation for the `langchain-mcp-adapters` library as a new MCP interoperability branch under the agent/tooling area of the wiki.
- Created a source page that preserves the source's Python and config examples, plus a library entity page, a concept page for MCP-to-LangChain adaptation, and a reusable integration checklist.
- Updated the home page, index, and open questions to reflect a new focus area around MCP, LangChain, and LangGraph interoperability.
- Pages touched: `wiki/sources/langchain-mcp-adapters.md`, `wiki/entities/langchain-mcp-adapters.md`, `wiki/concepts/mcp-to-langchain-adaptation.md`, `wiki/analyses/langchain-mcp-adapters-integration-checklist.md`, `wiki/home.md`, `wiki/index.md`, `wiki/meta/open-questions.md`.
- Follow-ups: compare adapter-based MCP integration against native framework tools, and clarify which transport/session patterns are appropriate for production deployments.

## [2026-04-13] ingest | ZP Application Score 2022 Bundle

- Scanned the latest raw inbox resources and grouped four related Zip Pay application-score documents into a single source bundle for reuse.
- Captured the scorecard lifecycle from original 2022 design and implementation through 2026 monitoring and a proposed rebuild path.
- Updated the Zip Co entity and open questions so future work can branch into scorecard governance, drift, and rebuild outcomes.
- Pages touched: `wiki/sources/zp-application-score-2022-bundle.md`, `wiki/entities/zip-co.md`, `wiki/index.md`, `wiki/meta/open-questions.md`, `wiki/log.md`.
- Follow-ups: identify the unstable variables, confirm whether the rebuild shipped, and decide whether to split this branch into dedicated concept or analysis pages later.

## [2026-04-13] ingest | ZP Application Score 2022 Bundle (refreshed clips)

- Re-ingested the four ZP App Score raw resources after a richer Confluence re-extraction replaced the earlier clipped markdown.
- Updated the existing source bundle in place with the new raw filenames, more precise monitoring dates, the full three-way outcome labeling, the explicit 13-feature set, and a clip-quality caveat.
- Preserved the remaining uncertainty that the refreshed clips still do not explicitly identify which new redevelopment features only started populating after June 2025.
- Pages touched: `wiki/sources/zp-application-score-2022-bundle.md`, `wiki/log.md`.
- Follow-ups: confirm feature rollout timing from a fuller export or source-of-truth table, and decide whether to add a dedicated redevelopment analysis page once the availability issue is resolved.

## [2026-04-13] query | ZP App Score Redevelopment Options

- Filed a durable analysis that captures the redevelopment tradeoffs around same-target rebuilding, waiting for more mature post-rollout sample, shortening the performance window, running dual tracks, and using hybrid segmentation.
- Explicitly recorded the concern that a 6-month target is likely too immature and noisy to serve as a clean like-for-like underwriting replacement, even if it is useful for challenger work.
- Updated the source bundle connections, open questions, and index so this redevelopment reasoning is discoverable alongside the underlying ZP score documentation.
- Pages touched: `wiki/analyses/zp-app-score-redevelopment-options.md`, `wiki/sources/zp-application-score-2022-bundle.md`, `wiki/meta/open-questions.md`, `wiki/index.md`, `wiki/log.md`.
- Follow-ups: confirm post-June-2025 feature rollout timing, estimate bad counts under each candidate sample design, and decide whether the near-term priority is a clean replacement or a richer-feature challenger.

## [2026-04-21] ingest | Change Management Wiki

- Ingested the new `raw/inbox/Change Management Wiki/` bundle as a practical organizational-change playbook rather than copying each raw page into a one-to-one wiki mirror.
- Created one bundled source note, three reusable concept pages, and one checklist analysis covering the lifecycle from change framing through sponsorship, rollout, launch readiness, and post-launch adoption monitoring.
- Recorded that the markdown bundle cites `Change management template.pdf`, but that upstream PDF was not present anywhere under `raw/` at ingest time.
- Pages touched: `wiki/sources/change-management-wiki-bundle.md`, `wiki/concepts/organizational-change-management.md`, `wiki/concepts/change-sponsorship-and-governance.md`, `wiki/concepts/change-adoption-monitoring.md`, `wiki/analyses/change-management-delivery-checklist.md`, `wiki/home.md`, `wiki/index.md`, `wiki/meta/open-questions.md`, `wiki/log.md`.
- Follow-ups: compare this branch against named change frameworks such as ADKAR or Kotter, and decide whether later sources warrant dedicated pages for stakeholder mapping, readiness assessment, or resistance management.

## [2026-04-21] ingest | Change Management Wiki (source provenance update)

- Updated the change-management source page after the original `Change management template.pdf` was added to the same raw bundle folder.
- Added the PDF path to the source page's `raw_sources` and replaced the earlier missing-file note with an explicit link to the original source artifact.
- Pages touched: `wiki/sources/change-management-wiki-bundle.md`, `wiki/log.md`.
- Follow-ups: if needed later, compare the PDF directly with the derived markdown notes to see whether any material sections were omitted or reframed.
