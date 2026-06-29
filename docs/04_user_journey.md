# User Journey — Competitor Intelligence Engine

## Demo Mode Journey

This document describes the end-to-end user journey for the **Demo Mode** of the Competitor Intelligence Engine, available as of Milestone 2.

---

### Step 1: Open App

The user launches the application locally:

```bash
streamlit run app.py
```

The browser opens to the Competitor Intelligence Engine home screen showing:
- The product title and positioning statement.
- A **Safety Notice** explaining outputs are hypotheses requiring human validation.
- A **Demo Mode badge** confirming no external API calls are made.

---

### Step 2: Review Demo Mode Disclaimer

Before interacting, the user reads and acknowledges two visible banners:

| Banner | Content |
|--------|---------|
| ⚠️ Safety Notice | "Generated outputs are product hypotheses and require human validation before strategic or implementation decisions." |
| 🔵 Demo Mode | "Fictional static demo data. No external API calls are made." |

This sets clear expectations: the results are illustrative and not derived from live research.

---

### Step 3: Run Demo Analysis

The user clicks the **▶ Run Demo Analysis** button.

- The application loads the `get_demo_result()` function from `demo_data.py`.
- No network calls, API keys, or environment variables are used.
- Results are stored in `st.session_state` so they persist across Streamlit reruns without re-triggering the load.
- A success confirmation message is shown immediately.

---

### Step 4: Review Outputs

Results are presented across **five labelled tabs**:

| Tab | Content |
|-----|---------|
| 📋 Executive Summary | High-level narrative summary of the competitor analysis |
| 🔲 SWOT Analysis | Strengths, Weaknesses, Opportunities, Threats — each with source IDs and confidence levels |
| 🎯 Opportunity Gaps | Prioritised product gaps with rationale and source traceability |
| 📦 Product Backlog | One Epic, three User Stories, and BDD-format acceptance criteria |
| 📚 Evidence Sources | All sources clearly labelled as fictional; no sources presented as verified |

The user may navigate freely between tabs. Results remain visible until the app is restarted.

---

### Step 5: Download Markdown Brief

On the **Executive Summary** tab, the user clicks:

> ⬇ **Download Markdown Brief**

This downloads `competitor-intelligence-demo-brief.md` — a complete, formatted summary of the full analysis including:
- Disclaimer
- Competitor name and URL
- Executive summary
- SWOT analysis
- Opportunity gaps
- Epic and User Stories with acceptance criteria
- Evidence sources

The brief is generated entirely by `build_markdown_brief()` from `utils.py` with no external calls.

---

### Future Journey (Milestone 3 Preview)

When **Live Research Mode** is released, the journey will extend to include:

- Inputting a real competitor URL.
- Triggering the Research Agent to retrieve live public sources.
- Reviewing AI-synthesised strategic insights grounded in retrieved evidence.
- Downloading an evidence-backed brief.

> This mode will only be available after API security, source retrieval, and access-control guardrails are fully implemented.
