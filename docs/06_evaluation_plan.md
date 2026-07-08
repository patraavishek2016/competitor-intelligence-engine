# Evaluation Plan — Competitor Intelligence Engine

This document defines the evaluation plan for validating the quality, security, robustness, and accuracy of the Competitor Intelligence Engine. It establishes structured test criteria across automated unit tests, quality scorecard rubrics, and manual live-run checks.

---

## 1. Evaluation Purpose
The evaluation plan is designed to verify that the multi-agent pipeline (Research Agent -> Strategic Analyst -> Backlog Writer) safely collects public data, performs grounded strategic syntheses without hallucinating details, and outputs structured, BDD-compliant product requirements that serve as a differentiated product response hypothesis rather than competitor roadmap recommendations.

---

## 2. Test Scope
The evaluation spans:
* **Automated Unit Testing**: Local verification of data models, URL validators, orchestrator failure paths, custom error messages, and prompt formatting.
* **Manual Quality Assessment**: Direct human evaluations of the live outputs using a structured scorecard.
* **Security & Leakage Audits**: Verification that API keys, raw provider logs, and internal tracebacks are never exposed to users or logs.
* **Performance & Costs Audits**: Monitoring latency profiles and OpenAI/Tavily API call spends.

---

## 3. Test Inputs
To protect sensitive IP, a strict rule is enforced on test inputs:

> [!WARNING]
> **Public-Data Rule**: Use only public competitor URLs and do not submit employer, customer, confidential, personal, or restricted data.

Tests utilize public marketing, pricing, or product landing pages for competitors (e.g., Miro, NimbusFlow, etc.).

---

## 4. Automated Test Coverage
Automated test coverage runs locally using `pytest`. The suite executes 47 distinct assertions verifying:
1. Pydantic schema validation rules (e.g., Epic contains exactly 3 stories, stories contain 3-5 Given/When/Then criteria).
2. URL validation utilities (blocking loopbacks, localhosts, and private IPs).
3. LangGraph orchestrator failure paths and error masking.
4. Settings managers and environment variables parsing logic.
5. Injected mock responses matching expected structural bounds.

---

## 5. Manual Live-Run Evaluation
Evaluations are run manually through the Streamlit Live Research interface. To monitor paid calls, the evaluation observes this policy:

> [!TIP]
> **Cost-Control Rule**: Begin with one controlled live run, review output quality, then run no more than three public evaluation URLs before deployment.

Evaluators input the target URL, the target product context, and the access code, run the engine, navigate results tabs, export briefs, and log details.

---

## 6. Quality Scoring Rubric
Every manual live run must be graded on a scale of 1 (poor) to 5 (excellent) across these 12 criteria:

1. **Source relevance (First-Party Evidence Relevance) (1–5)**: The retrieved pages represent actual first-party competitor material (allowed canonical domain and its valid subdomains) rather than generic search noise or third-party pages. Project 0 defaults strictly to first-party competitor-domain evidence only. Third-party evidence expansion is deferred to a later version and requires its own relevance and credibility policy.
2. **Source traceability (1–5)**: Statements in the SWOT and gaps tabs accurately cite source IDs from the evidence list.
3. **Groundedness of strategic claims (1–5)**: Insights are derived directly from retrieved excerpts rather than LLM assumptions.
4. **Quality of uncertainty disclosure (1–5)**: Evaluates whether the analyst uses words of uncertainty (e.g., "appears to", "suggests") when evidence is thin.
5. **Strategic usefulness of opportunity gaps (1–5)**: The logged gaps identify genuine competitor weaknesses or differentiators.
6. **Target-context relevance (1–5)**: The generated Epic and stories directly align with and support the provided target product/strategy context.
7. **Differentiation quality (1–5)**: The backlog represents a differentiated product response hypothesis rather than a feature roadmap for the competitor.
8. **Epic usefulness (1–5)**: The backlog Epic establishes a clear, strategic answer to the competitor's profile.
9. **User-story quality (1–5)**: Follows standard Agile format (As a... I want to... So that...).
10. **Acceptance-criteria testability (1–5)**: Verifies BDD criteria are actionable, realistic, and contain the required syntax.
11. **Output clarity (1–5)**: Text flow, narrative tone, and overall readability.
12. **End-to-end workflow usability (1–5)**: Streamlit loading states, responsive tabs, and report export behavior.

---

## 7. Safety and Failure Evaluation
Evaluates robustness under adverse conditions:
* Invalid/unsupported URL schema rejections.
* Mismatched access codes behavior.
* Verification that mock Tavily or OpenAI exceptions yield generic, user-safe instructions with no credentials exposed.

---

## 8. Cost and Latency Monitoring
* **Latency**: Evaluators monitor total runtime of the spinner in the UI.
* **Cost**: API query logs are audited via provider dashboards to keep costs within $0.05 per run.

---

## 9. Acceptance Thresholds
Before the system can be declared production-ready, it must meet the following criteria:

* **Strict Structural Rules**:
  - No source IDs outside the retrieved evidence list (no hallucinated citations).
  - Exactly one Epic and exactly three User Stories.
  - Every user story contains three to five Given/When/Then acceptance criteria.
* **Security Guardrails**:
  - No raw provider errors, API keys, stack traces, or secrets displayed.
* **Average Ratings**:
  - Mean score of at least 4.0/5 for source relevance, output clarity, and strategic usefulness across at least three manual live runs.
* **Manual Override & Review**:
  - Any critical unsupported claim must be marked as an issue and reviewed manually.
* **Backlog Evaluation Principle**:
  - The backlog must represent a differentiated response hypothesis for a target product. It must not be framed as a roadmap recommendation for the competitor being analyzed.

---

## 10. Known Evaluation Limits
* **Search Freshness**: Tavily results reflect search index currency, which may miss very recent modifications.
* **LLM Inherent Bias**: LLMs tend to generate backlog features for the competitor rather than the user's target product unless strictly prompted. Manual reviews are essential to enforce this mapping.
