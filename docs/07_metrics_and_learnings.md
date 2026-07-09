# Metrics & Learnings — Competitor Intelligence Engine

This document contains the evaluation logs, quality scorecard, identified product issues, root-cause hypotheses, and product decisions for Milestone 3.

---

## 1. Evaluation Run Log

### Pilot Run: Miro Evaluation (Pre-refinement)
* **Target Competitor**: Miro
* **Public URL**: `https://miro.com`
* **Status**: ❌ Failed Quality Gate (Pilot Run)
* **Details**:
  - Live Research Mode completed successfully.
  - The interface successfully rendered the Executive Summary, SWOT Analysis, Product Backlog, and the Markdown brief export button.
  - 47 automated unit tests and Ruff checks passed.
  - No secrets/keys exposed.
  - **Blocking Quality Issue**: The generated Epic and User Stories were framed directly as feature enhancements for Miro, rather than a differentiated response hypothesis for a target product context. This occurred because the pilot ran without target-product context input.
  - **Status**: **Excluded** from the final release-quality aggregate metrics until prompt refinements are validated.

---

## 2. Quality Scorecard Table

Below is the scorecard for tracking quality across manual live runs.

### Scorecard Table Template
| Criteria | Run #1: Miro (Pilot) [Excluded] | Run #2: Miro (Refined) | Run #3: [Pending] |
| :--- | :--- | :--- | :--- |
| **Source relevance** | N/A | [Pending Rating]* | |
| **Source traceability** | N/A | [Pending Rating]* | |
| **Groundedness of claims** | N/A | [Pending Rating]* | |
| **Quality of uncertainty disclosure** | N/A | [Pending Rating]* | |
| **Strategic usefulness of gaps** | N/A | [Pending Rating]* | |
| **Target-context relevance** | N/A | [Pending Rating]* | |
| **Differentiation quality** | N/A | [Pending Rating]* | |
| **Epic usefulness** | N/A | [Pending Rating]* | |
| **User-story quality** | N/A | [Pending Rating]* | |
| **Acceptance-criteria testability**| N/A | [Pending Rating]* | |
| **Output clarity** | N/A | [Pending Rating]* | |
| **End-to-end workflow usability** | N/A | [Pending Rating]* | |
| **Overall Mean Score** | N/A | [Pending Rating]* | |

*\*Note: Specific rating scores (1-5) are deferred to the final evaluation phase (Milestone 4).*

---

## 3. Issues Found
* **Pilot Quality Issue**: The backlog items generated (Epic title, user story text, acceptance criteria) were framed as extensions for Miro itself because no target product strategy context was provided.
* **Broad Retrieval Quality Issue**: The original Miro pilot had technically successful search retrieval but returned mixed source relevance, as the broad query returned several competitor-irrelevant, third-party packaging sources instead of strictly Miro first-party pages.
* **Low Recall Under Strict Gate**: Applying a strict first-party relevance gate correctly blocked competitor-irrelevant third-party sources but restricted search to a single query, which often returned fewer than two usable first-party sources (e.g. for Notion, Slack, Asana, and Miro), triggering a research failure.

---

## 4. Root-Cause Hypothesis
* **Hypothesis 1 (Target Context)**: System prompts did not specify that backlog items should serve as competitive responses for a distinct target product, and the application lacked an input fields interface for administrators to supply target context. The LLM defaulted to planning for the competitor since it was the only product context available.
* **Hypothesis 2 (Broad Retrieval)**: Tavily search was invoked without domain boundaries (`include_domains`), and search filtering allowed any HTTP/HTTPS URL containing competitor keywords, admitting competitor-irrelevant third-party pages (blogs, forums, etc.) into the strategic synthesis context.
* **Hypothesis 3 (Low Recall)**: Standard keyword queries restricted by `include_domains` often yield sparse index hits when search terms are not structured for target domain site-indexing, causing first-party evidence recall to drop below the minimum requirement.

---

## 5. Resolution or Follow-Up
* **Resolution 1 (Target Context)**: Added a required **Target Product / Strategy Context** text area input to Live Research Mode in `app.py`. Updated `generate_backlog()` in `agent_logic.py` to validate context presence and refined the prompt instructing the LLM that the competitor is solely an evidence source, not the roadmap recipient, and enforcing differentiated response requirements.
* **Resolution 2 (Broad Retrieval)**: Implemented a **First-Party Evidence Relevance Gate**. Added canonical competitor domain derivation helper (normalizing case and stripping `www.`), configured Tavily search call to pass the domain via `include_domains`, filtered normalized search results to strictly match the canonical competitor domain or its subdomains, and required at least 2 distinct usable first-party sources before downstream analysis. Retested successfully with 100% test coverage.
* **Resolution 3 (Low Recall)**: Implemented a **Site-Scoped First-Party Research Recall Fix**. Updated fallback queries in the sequential search loop to use site-scoped formats (`site:{canonical_domain} product features pricing templates updates` and `site:{canonical_domain} help docs release notes product updates customer use cases`). This ensures search engines return deep indexed pages from the target site, fixing the recall failures observed across Notion, Slack, Asana, and Miro while preserving strict first-party constraints.

---

## 6. Latency Observation
* **Pilot Run: Miro**: Completed successfully. (Exact latency tracking is deferred to the final evaluation phase).

---

## 7. Cost Observation
* **Pilot Run: Miro**: Completed successfully. (Exact API cost tracking is deferred to the final evaluation phase).

---

## 8. User Experience Notes
* **Input fields and labels render correctly.**
* **Fictional labels are removed dynamically when transitioning to live results.**
* **The target context displays at the top of the live results block.**

---

## 9. Product Decisions
* Maintain the Target Product / Strategy Context as a required input for all live research runs.
* Require that all backlog evaluations check the **Backlog Evaluation Principle** (enforcing that backlog items are formulated as a competitive response hypothesis for *our* product rather than feature enhancements for the competitor).
* Maintain domain constraints for all fallback search queries. Broad third-party evidence expansion remains deferred to protect evidence quality and brand credibility.

---

## 10. Release Readiness Decision
* **Status**: ⚠️ **Staged with Warnings**
* **Rationale**: The pilot run exposed a critical backlog framing issue which was successfully addressed by adding the Target Product Context parameter and prompt filters. The staging release will remain staged until manual refined runs confirm a mean scorecard grade of >= 4.0/5.
