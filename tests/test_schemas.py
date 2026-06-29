import pytest
from pydantic import ValidationError
from schemas import Epic, UserStory, OpportunityGap, EvidenceBackedInsight

def test_valid_user_story():
    story = UserStory(
        title="Test",
        as_a="User",
        i_want_to="Test",
        so_that="It works",
        acceptance_criteria=[
            "Given A, When B, Then C",
            "Given X, When Y, Then Z",
            "Given 1, When 2, Then 3"
        ]
    )
    assert story.title == "Test"

def test_invalid_acceptance_criteria_count():
    with pytest.raises(ValidationError):
        UserStory(
            title="Test",
            as_a="User",
            i_want_to="Test",
            so_that="It works",
            acceptance_criteria=[
                "Given A, When B, Then C"
            ]
        )
    with pytest.raises(ValidationError):
        UserStory(
            title="Test",
            as_a="User",
            i_want_to="Test",
            so_that="It works",
            acceptance_criteria=[
                "Given A, When B, Then C",
                "Given A, When B, Then C",
                "Given A, When B, Then C",
                "Given A, When B, Then C",
                "Given A, When B, Then C",
                "Given A, When B, Then C"
            ]
        )

def test_invalid_acceptance_criteria_format():
    with pytest.raises(ValidationError):
        UserStory(
            title="Test",
            as_a="User",
            i_want_to="Test",
            so_that="It works",
            acceptance_criteria=[
                "Given A, When B, Then C",
                "Given X, When Y, Then Z",
                "Invalid criteria format without the keywords"
            ]
        )

def test_invalid_epic_story_count():
    story = UserStory(
        title="Test",
        as_a="User",
        i_want_to="Test",
        so_that="It works",
        acceptance_criteria=[
            "Given A, When B, Then C",
            "Given X, When Y, Then Z",
            "Given 1, When 2, Then 3"
        ]
    )
    with pytest.raises(ValidationError):
        Epic(
            title="Test Epic",
            description="Test describing it",
            user_stories=[story, story]
        )

def test_insight_requires_source():
    with pytest.raises(ValidationError):
        EvidenceBackedInsight(
            statement="Test",
            source_ids=[],
            confidence="high"
        )

def test_opportunity_requires_source():
    with pytest.raises(ValidationError):
        OpportunityGap(
            title="Test",
            rationale="Test",
            source_ids=[],
            priority="low"
        )
