# Release Notes — Competitor Intelligence Engine

---

## v0.1.2 — Documentation Completion and Replication Guide

**Release date:** 2026-07-11
**Status:** ✅ Complete

### Overview
This release closes remaining public documentation gaps for Project 0 by populating blank documentation files and adding a tools, cost, and replication guide. No runtime logic or Python code has been modified.

### Deliverables & Documentation Updates
* **Populated Problem Statement**: Completed [docs/02_problem_statement.md](file:///C:/Users/avish/Documents/AI-Portfolio/competitor-intelligence-engine/docs/02_problem_statement.md) outlining Context, User Pain Points, Fragmented Research, Summarization vs Action, and the Human Review Boundary.
* **Populated Product Requirements Summary**: Completed [docs/03_product_requirements.md](file:///C:/Users/avish/Documents/AI-Portfolio/competitor-intelligence-engine/docs/03_product_requirements.md) summarising core goals, inputs, outputs, Demo Mode vs Live Mode, Agent Workflow, and Pydantic validation rules.
* **Populated System Architecture**: Completed [docs/05_system_architecture.md](file:///C:/Users/avish/Documents/AI-Portfolio/competitor-intelligence-engine/docs/05_system_architecture.md) with system flow diagram, agent nodes, validation gates, and deployment architecture details.
* **Added Tools, Costs, and Replication Guide**: Created [docs/11_tools_costs_and_replication_guide.md](file:///C:/Users/avish/Documents/AI-Portfolio/competitor-intelligence-engine/docs/11_tools_costs_and_replication_guide.md) documenting technical tools stack, environment configurations, pricing structures, and replication walkthroughs.
* **Added Docker Ignore Exclusions**: Populated [.dockerignore](file:///C:/Users/avish/Documents/AI-Portfolio/competitor-intelligence-engine/.dockerignore) with standard and safe exclude patterns.
* **Updated README Navigation**: Appended the Build, Tools & Replication Guide references in the root [README.md](file:///C:/Users/avish/Documents/AI-Portfolio/competitor-intelligence-engine/README.md).

### Constraints Check
* **No runtime logic changed**: No python files or execution flows modified.
* **No tests, secrets, dependencies, Dockerfile, or deployment settings changed**.

---

## v0.1.1 — Product Design and PRD Closure

**Release date:** 2026-07-11
**Status:** ✅ Complete

### Overview
This release closes out the project requirements phase by establishing mature product management documentation. It explains the customer pain points, design choices, and how the multi-agent system maps directly to these needs.

### Deliverables & Documentation Updates
* **Added Product Design Approach**: Created `docs/09_product_design_approach.md` covering customer journeys, friction, detailed 3C analysis, personas, OKRs, and agentic rationale.
* **Added Product Requirements Document**: Created `docs/10_prd.md` containing core system objectives, hypotheses, functional and non-functional requirements, detailed BDD user stories, and mitigations.
* **Added README Links**: Integrated links to all product design artifacts in `README.md`.
* **Updated Product Learnings**: Appended strategic reflections in `docs/07_metrics_and_learnings.md` addressing context gating, evidence traceability, and Demo Mode constraints.

### Constraints Check
* **No runtime logic changed**: No python execution flows or orchestration nodes modified.
* **No secrets, Docker, dependencies, tests, or deployment settings changed**.

---

## Milestone 4A — Final Project 0 Recruiter Packaging

**Release date:** 2026-07-09  
**Status:** ✅ Complete

### Overview
Milestone 4A packages the competitor-intelligence-engine prototype for direct recruiter and portfolio review. It establishes a polished root README.md, updates metrics documents with structured recruiter-oriented learnings, and marks the successful dockerized cloud hosting on Hugging Face Spaces. No runtime code, secrets, or tests were changed.

### Delivered Packaging
* **Recruiter-Facing Readme**: Restructured the root `README.md` to highlight live/demo links, target users, problem context, LangGraph architecture, AI safety features, and talking points.
* **Mermaid Workflow Diagram**: Added a detailed system sequence and flow diagram to illustrate multi-agent state coordination.
* **Docker & HF Spaces Documentation**: Added comprehensive guides for local and containerized hosting.
* **Recruiter-Facing Learnings**: Added architectural summaries in `docs/07_metrics_and_learnings.md` addressing key design choices (e.g., target context, first-party gates, and demo modes).

---

## Milestone 4 — Evaluation & Deployment

**Release date:** 2026-07-07  
**Status:** ✅ Complete

### Overview
Milestone 4 containerized the Streamlit application for production-ready portability and deployed the engine to a Hugging Face Spaces Docker runtime.

### Delivered Capabilities
* **Docker Containerization**: Designed a production-optimized `Dockerfile` exposing standard Streamlit ports.
* **Hugging Face Cloud Hosting**: Successfully deployed the dockerized container to Hugging Face Spaces at `https://huggingface.co/spaces/patraavishek2016/competitor-intelligence-engine`.
* **Environment Configuration**: Set up secure environment secrets mapping to prevent keys/access codes leaking to public clients.

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
