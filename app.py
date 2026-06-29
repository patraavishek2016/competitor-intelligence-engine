import streamlit as st
from demo_data import get_demo_result
from utils import build_markdown_brief

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Competitor Intelligence Engine",
    page_icon="🧠",
    layout="wide",
)

# ─────────────────────────────────────────────
# Global CSS — clean, professional, no neon/gaming
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Typography ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Top header accent bar ── */
    [data-testid="stAppViewContainer"] > .main::before {
        content: "";
        display: block;
        height: 4px;
        background: linear-gradient(90deg, #1e40af, #3b82f6, #60a5fa);
        margin-bottom: 0;
    }

    /* ── Metric cards ── */
    .cie-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .cie-card-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .cie-card-body { font-size: 0.95rem; color: #1e293b; }

    /* ── SWOT coloured borders ── */
    .swot-strength  { border-left-color: #16a34a !important; }
    .swot-weakness  { border-left-color: #dc2626 !important; }
    .swot-opportunity { border-left-color: #2563eb !important; }
    .swot-threat    { border-left-color: #d97706 !important; }

    /* ── Priority badges ── */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-high   { background: #fee2e2; color: #991b1b; }
    .badge-medium { background: #fef3c7; color: #92400e; }
    .badge-low    { background: #dcfce7; color: #166534; }

    /* ── Confidence badges ── */
    .conf-high   { background: #dbeafe; color: #1e40af; }
    .conf-medium { background: #ede9fe; color: #5b21b6; }
    .conf-low    { background: #f1f5f9; color: #475569; }

    /* ── Disclaimer / info banners ── */
    .cie-disclaimer {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 8px;
        padding: 10px 16px;
        font-size: 0.875rem;
        color: #78350f;
        margin-bottom: 6px;
    }
    .cie-demo-badge {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 10px 16px;
        font-size: 0.875rem;
        color: #1e40af;
        margin-bottom: 16px;
    }
    .cie-future-note {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 10px 16px;
        font-size: 0.875rem;
        color: #166534;
        margin-top: 12px;
    }

    /* ── Source fiction label ── */
    .fiction-label {
        display: inline-block;
        background: #fce7f3;
        color: #9d174d;
        border-radius: 4px;
        padding: 1px 8px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Footer ── */
    .cie-footer {
        margin-top: 48px;
        padding-top: 16px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        font-size: 0.8rem;
        color: #94a3b8;
    }

    /* ── Streamlit tab tweaks ── */
    [data-baseweb="tab-list"] button {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.title("🧠 Competitor Intelligence Engine")

st.markdown(
    "**An evidence-grounded multi-agent AI prototype** that transforms public competitor research "
    "into strategic product opportunities and implementation-ready backlog recommendations."
)

st.markdown(
    '<div class="cie-disclaimer">'
    "⚠️ <strong>Safety notice:</strong> Generated outputs are product hypotheses and require "
    "human validation before strategic or implementation decisions."
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="cie-demo-badge">'
    "🔵 <strong>Demo Mode:</strong> Fictional static demo data. No external API calls are made."
    "</div>",
    unsafe_allow_html=True,
)

st.divider()

# ─────────────────────────────────────────────
# Primary action
# ─────────────────────────────────────────────
col_btn, col_info = st.columns([2, 5])
with col_btn:
    if st.button("▶ Run Demo Analysis", type="primary", use_container_width=True):
        with st.spinner("Loading demo analysis…"):
            st.session_state["cie_result"] = get_demo_result()
        st.success("Demo analysis loaded.")

with col_info:
    st.caption(
        "Loads the NimbusFlow fictional competitor analysis from static demo data. "
        "No network requests are made."
    )

# ─────────────────────────────────────────────
# Results — only if loaded
# ─────────────────────────────────────────────
if "cie_result" in st.session_state:
    result = st.session_state["cie_result"]

    st.divider()
    st.subheader(f"Analysis: {result.competitor_name}")
    st.caption(f"Competitor URL: {result.competitor_url} · Mode: `{result.mode}`")

    tab_summary, tab_swot, tab_gaps, tab_backlog, tab_sources = st.tabs([
        "📋 Executive Summary",
        "🔲 SWOT Analysis",
        "🎯 Opportunity Gaps",
        "📦 Product Backlog",
        "📚 Evidence Sources",
    ])

    # ── Tab 1: Executive Summary ──────────────────
    with tab_summary:
        st.markdown("#### Executive Summary")
        st.markdown(result.analysis.executive_summary)

        st.markdown("---")
        st.markdown("#### Export Report")
        md_content = build_markdown_brief(result)
        st.download_button(
            label="⬇ Download Markdown Brief",
            data=md_content.encode("utf-8"),
            file_name="competitor-intelligence-demo-brief.md",
            mime="text/markdown",
            help="Downloads the full analysis as a Markdown document.",
        )

    # ── Tab 2: SWOT Analysis ─────────────────────
    with tab_swot:
        st.markdown("#### SWOT Analysis")
        swot = result.analysis.swot
        sw_col, ot_col = st.columns(2)

        def render_insight(item, css_class: str):
            conf = item.confidence
            srcs = ", ".join(f"`{s}`" for s in item.source_ids)
            st.markdown(
                f'<div class="cie-card {css_class}">'
                f'<div class="cie-card-body">{item.statement}</div>'
                f"<div style='margin-top:6px;font-size:0.78rem;color:#64748b;'>"
                f"Sources: {srcs} &nbsp;|&nbsp; "
                f'<span class="badge conf-{conf}">{conf} confidence</span>'
                f"</div></div>",
                unsafe_allow_html=True,
            )

        with sw_col:
            st.markdown("**💪 Strengths**")
            for item in swot.strengths:
                render_insight(item, "swot-strength")
            st.markdown("**⚠️ Weaknesses**")
            for item in swot.weaknesses:
                render_insight(item, "swot-weakness")

        with ot_col:
            st.markdown("**🌱 Opportunities**")
            for item in swot.opportunities:
                render_insight(item, "swot-opportunity")
            st.markdown("**⚡ Threats**")
            for item in swot.threats:
                render_insight(item, "swot-threat")

    # ── Tab 3: Opportunity Gaps ───────────────────
    with tab_gaps:
        st.markdown("#### Opportunity Gaps")
        for idx, gap in enumerate(result.analysis.opportunity_gaps, 1):
            srcs = ", ".join(f"`{s}`" for s in gap.source_ids)
            st.markdown(
                f'<div class="cie-card">'
                f'<div class="cie-card-title">Gap {idx}</div>'
                f'<div class="cie-card-body"><strong>{gap.title}</strong> '
                f'<span class="badge badge-{gap.priority}">{gap.priority}</span></div>'
                f"<div style='margin-top:6px;font-size:0.9rem;color:#334155;'>{gap.rationale}</div>"
                f"<div style='margin-top:6px;font-size:0.78rem;color:#64748b;'>Sources: {srcs}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── Tab 4: Product Backlog ────────────────────
    with tab_backlog:
        epic = result.epic
        st.markdown(f"#### Epic: {epic.title}")
        st.markdown(f"*{epic.description}*")
        st.markdown("---")

        for s_idx, story in enumerate(epic.user_stories, 1):
            with st.expander(f"Story {s_idx}: {story.title}", expanded=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(
                        f"**As a** {story.as_a}  \n"
                        f"**I want to** {story.i_want_to}  \n"
                        f"**So that** {story.so_that}"
                    )
                with c2:
                    st.markdown("**Acceptance Criteria:**")
                    for ac in story.acceptance_criteria:
                        st.markdown(f"- {ac}")

    # ── Tab 5: Evidence Sources ───────────────────
    with tab_sources:
        st.markdown("#### Evidence Sources")
        st.info(
            "⚠️ These sources are **entirely fictional** and are provided for demonstration "
            "purposes only. They do not represent verified live research.",
            icon="ℹ️",
        )
        for src in result.sources:
            label = '<span class="fiction-label">Fictional</span>' if src.is_fictional else ""
            st.markdown(
                f'<div class="cie-card">'
                f'<div class="cie-card-title">[{src.source_id}] {src.title} &nbsp;{label}</div>'
                f'<div class="cie-card-body">{src.excerpt}</div>'
                f"<div style='margin-top:6px;font-size:0.78rem;color:#64748b;'>"
                f"URL: <code>{src.url}</code></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── Future capability notice ──────────────────
    st.markdown(
        '<div class="cie-future-note">'
        "🔭 <strong>Coming in Milestone 3:</strong> Live Research Mode will be introduced after "
        "API security, source retrieval, and access-control guardrails are implemented. "
        "It will include a live Research Agent, Strategic Analyst, and Backlog Writer."
        "</div>",
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        """
        <div style="text-align:center; padding:48px 0; color:#94a3b8;">
            <div style="font-size:3rem;">🧠</div>
            <div style="font-size:1.1rem; margin-top:12px;">
                Click <strong>Run Demo Analysis</strong> above to load the NimbusFlow competitor analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown(
    '<div class="cie-footer">'
    "Portfolio prototype by Avishek Patra · Demo Mode only · Built with Streamlit and Pydantic."
    "</div>",
    unsafe_allow_html=True,
)
