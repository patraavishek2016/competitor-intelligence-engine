from schemas import (
    EvidenceSource,
    AnalysisResult,
    SWOTAnalysis,
    OpportunityGap,
    EvidenceBackedInsight,
    Epic,
    UserStory
)
from agent_logic import (
    ResearchError,
    AnalysisError,
    BacklogGenerationError,
    create_competitor_workflow
)

# --- Mock Helpers ---

def make_valid_analysis_result():
    insight = EvidenceBackedInsight(
        statement="Competitor has sync functionality.",
        source_ids=["SRC-1"],
        confidence="high"
    )
    swot = SWOTAnalysis(strengths=[insight], weaknesses=[], opportunities=[], threats=[])
    gap1 = OpportunityGap(title="Gap 1", rationale="Rationale 1", source_ids=["SRC-1"], priority="high")
    gap2 = OpportunityGap(title="Gap 2", rationale="Rationale 2", source_ids=["SRC-1"], priority="medium")
    gap3 = OpportunityGap(title="Gap 3", rationale="Rationale 3", source_ids=["SRC-1"], priority="low")
    return AnalysisResult(
        executive_summary="Summary.",
        swot=swot,
        opportunity_gaps=[gap1, gap2, gap3]
    )

def make_valid_epic():
    ac = [
        "Given user logins, When login is valid, Then user is redirected",
        "Given user profile, When update triggers, Then changes persist",
        "Given active session, When logout executes, Then session is cleared"
    ]
    stories = [
        UserStory(title=f"Story {i}", as_a="User", i_want_to="do", so_that="benefit", acceptance_criteria=ac)
        for i in range(3)
    ]
    return Epic(
        title="Epic Title",
        description="Epic Description.",
        user_stories=stories
    )


# --- Workflow Tests ---

# 1. Successful workflow:
#    - Research executes first.
#    - Analysis executes second.
#    - Backlog Writer executes third.
#    - Final stage is "completed".
#    - Final result has sources, analysis, and epic.
#    - error is None.
def test_successful_workflow():
    calls = []
    captured_context = []

    def fake_research(url, tavily_api_key):
        calls.append("research")
        return [
            EvidenceSource(
                source_id="SRC-1",
                title="Title",
                url="https://competitor.com",
                excerpt="Excerpt",
                is_fictional=False
            )
        ]

    def fake_analysis(sources, openai_api_key, model_name):
        calls.append("analysis")
        return make_valid_analysis_result()

    def fake_backlog(analysis, openai_api_key, model_name, target_product_context):
        calls.append("backlog")
        captured_context.append(target_product_context)
        return make_valid_epic()

    app = create_competitor_workflow(
        research_fn=fake_research,
        analysis_fn=fake_analysis,
        backlog_fn=fake_backlog
    )

    initial_state = {
        "url": "https://competitor.com",
        "tavily_api_key": "dummy-tavily-key",
        "openai_api_key": "dummy-openai-key",
        "model_name": "gpt-4o-mini",
        "target_product_context": "B2B collaboration workspace",
        "sources": None,
        "analysis": None,
        "epic": None,
        "error": None,
        "stage": "not_started"
    }

    final_state = app.invoke(initial_state)

    assert calls == ["research", "analysis", "backlog"]
    assert final_state["stage"] == "completed"
    assert final_state["error"] is None
    assert final_state["target_product_context"] == "B2B collaboration workspace"
    assert captured_context == ["B2B collaboration workspace"]
    assert isinstance(final_state["sources"], list)
    assert len(final_state["sources"]) == 1
    assert isinstance(final_state["analysis"], AnalysisResult)
    assert isinstance(final_state["epic"], Epic)

# 2. Research failure:
#    - Research raises ResearchError.
#    - Workflow final stage is "failed".
#    - Workflow contains a safe error.
#    - Analyst is never called.
#    - Backlog Writer is never called.
def test_research_failure():
    calls = []

    def fake_research(url, tavily_api_key):
        calls.append("research")
        raise ResearchError("Safe research error details.")

    def fake_analysis(sources, openai_api_key, model_name):
        calls.append("analysis")
        return make_valid_analysis_result()

    def fake_backlog(analysis, openai_api_key, model_name, target_product_context):
        calls.append("backlog")
        return make_valid_epic()

    app = create_competitor_workflow(
        research_fn=fake_research,
        analysis_fn=fake_analysis,
        backlog_fn=fake_backlog
    )

    initial_state = {
        "url": "https://competitor.com",
        "target_product_context": "B2B context",
        "stage": "not_started"
    }

    final_state = app.invoke(initial_state)

    assert calls == ["research"]
    assert final_state["stage"] == "failed"
    assert final_state["error"] == "Safe research error details."
    assert final_state.get("sources") is None
    assert final_state.get("analysis") is None
    assert final_state.get("epic") is None

