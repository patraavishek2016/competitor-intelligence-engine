import pytest
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
    AnalysisError,
    BacklogGenerationError,
    build_evidence_context,
    analyze_competitor_evidence,
    generate_backlog
)

# --- Fake Structured Model ---

class FakeStructuredModel:
    def __init__(self, response=None, should_raise=False):
        self.response = response
        self.should_raise = should_raise
        self.calls = []

    def invoke(self, messages):
        self.calls.append(messages)
        if self.should_raise:
            raise Exception("Simulated OpenAI API / Provider Exception")
        return self.response


# --- Helper Generators for Mock Pydantic Data ---

def make_valid_analysis_result(source_ids=["SRC-1"]):
    insight = EvidenceBackedInsight(
        statement="Competitor cloud instance offers 99.9% uptime SLA.",
        source_ids=source_ids,
        confidence="high"
    )
    swot = SWOTAnalysis(
        strengths=[insight],
        weaknesses=[],
        opportunities=[],
        threats=[]
    )
    gap1 = OpportunityGap(
        title="Sync Support",
        rationale="Needs offline capabilities.",
        source_ids=source_ids,
        priority="high"
    )
    gap2 = OpportunityGap(
        title="AI Automation",
        rationale="No built-in automation.",
        source_ids=source_ids,
        priority="medium"
    )
    gap3 = OpportunityGap(
        title="Custom Templates",
        rationale="Restricts customization.",
        source_ids=source_ids,
        priority="low"
    )
    return AnalysisResult(
        executive_summary="Overview summary text here.",
        swot=swot,
        opportunity_gaps=[gap1, gap2, gap3]
    )

def make_valid_epic():
    ac = [
        "Given user logins, When login is valid, Then user is redirected",
        "Given user profile, When update triggers, Then changes persist",
        "Given active session, When logout executes, Then session is cleared"
    ]
    story1 = UserStory(
        title="Story One",
        as_a="User",
        i_want_to="do one",
        so_that="benefit one",
        acceptance_criteria=ac
    )
    story2 = UserStory(
        title="Story Two",
        as_a="User",
        i_want_to="do two",
        so_that="benefit two",
        acceptance_criteria=ac
    )
    story3 = UserStory(
        title="Story Three",
        as_a="User",
        i_want_to="do three",
        so_that="benefit three",
        acceptance_criteria=ac
    )
    return Epic(
        title="Valid Epic Title",
        description="Epic Description Text.",
        user_stories=[story1, story2, story3]
    )


# --- Unit Tests ---

# 1. build_evidence_context includes source IDs, titles, URLs, and excerpts.
def test_build_evidence_context_includes_required_fields():
    sources = [
        EvidenceSource(
            source_id="SRC-1",
            title="Strategic Pricing",
            url="https://competitor.com/pricing",
            excerpt="Starts at $50/mo.",
            is_fictional=False
        ),
        EvidenceSource(
            source_id="SRC-2",
            title="Core Features List",
            url="https://competitor.com/features",
            excerpt="Includes custom workflows.",
            is_fictional=False
        )
    ]
    context = build_evidence_context(sources)

    assert "SRC-1" in context
    assert "Strategic Pricing" in context
    assert "https://competitor.com/pricing" in context
    assert "Starts at $50/mo." in context

    assert "SRC-2" in context
    assert "Core Features List" in context
    assert "https://competitor.com/features" in context
    assert "Includes custom workflows." in context

    assert "UNTRUSTED REFERENCE MATERIAL" in context

# 2. build_evidence_context rejects empty evidence.
def test_build_evidence_context_rejects_empty():
    with pytest.raises(AnalysisError, match="no evidence sources provided"):
        build_evidence_context([])

# 3. Strategic Analyst returns a valid AnalysisResult using an injected fake model.
def test_analyst_returns_valid_analysis():
    sources = [
        EvidenceSource(
            source_id="SRC-1",
            title="Competitor Details",
            url="https://competitor.com",
            excerpt="Competitor info.",
            is_fictional=False
        )
    ]
    expected_result = make_valid_analysis_result(["SRC-1"])
    fake_model = FakeStructuredModel(response=expected_result)

    result = analyze_competitor_evidence(sources, structured_model=fake_model)

    assert isinstance(result, AnalysisResult)
    assert result.executive_summary == expected_result.executive_summary
    assert len(result.opportunity_gaps) == 3

# 4. Analyst prompt contains target phrases and source details.
def test_analyst_prompt_contents():
    sources = [
        EvidenceSource(
            source_id="SRC-1",
            title="Competitor Details",
            url="https://competitor.com",
            excerpt="Competitor info.",
            is_fictional=False
        )
    ]
    expected_result = make_valid_analysis_result(["SRC-1"])
    fake_model = FakeStructuredModel(response=expected_result)

    analyze_competitor_evidence(sources, structured_model=fake_model)

    assert len(fake_model.calls) == 1
    messages = fake_model.calls[0]

    system_prompt = next(m["content"] for m in messages if m["role"] == "system")
    user_prompt = next(m["content"] for m in messages if m["role"] == "user")

    assert "untrusted reference material" in system_prompt
    assert "do not invent" in system_prompt.lower()
    assert "SRC-1" in user_prompt
    assert "Competitor Details" in user_prompt

# 5. Analyst rejects unknown source IDs.
def test_analyst_rejects_unknown_source_ids():
    sources = [
        EvidenceSource(
            source_id="SRC-1",
            title="Competitor Details",
            url="https://competitor.com",
            excerpt="Competitor info.",
            is_fictional=False
        )
    ]
    invalid_result = make_valid_analysis_result(["SRC-99"])
    fake_model = FakeStructuredModel(response=invalid_result)

    with pytest.raises(AnalysisError, match="references unknown source ID"):
        analyze_competitor_evidence(sources, structured_model=fake_model)

