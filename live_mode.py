import os
import hmac
import urllib.parse
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class LiveModeSettings:
    openai_api_key: str
    tavily_api_key: str
    model_name: str
    live_research_access_code: str

def load_live_mode_settings(env=None) -> LiveModeSettings:
    """
    Load environment configuration for Live Research Mode.
    If env mapping is provided, read strictly from it (for testing).
    Otherwise, load .env file and read from os.environ.
    """
    if env is None:
        load_dotenv(override=False)
        source = os.environ
    else:
        source = env

    openai_api_key = source.get("OPENAI_API_KEY", "").strip()
    tavily_api_key = source.get("TAVILY_API_KEY", "").strip()
    model_name = source.get("OPENAI_MODEL", "").strip()
    if not model_name:
        model_name = "gpt-4o-mini"
    live_research_access_code = source.get("LIVE_RESEARCH_ACCESS_CODE", "").strip()

    return LiveModeSettings(
        openai_api_key=openai_api_key,
        tavily_api_key=tavily_api_key,
        model_name=model_name,
        live_research_access_code=live_research_access_code
    )

def is_live_mode_configured(settings: LiveModeSettings) -> bool:
    """
    Verify whether all required keys and configuration parameters are set.
    """
    return bool(
        settings.openai_api_key and
        settings.tavily_api_key and
        settings.live_research_access_code
    )

def is_live_request_authorized(submitted_code: str, expected_code: str) -> bool:
    """
    Verify that the submitted access code matches the configured access code.
    Uses hmac.compare_digest for secure constant-time comparison.
    """
    if not submitted_code or not expected_code:
        return False
    return hmac.compare_digest(submitted_code.strip().encode("utf-8"), expected_code.strip().encode("utf-8"))

def build_live_workflow_input(url: str, settings: LiveModeSettings, target_product_context: str) -> dict:
    """
    Build the initial state dictionary required by create_competitor_workflow().invoke().
    """
    return {
        "url": url,
        "tavily_api_key": settings.tavily_api_key,
        "openai_api_key": settings.openai_api_key,
        "model_name": settings.model_name,
        "target_product_context": target_product_context,
        "sources": None,
        "analysis": None,
        "epic": None,
        "error": None,
        "stage": "not_started"
    }

class LiveResearchResult:
    """
    Duck-typed wrapper class that mimics CompetitorIntelligenceResult Pydantic schema,
    allowing the existing rendering blocks and build_markdown_brief() in utils.py
    to seamlessly render live research outcomes.
    """
    def __init__(self, state: dict):
        self.competitor_url = state.get("url", "")
        # Extract competitor name from url hostname
        try:
            hostname = urllib.parse.urlparse(self.competitor_url).hostname or "Competitor"
            self.competitor_name = hostname.replace("www.", "").split(".")[0].capitalize()
        except Exception:
            self.competitor_name = "Competitor"

        self.mode = "live"
        self.disclaimer = "Generated outputs are product hypotheses and require human validation before strategic or implementation decisions."
        self.sources = state.get("sources") or []
        self.analysis = state.get("analysis")
        self.epic = state.get("epic")
        self.target_product_context = state.get("target_product_context", "")
