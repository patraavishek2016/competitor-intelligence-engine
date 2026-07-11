# Release Notes — Competitor Intelligence Engine

---

## v0.1.1 — Product Design and PRD Closure

**Release date:** 2026-07-11
**Status:** ✅ Complete

### Overview
This release closes out the project requirements phase by establishing mature product management documentation. It explains the customer pain points, design choices, and how the multi-agent system maps directly to these needs.

### Deliverables & Documentation Updates
* **Added Product Design Approach**: Created `docs/09_product_design_approach.md` covering customer journeys, friction, detailed 3C analysis, personas, OKRs, and agentic rationale.
* **Added Product Requirements Document**: Created `docs/10_prd.md` containing core system objectives, hypotheses, functional and non-functional requirements, detailed BDD user stories, and mitigations.
* **Added README Links**: Integrated links to all product design artifacts in `README.md` and updated the folder layout graphic.
* **Updated Product Learnings**: Appended strategic reflections in `docs/07_metrics_and_learnings.md` addressing context gating, evidence traceability, and Demo Mode constraints.

### Constraints Check
* **No runtime logic changed**: No python execution flows or orchestration nodes modified.
* **No secrets, Docker, dependencies, tests, or deployment settings changed**.

---

## Milestone 3 — Live Orchestration & Fail-safe Research

**Release date:** 2026-06-30
**Status:** ✅ Complete

### Overview
Milestone 3 transitions the Competitor Intelligence Engine from a static dashboard into an active, secure multi-agent live pipeline. It introduces a Tavily search agent, an OpenAI strategic analyst, an automated backlog writer, and orchestrates them using a deterministic LangGraph workflow. The entire system is secured behind an access-code prototype gate and is fully covered by mocked unit tests.

### Refinements & Quality Improvements
* **Target Product Context Gating**: Added a required **Target Product / Strategy Context** text area input to Live Research Mode. This anchors the generated strategic requirements to a specified B2B strategy instead of formulating features for the competitor itself.
* **Refined Backlog Prompt Filters**: Explicitly instructed the Backlog Writer that the competitor is solely an evidence source, not the roadmap recipient, and banned naming Epics after enhancing the competitor.
* **First-Party Evidence Relevance Gate**: Implemented domain-bound search queries using Tavily's `include_domains` with the canonical competitor domain, and introduced a post-retrieval relevance gate that filters out competitor-irrelevant third-party domains. Requires at least 2 distinct usable first-party sources before downstream agents run.
* **First-Party Multi-Query Research Fallback (Site-Scoped)**: Added a sequential multi-query fallback mechanism to improve first-party recall. The Research Agent issues up to three domain-bounded query variants (general positioning query, and two site-scoped queries targeting pricing/templates/updates and help/docs) before applying the relevance gate. Includes early-stopping cost controls that skip subsequent queries as soon as two or more usable sources are found, resolving recall errors on Notion, Slack, Asana, and Miro.

### Delivered Capabilities

| Capability | Detail |
| :--- | :--- |
| **Tavily Research Agent** | Resolves target hostnames, canonicalizes competitor domains (normalizing case and stripping `www.`), queries public indexing restricted to the competitor domain using up to three sequential search queries (including site-scoped variants) with early-stopping cost controls, and normalizes search outcomes to Pydantic `EvidenceSource` objects. Handles URL deduplication, content truncation (300 chars max), and filters out unrelated third-party domains. |
| **OpenAI Strategic Analyst** | Summarizes public evidence, builds SWOT insights, maps opportunity gaps, and validates that every claim has a valid source ID citation in the original search list. |
| **OpenAI Backlog Writer** | Translates strategic gaps into exactly one Epic and exactly three User Stories with 3-5 Given/When/Then acceptance criteria, framed as a differentiated response hypothesis. |
| **LangGraph Orchestrator** | A StateGraph workflow coordinating Research -> Analyst -> Backlog Writer nodes. Halts immediately on any upstream failure, preventing downstream API calls. |
| **Secure Live Mode in UI** | Streamlit selectbox switches to **Live Research Mode**, offering an access code gate (`type="password"`) and safe, generic user-facing error reporting. |
| **Dependency Injection** | All core logical steps support dependency injection, allowing tests to run keyless and networkless. |

### Security & Cost-Control Design
* **Credentials Gating**: The user is never prompted to input OpenAI or Tavily API keys. Server-side secrets are loaded from `.env`.
* **Zero Leakage**: Stack traces, raw provider exceptions, LLM prompts, and API keys are caught and mapped to safe, generic user-facing strings (e.g., `"Access code was not accepted."`).
* **Timing attack prevention**: Secure constant-time string comparison (`hmac.compare_digest`) validates authorization.
* **Cost Cap**: The research agent limits search output to a maximum of 5 hits, preventing run-away token usage.

### Intentionally Deferred Capabilities
* **Persistence store / DB**: Live results exist in memory within `st.session_state` and are not stored in a database.
* **Persistent Authentication**: Cookie-based login or OAuth is deferred to future enterprise deployments.
* **Advanced retry loops**: Retries or parallel branches are omitted to keep the LangGraph orchestrator highly deterministic.

### Known Limitations
* **Prototype Access Gate**: The access code is a simple gate to prevent unauthorized execution of your endpoints and billing; it is not a substitute for enterprise-grade authentication.
* **LLM Dependency**: Errors in OpenAI schema validation will result in the workflow terminating immediately with a generic error block.

---

## Milestone 4 — Evaluation & Deployment (Preview)
The next milestone will focus on:
* **LLM Quality Evaluation**: Measuring accuracy, hallucination rate, and citation precision.
* **Docker Packaging**: Containerizing the application for portable deployments.
* **Hugging Face / Cloud Deployment**: Launching the portfolio prototype to a cloud runtime environment.

---

## Milestone 2 — Demo Mode Foundation

**Release date:** 2026-06-28
**Status:** ✅ Complete

### Overview
Milestone 2 establishes a fully validated, fully static Demo Mode for the Competitor Intelligence Engine. It delivers a professional Streamlit interface backed by fictional demo data that demonstrates the complete analysis workflow without touching any external APIs, environment variables, or network services.
### Delivered Capabilities
* **Pydantic v2 schema layer**: Eight validated models covering `EvidenceSource`, `EvidenceBackedInsight`, `SWOTAnalysis`, `OpportunityGap`, `UserStory`, `Epic`, `AnalysisResult`, and `CompetitorIntelligenceResult`.
* **Field-level validation rules**: Opportunity gaps: 3–5 items · Epic: exactly 3 User Stories · Acceptance criteria: 3–5 per story · BDD format enforced (Given/When/Then) · Source IDs required on all insights and gaps.
* **Fictional demo data layer**: `get_demo_result()` returns a complete fictional NimbusFlow competitor brief; all sources use `.example` TLD.
* **URL validation utility**: `validate_public_url()` rejects empty, non-HTTP/HTTPS, localhost, loopback, and private-IP URLs without any DNS lookups.
* **Markdown export utility**: `build_markdown_brief()` produces a full structured Markdown document from any `CompetitorIntelligenceResult`.
* **Streamlit Demo Mode interface**: Professional five-tab UX (Executive Summary · SWOT · Opportunity Gaps · Product Backlog · Evidence Sources).

---

*Competitor Intelligence Engine · Portfolio prototype by Avishek Patra*
