# Product Charter: Competitor Intelligence Engine

---

## 1. Product Vision

The Competitor Intelligence Engine empowers product professionals to instantly convert unstructured competitor research into structured, high-fidelity, and evidence-grounded strategic planning outputs. By employing a multi-agent system, the product aims to bridge the gap between competitive market realities and active development backlogs, ensuring that product choices are always grounded in verified public evidence.

---

## 2. Problem Statement

Modern product teams struggle to maintain a continuous, structured pulse on competitors. The process of gathering data, analyzing competitor strengths and weaknesses, identifying gaps, and converting those insights into development items (Epics and User Stories) is slow and highly manual. The resulting outputs are often:
* Lacking citation, making validation difficult.
* Divorced from original evidence, leading to unsupported product decisions.
* Structurally non-compliant with standard agile workflows, adding manual translation overhead.

---

## 3. Target Users

* **Product Managers** – Need to quickly evaluate competitor adjustments to adjust roadmap prioritization.
* **Product Owners / Business Analysts** – Need to translate high-level competitive gaps into development-ready user stories.
* **Product Strategy Leads** – Need to track market shifts and identify strategic opportunities.
* **Startup Founders** – Need to evaluate market entrance strategies with minimal resources.

*Portfolio audience: Recruiters and interviewers are secondary reviewers of this prototype, not intended operational users of the product.*

---

## 4. Jobs To Be Done

“When reviewing AI-generated recommendations, I want to inspect supporting public references and identify unsupported assumptions so that I can validate the evidence before making product decisions.”

---

## 5. User Journey

1. **Setup & Authentication:** A user accesses the Streamlit web application. If they wish to perform live research, they provide their `LIVE_RESEARCH_ACCESS_CODE`. Otherwise, they navigate the preloaded Demo datasets.
2. **Search Submission:** The user inputs a competitor public URL (e.g., a pricing page, product announcement, or documentation link) and triggers the analysis.
3. **Multi-Agent Processing:** The app orchestrates research retrieving public details, executing strategic assessment, and composing development backlog items.
4. **Structured Review:** The user views the generated executive summary, SWOT, and opportunity gaps.
5. **Backlog Inspection:** The user inspects the proposed Epic and three user stories (including testable acceptance criteria), validation badges, and direct links to parsed sources.
6. **Export & Action:** The user downloads the final Markdown report containing the structured analysis for ingestion into their project management tools (e.g. Jira, Linear).

---

## 6. MVP Scope

* **Framework Foundation:** Streamlit web application for interactive dashboard presentation.
* **Dual Operation Modes:** Public Demo Mode (static, preloaded) and protected Live Research Mode (live search via Tavily and LLM orchestration).
* **LangGraph Agent Workflow:** Orchestrated execution of Research Agent, Strategic Analyst, and Backlog Writer.
* **Structured Document Generation:** Outputting a complete, source-grounded competitor brief (including executive summary, SWOT, opportunity gaps, and backlog items).
* **Strict Validation:** Using Pydantic to ensure all outputs match strict structural requirements.
* **Download Capability:** Simple markdown downloader button for local file storage.

---

## 7. Explicit Non-Goals

* **No Authentication Services:** The MVP does not support user accounts, login databases, or individual profiles; access to Live Mode is gated solely by a simple token check (`LIVE_RESEARCH_ACCESS_CODE`).
* **No Direct Jira Integration:** The system will output standard Markdown backlog files; it will not directly write to third-party endpoints or APIs like Jira, Linear, or Azure DevOps.
* **No Private Content Research:** The engine only parses publicly available data. It does not support scanning private customer databases, password-protected portals, or paywalled repositories.
* **No Real-Time Monitoring or Alerts:** This tool is run on-demand. Continuous cron-job alerts, change notifications, or email reports are out of scope.

---

## 8. Agent Responsibilities

The system divides labor among three distinct agents coordinated via LangGraph state updates:

1. **Research Agent**
   * *Responsibility:* Interacts with search systems (Tavily) to retrieve public information regarding the target competitor.
   * *Output:* Raw crawled text blocks and verified source URLs (reference links).
2. **Strategic Analyst**
   * *Responsibility:* Evaluates raw evidence from the Research Agent to outline competitor strengths, weaknesses, opportunities, and threats.
   * *Output:* Executive summary, source-grounded SWOT, and 3-5 opportunity gaps.
3. **Backlog Writer**
   * *Responsibility:* Consumes opportunity gaps and strategic details to engineer one Epic and exactly three User Stories.
   * *Output:* Backlog artifacts containing testable acceptance criteria, validated against strict Pydantic schemas.

---

## 9. AI Safety and Human-in-the-Loop Design

* **Reference Sanitization:** Raw page crawlers present high prompt injection risks if competitor sites host hostile instructions. To counter this, crawled content is classified solely as untrusted semantic data (references) rather than control prompts.
* **Source-Verifiable Statements:** Every Opportunity Gap and SWOT quadrant item must link to one or more resource URLs fetched by the Research Agent. Users can instantly cross-verify statements against these citations to ensure grounding.
* **Manual Backlog Refinement:** The artifact model is designed to support future phases where humans can review, edit, or reject the SWOT analysis and Opportunity Gaps before triggering the Backlog Writer agent.

---

## 10. Success Metrics

* **Output Compliance Rate:** 100% of successful completed runs must generate exactly one Epic, exactly three User Stories, and three to five opportunity gaps.
* **Source Grounding Rate:** 100% of generated SWOT quadrants and opportunity gaps must contain at least one verifiable Web source URL extracted during the session.
* **Access Control Integrity:** Zero successful Live Research agent runs executed without verification of the `LIVE_RESEARCH_ACCESS_CODE`.

---

## 11. Quality Metrics

* **Live Research Performance Target:** Under normal provider availability, target completion within 90 seconds. This target excludes external provider outages, rate limits, and inaccessible public sources.
* **Pydantic Validation Pass Rate:** >= 98% pass rate on structural validation tests during agent runs without requiring orchestration retries.
* **Unit Test Coverage:** 100% coverage on core extraction schemas and state transmission logic.

---

## 12. Risks and Mitigations

* **Risk: Downstream AI Hallucinations.** The model could formulate false claims or mischaracterize competitor capabilities.
  * *Mitigation:* Explicitly state that the system does not guarantee factual completeness or hallucination-free output. Display evidence links side-by-side with generated items to enforce manual verification.
* **Risk: External API Rate Limits & Cost Overruns.** Unrestricted live research loops can drain OpenAI & Tavily credits.
  * *Mitigation:* Imposed access limits via the `LIVE_RESEARCH_ACCESS_CODE` and request rate limits. Host preloaded datasets for public interaction under Demo Mode (which bypasses API runs entirely).
* **Risk: target Website Blocking Search Scraping.** Some websites block extraction spiders.
  * *Mitigation:* Fallback gracefully by alerting the user to data access failures, pointing them to static Demo datasets, and excluding these outages from performance SLA reporting.

---

## 13. Milestone 1 Definition of Done

* `README.md` updated with recruiter positioning, system definition, and architecture diagrams.
* `01_project_charter.md` completed.
* `BUILD_PLAN.md` finalized with specific agent configurations, security boundaries, and hosting plans.
* Python validation schemas configured and linting cleanly.
* Demo data stub modules ready to return static analysis configurations.
* No live functional python files, dependencies, Docker configurations, git settings, or secret files modified.
