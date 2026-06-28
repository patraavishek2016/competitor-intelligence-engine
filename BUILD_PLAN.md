# Build Plan: Competitor Intelligence Engine

This build plan outlines the core architecture, agent interactions, security boundaries, and step-by-step implementation milestones for the Competitor Intelligence Engine prototype.

---

## 1. Scope and Architectural Guidelines

To maintain speed, agility, and simplicity, this prototype is designed as a single monolithic **Streamlit** application hosted on **Hugging Face Spaces**. 

### Technology Stack
* **Core Interface:** Streamlit (Python)
* **Agentic Orchestration:** LangGraph (Python)
* **External Public Search:** Tavily API
* **Language Model Provider:** OpenAI API
* **Structure & Validation:** Pydantic
* **Local Containerization:** Docker
* **Testing Suite:** Pytest

### Architectural Exclusions
To keep the scope of Project 0 manageable and focused, the following technologies are **explicitly excluded** from the architecture:
* No external web frameworks (e.g., React, Vite).
* No decoupled backend API servers (e.g., FastAPI).
* No browser automation or scraping libraries (e.g., Playwright).
* No real-time transport protocols (e.g., WebSockets, Server-Sent Events).
* No distributed microservices.

---

## 2. Operation Profiles

The application implements a strict separation between public guest testing and authorized research:

1. **Demo Mode (Public)**
   * Access profile: Publicly available, requiring no configuration.
   * Execution profile: Returns static, preloaded, fictional competitor datasets.
   * **Makes zero external API calls**, protecting the project's OpenAI and Tavily API budget from public exhaustion.
2. **Live Research Mode (Authorized)**
   * Access profile: Requires a valid **`LIVE_RESEARCH_ACCESS_CODE`** environment variable check.
   * Execution profile: Triggers live Tavily searches and OpenAI generation requests to compile analysis datasets.

---

## 3. Core Agent Workflow

The systems agentic process is coordinated via a stateful **LangGraph** flow containing three specialized, sequential agents:

```
[Start] --> (Research Agent) --> (Strategic Analyst) --> (Backlog Writer) --> [End]
```

### Agent Definitions
1. **Research Agent**
   * *Purpose:* Gathers unstructured web documentation for a user-supplied URL.
   * *Mechanism:* Dispatches targeted queries via the Tavily Search API.
   * *Output:* Extracted raw text snippets associated with verified source URLs.
2. **Strategic Analyst**
   * *Purpose:* Performs strategic analysis on the gathered research data.
   * *Mechanism:* Prompts OpenAI models to process raw findings.
   * *Output:* Creates a formatted competitor summary, a source-grounded SWOT analysis, and identifies 3 to 5 opportunity gaps.
3. **Backlog Writer**
   * *Purpose:* Translates opportunities into implementation tasks.
   * *Mechanism:* Uses structured OpenAI API responses validated against Pydantic schemas.
   * *Output:* Exactly one Epic and exactly three User Stories equipped with testable acceptance criteria.

---

## 4. Security & Quality Guardrails

### Untrusted Content Isolation
External web page content returned by search runs is labeled and processed strictly as **untrusted reference data**. It is passed into LLM completion templates as data parameters only, ensuring that instructions embedded inside scraped competitor web pages cannot hijack the system prompts (preventing indirect prompt injection).

### Truthfulness & Hallucination Mitigation
The system prioritizes grounding over completeness:
* Output items (SWOT cells and opportunity gaps) are parsed with mandatory source citation links.
* **No Factual Completeness Guarantees:** The engine does not make claims of guaranteeing factual completeness or producing entirely hallucination-free output. Every generation is framed as a strategic recommendation requiring human verification.

### Resource Controlling & Hosting Limits
* **Host Platform:** Hugging Face Spaces (free tier, CPU basic).
* **API Usage:** Strictly restricted in Live Research Mode. In addition to testing for the `LIVE_RESEARCH_ACCESS_CODE`, strict token budgets and search depth overrides are set on OpenAI and Tavily APIs to prevent runaway loop costs.

---

## 5. Implementation Phases (Milestones)

### Phase 1: Foundation, Schemas, & Demo Mode
* **Step 1:** Define the Pydantic validator schemas in `schemas.py` representing the SWOT structure, opportunity gaps, and backlog stories.
* **Step 2:** Populate `demo_data.py` with pre-baked competitor profiles matching the validated schemas.
* **Step 3:** Implement the core Streamlit user interface in `app.py`. Ensure Demo Mode works out of the box with zero setup.
* **Step 4:** Set up verification tests under the `tests/` directory verifying configuration checking and schema validation.

### Phase 2: LangGraph Orchestration & Live Research Mode
* **Step 1:** Implement LangGraph state variables and execution helper hooks in `agent_logic.py`.
* **Step 2:** Write `LIVE_RESEARCH_ACCESS_CODE` checks inside application startup hooks.
* **Step 3:** Hook the Research Agent into the Tavily search interface to query, retrieve, and parse public articles and competitor pages.
* **Step 4:** Integrate the Strategic Analyst and Backlog Writer nodes, binding completion chains to their respective formatting schemas.

### Phase 3: Human Verification Checkpoints
* **Step 1:** Modify the LangGraph flow to support validation checkpoints.
* **Step 2:** Implement review steps in the Streamlit UI, allowing users to verify or edit research outputs before the final stories are drafted.
* **Step 3:** Build markdown compiler helpers in `utils.py` to bundle finalized data into user-downloadable brief reports.

### Phase 4: Containerization & Deployment
* **Step 1:** Finalize the local configuration files (`Dockerfile`, `.dockerignore`).
* **Step 2:** Validate multi-mode testing suites via Pytest.
* **Step 3:** Push the repository codebase to Hugging Face Spaces. Configure the backend secret keys (`OPENAI_API_KEY`, `TAVILY_API_KEY`, and `LIVE_RESEARCH_ACCESS_CODE`).
