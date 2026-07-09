# User Journey — Competitor Intelligence Engine

This document describes the end-to-end user journeys for both **Demo Mode** and **Live Research Mode** of the Competitor Intelligence Engine.

---

## Demo Mode Journey

No-cost evaluation of the dashboard structure using high-fidelity fictional static data.

### Step 1: Open App
The user launches the application:
```bash
streamlit run app.py
```
The browser opens to the home screen showing:
* Product title and strategic description.
* **Safety Notice** banner warning that outputs are hypotheses requiring validation.
* Default selectbox set to **Demo Mode**.

### Step 2: Review Demo Mode Banners
Before interacting, the user reads the default banners:
* ⚠️ **Safety Notice**: "Generated outputs are product hypotheses and require human validation..."
* 🔵 **Demo Mode**: "Fictional static demo data. No external API calls are made."

### Step 3: Run Demo Analysis
The user clicks the **▶ Run Demo Analysis** button.
* The application immediately fetches `get_demo_result()` from `demo_data.py`.
* No network requests, API keys, or environment variables are accessed.
* A success confirmation message appears.

### Step 4: Review Outputs
The user navigates the five results tabs:
* **📋 Executive Summary**: Synthesized narrative of the fictional NimbusFlow competitor.
* **🔲 SWOT Analysis**: Grid with source citations and confidence values.
* **🎯 Opportunity Gaps**: Prioritized market gaps with BDD-like rationale.
* **📦 Product Backlog**: One Epic and three User Stories with acceptance criteria.
* **📚 Evidence Sources**: All sources are clearly labeled with a **Fictional** badge.

### Step 5: Export Report
The user downloads a compiled markdown file titled `competitor-intelligence-demo-brief.md` by clicking the download button in the Executive Summary tab.

---

## Live Research Mode Journey

Controlled public research using active server-side APIs, protected by an access gate.

### Step 1: Switch Mode
The user changes the operation mode selectbox from **Demo Mode** to **Live Research Mode**.
* The blue Demo badge transitions to a red **Live Research Mode** badge.
* The system renders a warning regarding paid API usage and the necessity to input only public competitor URLs.

### Step 2: Read Warnings and Secure Gate Notes
The user reviews:
* ⚠️ **Paid API Warning**: "This mode performs paid external API requests using server-side credentials. Use only public competitor URLs..."
* 💡 **Security Disclaimer**: "Prototype limitation: access-code protection is a basic usage gate. It is not a substitute for enterprise authentication..."

### Step 3: Enter Target Product Context, Target URL, and Access Code
The user enters:
* **Public Competitor URL**: e.g., `https://competitor.com`
* **Target Product / Strategy Context**: Describes the target product users and differentiation goal (e.g., *"A hypothetical B2B collaboration workspace for distributed product teams that differentiates through asynchronous decision capture, auditability, and lightweight governance."*). This is required and cannot be blank.
* **Access Code**: The secret deployment gate code (masked with type `password`).

### Step 4: Submit Live Research
The user clicks **Run Live Research**.
1. **Server Configuration Check**: The server loads the `.env` settings. If API keys or the access code are missing, the UI displays: *"Live Research Mode is not configured in this deployment."*
2. **Authorization Check**: The server uses secure comparison (`hmac.compare_digest`). If the access code is invalid, the UI displays: *"Access code was not accepted."*
3. **Graph Execution**: If validation and authorization succeed, the server triggers the compiled LangGraph workflow under a generic spinner: *"Running the controlled research, analysis, and backlog workflow..."*

### Step 5: Review Live Outputs
If successful, the dashboard renders live-fetched, AI-structured data across the same tabs:
* **Target Product Context**: The user's submitted context is rendered at the top of the results section.
* **📋 Executive Summary**: Real competitor summary.
* **🔲 SWOT Analysis**: Real SWOT with validated source references.
* **🎯 Opportunity Gaps**: Real opportunity gaps.
* **📦 Product Backlog**: Generated Epic and Stories representing a differentiated response hypothesis for the target product context (rather than a roadmap for the competitor).
* **📚 Evidence Sources**: Real sources retrieved by the Tavily agent. Sources are **not** labeled fictional, and display a note: *"Public evidence retrieved during this live run. Validate before relying on it."*

### Step 6: Export Report
The user downloads the generated report as `competitor-intelligence-live-brief.md` containing the prepended Target Product Context header.
