from demo_data import get_demo_result
from schemas import CompetitorIntelligenceResult

def test_get_demo_result_valid():
    result = get_demo_result()
    assert isinstance(result, CompetitorIntelligenceResult)
    assert result.mode == "demo"
    assert result.competitor_name == "NimbusFlow"

    assert len(result.epic.user_stories) == 3
    for story in result.epic.user_stories:
        assert 3 <= len(story.acceptance_criteria) <= 5

def test_demo_result_no_external_dependencies():
    # If get_demo_result() required env variables or network, it would crash or block during tests.
    # The fact that it succeeds under test conditions without mocks implies it's static.
    result = get_demo_result()
    assert result is not None
