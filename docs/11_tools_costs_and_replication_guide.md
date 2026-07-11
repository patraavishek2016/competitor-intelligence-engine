# Tools, Costs, and Replication Guide

---

## Summary
This guide provides a comprehensive overview of the technical tools, operational cost structures, security configurations, and replication steps required to run and deploy the **Competitor Intelligence Engine**. 

Designed as a modular, low-cost portfolio showcase, the architecture supports both a zero-cost local static evaluation mode (Demo Mode) and a secure, evidence-grounded agentic workflow execution mode (Live Research Mode).

---

## Tools Used and Why

### Agentic AI & Search Stack
* **LangGraph**: Used as the orchestrator to build a stateful, multi-agent execution pipeline. It enables deterministic transitions between research, analysis, and drafting nodes, and handles retries or halts cleanly.
* **Tavily**: An AI-native search engine designed specifically for LLMs. It handles domain normalizations, canonicalizes target competitor hostnames, and extracts webpage texts.
* **OpenAI API**: Powering the strategic analyst and requirements backlog nodes (using GPT-4o). It parses raw unstructured evidence and generates structured SWOT and agile User Stories.

### Local Development & Languages
* **Python**: The core programming language, selected for its rich ecosystems in AI agents, data validation, and web applications.
* **PowerShell**: Used for local terminal interactions, shell-based diagnostics, and automation tasks.
* **Antigravity**: The pair-programming AI coding assistant utilized to edit and refine the codebase, ensure Pydantic contract integrations, and write comprehensive public case study documentation.

### Interface & Validation
* **Streamlit**: Selected as the web application framework. It provides a clean, responsive Python-native UI to demonstrate SWOT tables, opportunity cards, and Epic backlog navigation.
* **Pydantic**: Acts as the system's runtime validation boundary. Pydantic v2 schemas programmatically verify that LLM outputs conform to required field structures (e.g., Given/When/Then acceptance criteria counts and stable source citations).

### Quality & Linting Stack
* **Pytest**: Used as the testing framework. The suite includes mocked tests verifying domain validation, early-stopping loops, and regex BDD format rules without active API connections.
* **Ruff**: Employed as the fast linter and formatter to ensure clean, PEP-8 compliant code hygiene across all scripts.

### Containerization & Hosting Stack
* **Docker**: Packages the application into a portable, isolated image, guaranteeing that local runs match the cloud production runtime.
* **GitHub**: Used for codebase version control, dependency tracking, and open-source hosting.
* **Hugging Face Spaces**: Hosts the live Streamlit instance using the Docker SDK, providing low-overhead, containerized cloud application hosting.
* **Vercel**: Serves as the landing portfolio directory, routing visitors to the live Hugging Face Space instance.

---

## Secrets and Environment Variables

To operate the Competitor Intelligence Engine, three environment variables must be configured. These secrets are loaded at server-side runtime and are never exposed to public clients.

| Environment Variable | Description | Requirement |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | OpenAI API credential for GPT-4o reasoning. | Required for Live Research Mode |
| `TAVILY_API_KEY` | Tavily API credential for web searches. | Required for Live Research Mode |
| `LIVE_RESEARCH_ACCESS_CODE` | A secure password to gate and authorize Live Mode executions. | Required for Live Research Mode |

> [!WARNING]
> **Never commit your `.env` file or raw API keys to GitHub.** Ensure `.env` is listed in your `.gitignore` to prevent secret leaks.

---

## Approximate Cost Model

### Free-Mode Path
* **Demo Mode is free to run and makes no external API calls.**
* Users can run the Streamlit UI, explore SWOT grids, navigate opportunity cards, export markdown briefs, and run the complete test suite offline for **$0**.

### Paid Live Research Mode Cost Considerations
Live Research Mode triggers active web searches and LLM text generation, incurring API costs on your provider billing sheets.

1. **Tavily API Costs**:
   - Each search query consumes search credits.
   - The engine utilizes site-scoped fallback query strings and an **early-stopping control** that halts subsequent queries as soon as $\ge 2$ unique pages are retrieved, keeping Tavily credits focused.
2. **OpenAI API Costs**:
   - Charges are calculated based on input and output tokens for GPT-4o.
   - External web excerpts are truncated to 300 characters before prompt packaging, managing context window inflation.
   - On average, a complete Live Research execution run costs between **$0.02 and $0.05** in OpenAI API tokens.

> [!IMPORTANT]
> **Check official provider pricing sheets.** API pricing is subject to change by OpenAI and Tavily; always review their active fee structures to set appropriate billing alerts.

### Hosting Costs
* **Hugging Face CPU Basic**: The application runs within Hugging Face Spaces on a free CPU Basic hardware container, costing **$0/month** for public hosting.
* **Vercel Hobby**: The portfolio showcase and routing layer are hosted on Vercel's Hobby Tier, which is **free** for personal use.

---

## Replication Steps

### 1. Local Setup
Clone the codebase and navigate to the project root:
```powershell
git clone https://github.com/patraavishek2016/competitor-intelligence-engine.git
cd competitor-intelligence-engine
```

Create a virtual environment and activate it:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install development and runtime dependencies:
```powershell
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
LIVE_RESEARCH_ACCESS_CODE=your-custom-passcode
```

### 3. Run the App
Launch the local Streamlit development server:
```powershell
streamlit run app.py
```
Open `http://localhost:8501` in your browser. Select **Demo Mode** to run keyless, or validate with your `LIVE_RESEARCH_ACCESS_CODE` to run **Live Research Mode**.

### 4. Running the Tests
Execute the local test suite using Pytest to verify logic and schemas:
```powershell
pytest
```

### 5. Docker Containerization
Verify container packaging locally:
```powershell
# Build the Docker image
docker build -t competitor-intelligence-engine .

# Run the container locally using your environment variables
docker run -p 7860:7860 --env-file .env competitor-intelligence-engine
```
Access the local container application at `http://localhost:7860`.

### 6. Cloud Deployment (Hugging Face Spaces)
1. Create a new Space on [Hugging Face](https://huggingface.co/) and select the **Docker** SDK with the blank template.
2. Clone your Hugging Face Space repository or link it to your GitHub workflow.
3. In Hugging Face, navigate to **Settings** -> **Variables and secrets**.
4. Add your secrets:
   - `OPENAI_API_KEY`
   - `TAVILY_API_KEY`
   - `LIVE_RESEARCH_ACCESS_CODE`
5. Push the codebase. Hugging Face will automatically parse the `Dockerfile`, compile the image, and serve the application on port `7860`.

---

## Cost-Control Recommendations
* **Always set billing alert thresholds** in your OpenAI and Tavily developer dashboards.
* Ensure the **relevance gate** is active, stopping search execution immediately once the target threshold is met.
* Rely on **Demo Mode** for design and UI styling iterations to avoid making unnecessary Live API calls during frontend layout development.