# 6. Analyst converts fake provider exceptions into AnalysisError without exposing raw exception text.
def test_analyst_handles_provider_exceptions():
    sources = [
        EvidenceSource(
            source_id="SRC-1",
            title="Competitor Details",
            url="https://competitor.com",
            excerpt="Competitor info.",
            is_fictional=False
        )
    ]
    fake_model = FakeStructuredModel(should_raise=True)

    with pytest.raises(AnalysisError) as exc_info:
        analyze_competitor_evidence(sources, structured_model=fake_model)

    assert "Simulated OpenAI API / Provider Exception" not in str(exc_info.value)
    assert "Strategic analysis could not be completed. Please try again." in str(exc_info.value)

# 7. Analyst requires no API key when an injected model is supplied.
def test_analyst_requires_no_key_when_injected():
    sources = [
        EvidenceSource(
            source_id="SRC-1",
            title="Competitor Details",
            url="https://competitor.com",
            excerpt="Competitor info.",
            is_fictional=False
        )
    ]
    expected_result = make_valid_analysis_result(["SRC-1"])
    fake_model = FakeStructuredModel(response=expected_result)

    result = analyze_competitor_evidence(sources, openai_api_key=None, structured_model=fake_model)
    assert result is not None

# 8. Backlog Writer returns a valid Epic using an injected fake model.
def test_backlog_writer_returns_valid_epic():
    analysis = make_valid_analysis_result(["SRC-1"])
    expected_epic = make_valid_epic()
    fake_model = FakeStructuredModel(response=expected_epic)
    context = "Differentiated async task app context"

    epic = generate_backlog(analysis, structured_model=fake_model, target_product_context=context)

    assert isinstance(epic, Epic)
    assert epic.title == expected_epic.title
    assert len(epic.user_stories) == 3

# 9. Backlog Writer output contains exactly three stories through Pydantic validation.
def test_backlog_writer_contains_exactly_three_stories():
    analysis = make_valid_analysis_result(["SRC-1"])
    expected_epic = make_valid_epic()
    fake_model = FakeStructuredModel(response=expected_epic)
    context = "Differentiated async task app context"

    epic = generate_backlog(analysis, structured_model=fake_model, target_product_context=context)
    assert len(epic.user_stories) == 3

# 10. Invalid backlog outputs, such as two user stories, raise BacklogGenerationError.
def test_invalid_backlog_raises_error():
    analysis = make_valid_analysis_result(["SRC-1"])
    epic_dict = make_valid_epic().model_dump()
    epic_dict["user_stories"] = epic_dict["user_stories"][:2]
    fake_model = FakeStructuredModel(response=epic_dict)
    context = "Differentiated async task app context"

    with pytest.raises(BacklogGenerationError, match="returned invalid data structure"):
        generate_backlog(analysis, structured_model=fake_model, target_product_context=context)

# 11. Backlog Writer converts fake provider exceptions into BacklogGenerationError without exposing raw exception text.
def test_backlog_writer_handles_provider_exceptions():
    analysis = make_valid_analysis_result(["SRC-1"])
    fake_model = FakeStructuredModel(should_raise=True)
    context = "Differentiated async task app context"

    with pytest.raises(BacklogGenerationError) as exc_info:
        generate_backlog(analysis, structured_model=fake_model, target_product_context=context)

    assert "Simulated OpenAI API / Provider Exception" not in str(exc_info.value)
    assert "Product backlog generation could not be completed. Please try again." in str(exc_info.value)

# 12. Backlog Writer requires no API key when an injected model is supplied.
def test_backlog_writer_requires_no_key_when_injected():
    analysis = make_valid_analysis_result(["SRC-1"])
    expected_epic = make_valid_epic()
    fake_model = FakeStructuredModel(response=expected_epic)
    context = "Differentiated async task app context"

    epic = generate_backlog(analysis, openai_api_key=None, structured_model=fake_model, target_product_context=context)
    assert epic is not None

# 13. Blank target-product context raises BacklogGenerationError before model invocation.
def test_blank_target_product_context_raises_error():
    analysis = make_valid_analysis_result(["SRC-1"])
    expected_epic = make_valid_epic()
    fake_model = FakeStructuredModel(response=expected_epic)

    # Empty string
    with pytest.raises(BacklogGenerationError, match="Target product context cannot be blank."):
        generate_backlog(analysis, structured_model=fake_model, target_product_context="")
    # Whitespace
    with pytest.raises(BacklogGenerationError, match="Target product context cannot be blank."):
        generate_backlog(analysis, structured_model=fake_model, target_product_context="   ")

    assert len(fake_model.calls) == 0

# 14. Target-product context is included in the Backlog Writer prompt, and competitor is not roadmap recipient.
def test_backlog_writer_prompt_contains_context_and_guards():
    analysis = make_valid_analysis_result(["SRC-1"])
    expected_epic = make_valid_epic()
    fake_model = FakeStructuredModel(response=expected_epic)
    context = "Special Secure Async Auditing Workspace context"

    generate_backlog(analysis, structured_model=fake_model, target_product_context=context)

    assert len(fake_model.calls) == 1
    messages = fake_model.calls[0]

    system_prompt = next(m["content"] for m in messages if m["role"] == "system")

    assert "Special Secure Async Auditing Workspace context" in system_prompt
    assert "competitor is an evidence source, not the roadmap recipient" in system_prompt
    assert "Do not title the Epic as 'Enhancing" in system_prompt
    assert "Do not write user stories as though users are using the competitor product" in system_prompt
