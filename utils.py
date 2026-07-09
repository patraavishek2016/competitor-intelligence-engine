import urllib.parse
import ipaddress
from schemas import CompetitorIntelligenceResult

def validate_public_url(url: str) -> str:
    if not url or not url.strip():
        raise ValueError("URL cannot be empty.")

    url = url.strip()

    if not url.startswith('http://') and not url.startswith('https://'):
        raise ValueError("URL must use HTTP or HTTPS scheme.")

    try:
        parsed = urllib.parse.urlparse(url)
    except Exception as e:
        raise ValueError(f"Invalid URL format: {e}")

    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use HTTP or HTTPS scheme.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname.")

    hostname_lower = hostname.lower()

    if hostname_lower == "localhost":
        raise ValueError("Localhost is not allowed.")

    # Check if it's an IP address
    is_ip = False
    try:
        ip = ipaddress.ip_address(hostname_lower)
        is_ip = True
    except ValueError:
        pass

    if is_ip:
        if ip.is_loopback:
            raise ValueError("Loopback IP addresses are not allowed.")
        if ip.is_private:
            raise ValueError("Private IP addresses are not allowed.")

    return urllib.parse.urlunparse(parsed)

def build_markdown_brief(result: CompetitorIntelligenceResult) -> str:
    lines = []

    # Disclaimer
    lines.append(f"**DISCLAIMER**: {result.disclaimer}")
    lines.append("")

    # Title
    lines.append(f"# Analysis Report: {result.competitor_name}")
    lines.append(f"**URL**: {result.competitor_url}")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append(result.analysis.executive_summary)
    lines.append("")

    # Sources
    lines.append("## Sources")
    for s in result.sources:
        fictional_tag = " *(Fictional)*" if s.is_fictional else ""
        lines.append(f"- **[{s.source_id}]** [{s.title}]({s.url}){fictional_tag}: {s.excerpt}")
    lines.append("")

    # SWOT
    lines.append("## SWOT Analysis")
    for category in ["strengths", "weaknesses", "opportunities", "threats"]:
        items = getattr(result.analysis.swot, category)
        if items:
            lines.append(f"### {category.capitalize()}")
            for item in items:
                sources_str = ", ".join(item.source_ids)
                lines.append(f"- {item.statement} *(Sources: {sources_str} | Confidence: {item.confidence})*")
    lines.append("")

    # Opportunity Gaps
    lines.append("## Opportunity Gaps")
    for gap in result.analysis.opportunity_gaps:
        sources_str = ", ".join(gap.source_ids)
        lines.append(f"### {gap.title} (Priority: {gap.priority})")
        lines.append(f"{gap.rationale}")
        lines.append(f"**Sources**: {sources_str}")
        lines.append("")

    # Epic
    lines.append("## Recommended Epic")
    lines.append(f"### {result.epic.title}")
    lines.append(result.epic.description)
    lines.append("")

    for idx, story in enumerate(result.epic.user_stories, 1):
        lines.append(f"#### Story {idx}: {story.title}")
        lines.append(f"**As a** {story.as_a},")
        lines.append(f"**I want to** {story.i_want_to},")
        lines.append(f"**So that** {story.so_that}.")
        lines.append("")
        lines.append("**Acceptance Criteria:**")
        for ac in story.acceptance_criteria:
            lines.append(f"- {ac}")
        lines.append("")

    return "\n".join(lines).strip()
