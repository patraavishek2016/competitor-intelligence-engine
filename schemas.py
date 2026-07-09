from typing import List, Literal
from pydantic import BaseModel, Field, field_validator

class EvidenceSource(BaseModel):
    source_id: str = Field(..., description="Unique identifier for the source")
    title: str = Field(..., description="Title of the source Document or Article")
    url: str = Field(..., description="URL of the source")
    excerpt: str = Field(..., description="Relevant excerpt from the source")
    is_fictional: bool = Field(False, description="Flag indicating if the source is fictional")

class EvidenceBackedInsight(BaseModel):
    statement: str = Field(..., description="The insight statement")
    source_ids: List[str] = Field(..., min_length=1, description="List of source IDs backing this insight. Must contain at least one source ID.")
    confidence: Literal["high", "medium", "low"] = Field(..., description="Confidence level of the insight")

class SWOTAnalysis(BaseModel):
    strengths: List[EvidenceBackedInsight] = Field(..., description="List of strengths")
    weaknesses: List[EvidenceBackedInsight] = Field(..., description="List of weaknesses")
    opportunities: List[EvidenceBackedInsight] = Field(..., description="List of opportunities")
    threats: List[EvidenceBackedInsight] = Field(..., description="List of threats")

class OpportunityGap(BaseModel):
    title: str = Field(..., description="Title of the opportunity gap")
    rationale: str = Field(..., description="Rationale behind the opportunity gap")
    source_ids: List[str] = Field(..., min_length=1, description="List of source IDs backing this gap. Must contain at least one source ID.")
    priority: Literal["high", "medium", "low"] = Field(..., description="Priority of the opportunity gap")

class UserStory(BaseModel):
    title: str = Field(..., description="Title of the user story")
    as_a: str = Field(..., description="The user persona (As a...)")
    i_want_to: str = Field(..., description="The objective (I want to...)")
    so_that: str = Field(..., description="The benefit (So that...)")
    acceptance_criteria: List[str] = Field(..., min_length=3, max_length=5, description="List of 3 to 5 acceptance criteria")

    @field_validator("acceptance_criteria")
    @classmethod
    def validate_acceptance_criteria(cls, v: List[str]) -> List[str]:
        for idx, ac in enumerate(v):
            lower_ac = ac.lower()
            if not ("given" in lower_ac and "when" in lower_ac and "then" in lower_ac):
                raise ValueError(f"Acceptance criterion at index {idx} must contain 'Given', 'When', and 'Then'")
        return v

class Epic(BaseModel):
    title: str = Field(..., description="Title of the Epic")
    description: str = Field(..., description="Description of the Epic")
    user_stories: List[UserStory] = Field(..., min_length=3, max_length=3, description="List of exactly 3 user stories")

class AnalysisResult(BaseModel):
    executive_summary: str = Field(..., description="Executive summary of the analysis")
    swot: SWOTAnalysis = Field(..., description="SWOT Analysis")
    opportunity_gaps: List[OpportunityGap] = Field(..., min_length=3, max_length=5, description="List of 3 to 5 opportunity gaps")

class CompetitorIntelligenceResult(BaseModel):
    competitor_name: str = Field(..., description="Name of the competitor")
    competitor_url: str = Field(..., description="URL of the competitor")
    mode: Literal["demo"] = Field(..., description="Must explicitly be 'demo'")
    disclaimer: str = Field(..., description="Disclaimer regarding the data source")
    sources: List[EvidenceSource] = Field(..., description="List of sources used")
    analysis: AnalysisResult = Field(..., description="The full analysis result")
    epic: Epic = Field(..., description="The generated Epic")