# 3. Analysis failure:
#    - Research succeeds.
#    - Analysis raises AnalysisError.
#    - Workflow final stage is "failed".
#    - Backlog Writer is never called.
def test_analysis_failure():
    calls = []

    def fake_research(url, tavily_api_key):
        calls.append("research")
        return [
            EvidenceSource(
                source_id="SRC-1",
                title="Title",
                url="https://competitor.com",
                excerpt="Excerpt",
                is_fictional=False
            )
        ]

    def fake_analysis(sources, openai_api_key, model_name):
        calls.append("analysis")
        raise AnalysisError("Safe strategic analysis error.")

    def fake_backlog(analysis, openai_api_key, model_name, target_product_context):
        calls.append("backlog")
        return make_valid_epic()

    app = create_competitor_workflow(
        research_fn=fake_research,
        analysis_fn=fake_analysis,
        backlog_fn=fake_backlog
    )

    initial_state = {
        "url": "https://competitor.com",
        "target_product_context": "B2B context",
        "stage": "not_started"
    }

    final_state = app.invoke(initial_state)

    assert calls == ["research", "analysis"]
    assert final_state["stage"] == "failed"
    assert final_state["error"] == "Safe strategic analysis error."
    assert final_state.get("epic") is None

# 4. Backlog failure:
#    - Research and analysis succeed.
#    - Backlog Writer raises BacklogGenerationError.
#    - Workflow final stage is "failed".
#    - Safe error is returned.
def test_backlog_failure():
    calls = []

    def fake_research(url, tavily_api_key):
        calls.append("research")
        return [
            EvidenceSource(
                source_id="SRC-1",
                title="Title",
                url="https://competitor.com",
                excerpt="Excerpt",
                is_fictional=False
            )
        ]

    def fake_analysis(sources, openai_api_key, model_name):
        calls.append("analysis")
        return make_valid_analysis_result()

    def fake_backlog(analysis, openai_api_key, model_name, target_product_context):
        calls.append("backlog")
        raise BacklogGenerationError("Safe backlog generation error.")

    app = create_competitor_workflow(
        research_fn=fake_research,
        analysis_fn=fake_analysis,
        backlog_fn=fake_backlog
    )

    initial_state = {
        "url": "https://competitor.com",
        "target_product_context": "B2B context",
        "stage": "not_started"
    }

    final_state = app.invoke(initial_state)

    assert calls == ["research", "analysis", "backlog"]
    assert final_state["stage"] == "failed"
    assert final_state["error"] == "Safe backlog generation error."

# 5. Unexpected exception:
#    - A fake function raises a generic exception containing sensitive-looking text.
#    - Final state must not expose that raw exception text.
def test_unexpected_exception_hides_raw_details():
    def fake_research(url, tavily_api_key):
        raise RuntimeError("CONNECTION FAILED: API_KEY=secret_key_123456 at line 42")

    app = create_competitor_workflow(
        research_fn=fake_research
    )

    initial_state = {
        "url": "https://competitor.com",
        "target_product_context": "B2B context",
        "stage": "not_started"
    }

    final_state = app.invoke(initial_state)

    assert final_state["stage"] == "failed"
    assert "secret_key" not in final_state["error"]
    assert "CONNECTION FAILED" not in final_state["error"]
    assert "Public research could not be completed" in final_state["error"]

# 6. Dependency injection:
#    - Tests prove the workflow can run entirely using injected fake functions.
#    - No API key or environment variable is required for tests.
def test_dependency_injection_no_keys_required():
    def fake_research(url, tavily_api_key):
        return [
            EvidenceSource(
                source_id="SRC-1",
                title="Title",
                url="https://competitor.com",
                excerpt="Excerpt",
                is_fictional=False
            )
        ]

    def fake_analysis(sources, openai_api_key, model_name):
        return make_valid_analysis_result()

    def fake_backlog(analysis, openai_api_key, model_name, target_product_context):
        return make_valid_epic()

    app = create_competitor_workflow(
        research_fn=fake_research,
        analysis_fn=fake_analysis,
        backlog_fn=fake_backlog
    )

    initial_state = {
        "url": "https://competitor.com",
        "target_product_context": "B2B context",
        "tavily_api_key": None,
        "openai_api_key": None,
        "stage": "not_started"
    }

    final_state = app.invoke(initial_state)
    assert final_state["stage"] == "completed"
    assert final_state["error"] is None
