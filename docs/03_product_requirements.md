# Product Requirements Summary

---

## Product Goal
The core goal of the **Competitor Intelligence Engine** is to automate competitor intelligence ingestion and translation into structured, BDD-compliant developer requirements. The product accelerates the strategic discovery loop by transforming public web evidence into a differentiated product backlog brief.

---

## Core Input Requirements
The system must accept and validate the following inputs:
* **Competitor URL**: A valid public URL pointing to a competitor's domain. The URL validator must enforce that the string is a well-formed HTTP/HTTPS address, rejecting localhost, private subnets, and loopback IPs.
* **Target Product / Strategy Context**: A user-supplied strategic prompt defining their own product's differentiation goals, constraints, and value proposition. This anchors backlog creation to *our* strategy instead of mirroring the competitor.

---

## Core Output Requirements
The application must generate and present a five-tab structured dashboard containing:
1. **Executive Summary**: Synthesized high-level strategic takeaways from the competitor's public material.
2. **SWOT Analysis**: A standard strengths, weaknesses, opportunities, and threats grid where each point is referenced to a specific source ID.
3. **Opportunity Gaps**: A list of 3 to 5 clear market or product opportunities, grounded in evidence sources.
4. **Product Backlog**: Exactly one Epic and exactly three User Stories with 3-5 BDD-formatted (Given/When/Then) acceptance criteria per story.
5. **Evidence Sources**: A list of verified, canonical first-party competitor URLs parsed during the query run.

---

## Demo Mode Requirements
* **Offline Execution**: The mode must run without external network requests or dependency on live API keys.
* **Fictional Competitor Data**: The system must load static, predefined, high-quality analysis data modeling a fictional competitor (`nimbusflow.example`).
* **$0 Cost Boundary**: Running Demo Mode must not consume OpenAI or Tavily API tokens, providing an instant, zero-cost showcase path.

---

## Protected Live Research Mode Requirements
* **Access Control Gate**: Live research execution must be gate-kept behind a secure passcode check using constant-time string comparison (`hmac.compare_digest`).
* **Secret Configuration**: All API keys (`OPENAI_API_KEY`, `TAVILY_API_KEY`) and the access code must be loaded from server-side environment variables, never exposed to public clients.
* **Exception Catching**: Under no circumstances should raw stack traces, prompts, or API payloads leak to the user interface. Errors must map to clean, user-safe warning components.

---

## Agent Workflow Requirements
The Live Research pipeline must coordinate three nodes in a stateful orchestration pattern:
1. **Research Agent**: Normalizes the target hostname (stripping `www.`, resolving subdomains) and queries public directories. Must employ a **multi-query fallback loop** (executing up to 3 domain-bounded queries if initial results yield $< 2$ sources) and an **early-stopping cost-control gate** that halts searching once $\ge 2$ unique sources are collected.
2. **Strategic Analyst**: Filters out third-party review sites/blogs and compiles the SWOT grid, ensuring all statements are explicitly linked to sequentially generated source IDs (e.g., `SRC-1`, `SRC-2`).
3. **Backlog Writer**: Generates the agile Epic and stories by synthesizing the SWOT findings with the user's strategy context.

---

## Validation Requirements
* **Pydantic Validation Gates**: The system must validate all agent outputs against strict schema contracts.
* **Agile Integrity Rules**:
  - The backlog must contain exactly one Epic.
  - The Epic must contain exactly three User Stories.
  - Each User Story must include 3 to 5 acceptance criteria.
  - Each acceptance criterion must strictly conform to BDD syntax (containing `Given`, `When`, and `Then` keywords).
* **Reference Grounding Gates**: SWOT claims and opportunity gaps must contain valid, non-empty source ID citations that reference verified sources returned by the Research Agent.

---

## Non-Goals
* **Jira/Backlog Sync**: Active write integration or syncing with external ticketing platforms (e.g., Jira, Azure DevOps) is out of scope. The system outputs standard exportable Markdown instead.
* **User Authentication**: Standard user accounts, multi-tenant databases, or OAuth flows are omitted. Live mode uses a shared session password.
* **Executing/Validating Competitor Code**: The engine solely analyzes unstructured public text and documentation; it does not crawl code repositories or run API vulnerability sweeps.

---

## Reference Document
For full details, edge cases, user journeys, functional matrices, and release metrics, please consult the complete [Product Requirements Document](file:///C:/Users/avish/Documents/AI-Portfolio/competitor-intelligence-engine/docs/10_prd.md).
