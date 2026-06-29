from schemas import (
    CompetitorIntelligenceResult, EvidenceSource, AnalysisResult, SWOTAnalysis,
    EvidenceBackedInsight, OpportunityGap, Epic, UserStory
)

def get_demo_result() -> CompetitorIntelligenceResult:
    sources = [
        EvidenceSource(
            source_id="src-1",
            title="NimbusFlow Features Overview",
            url="https://nimbusflow.example/features",
            excerpt="NimbusFlow offers a comprehensive suite of workflow automation tools designed for enterprise scale.",
            is_fictional=True
        ),
        EvidenceSource(
            source_id="src-2",
            title="SaaS Review: NimbusFlow Pricing",
            url="https://reviews.software.example/nimbusflow-pricing",
            excerpt="While feature-rich, NimbusFlow's enterprise pricing structure is prohibitively expensive for mid-market customers.",
            is_fictional=True
        ),
        EvidenceSource(
            source_id="src-3",
            title="NimbusFlow AI Integration Announcement",
            url="https://blog.nimbusflow.example/ai-capabilities",
            excerpt="We are launching beta AI integrations, but currently they lack custom prompt capabilities and remain rigid.",
            is_fictional=True
        ),
        EvidenceSource(
            source_id="src-4",
            title="Industry Trends in Workflow Automation",
            url="https://industry.trends.example/workflow-2026",
            excerpt="The market is rapidly shifting towards localized and private LLM deployments for data security in enterprise workflows.",
            is_fictional=True
        )
    ]

    swot = SWOTAnalysis(
        strengths=[
            EvidenceBackedInsight(
                statement="Comprehensive enterprise suite for workflow automation.",
                source_ids=["src-1"],
                confidence="high"
            )
        ],
        weaknesses=[
            EvidenceBackedInsight(
                statement="Enterprise tier pricing is too expensive for mid-market users.",
                source_ids=["src-2"],
                confidence="high"
            ),
            EvidenceBackedInsight(
                statement="AI capabilities are currently rigid without customization options.",
                source_ids=["src-3"],
                confidence="medium"
            )
        ],
        opportunities=[
            EvidenceBackedInsight(
                statement="Growing demand for localized LLM deployments in workflows.",
                source_ids=["src-4"],
                confidence="medium"
            )
        ],
        threats=[
            EvidenceBackedInsight(
                statement="Competitors capturing the mid-market due to NimbusFlow's high costs.",
                source_ids=["src-2"],
                confidence="high"
            )
        ]
    )

    opportunity_gaps = [
        OpportunityGap(
            title="Mid-Market Pricing Tier",
            rationale="Capturing users priced out of NimbusFlow by offering a lower-cost tier.",
            source_ids=["src-2"],
            priority="high"
        ),
        OpportunityGap(
            title="Custom AI Prompt Engine",
            rationale="Providing flexibility that NimbusFlow currently lacks in its AI beta.",
            source_ids=["src-3"],
            priority="high"
        ),
        OpportunityGap(
            title="On-Premise LLM Support",
            rationale="Addressing the industry trend for private, secure enterprise deployments.",
            source_ids=["src-4"],
            priority="medium"
        ),
        OpportunityGap(
            title="Quick-Start Templates",
            rationale="Lowering the barrier to entry compared to deep enterprise configurations.",
            source_ids=["src-1"],
            priority="low"
        )
    ]

    epic = Epic(
        title="Custom AI Prompt Engine Development",
        description="Develop a flexible AI prompt management system to differentiate from rigid competitors.",
        user_stories=[
            UserStory(
                title="Create Custom Prompt Templates",
                as_a="Workflow Administrator",
                i_want_to="create custom AI prompt templates",
                so_that="I can tailor the AI outputs to my specific department's needs",
                acceptance_criteria=[
                    "Given I am on the prompt builder screen, When I click 'New Template', Then an editor is shown.",
                    "Given I am in the editor, When I save valid prompt text, Then it is stored in my template library.",
                    "Given I view my templates, When I select a template, Then I can use it in a workflow step."
                ]
            ),
            UserStory(
                title="Dynamic Variable Injection in Prompts",
                as_a="Process Designer",
                i_want_to="inject workflow variables into my prompts",
                so_that="the AI context is automatically updated based on live data",
                acceptance_criteria=[
                    "Given I am editing a prompt, When I type '@', Then a variable autocomplete menu appears.",
                    "Given I have injected a variable, When the workflow runs, Then the variable resolves to its actual value.",
                    "Given a variable is missing, When the prompt executes, Then a fallback or error is gracefully handled."
                ]
            ),
            UserStory(
                title="Enterprise Prompt Security Controls",
                as_a="Security Officer",
                i_want_to="restrict access to certain prompt execution engines",
                so_that="sensitive workflows are processed only by approved models",
                acceptance_criteria=[
                    "Given I am in the admin panel, When I configure model access, Then I can assign roles per model.",
                    "Given a user without access runs a workflow, When the prompt step starts, Then execution is blocked.",
                    "Given a blocked execution, When it occurs, Then an audit log is securely recorded."
                ]
            )
        ]
    )

    return CompetitorIntelligenceResult(
        competitor_name="NimbusFlow",
        competitor_url="https://nimbusflow.example",
        mode="demo",
        disclaimer="WARNING: This is fictional demo data for NimbusFlow used entirely for demonstration and validation purposes.",
        sources=sources,
        analysis=AnalysisResult(
            executive_summary="NimbusFlow is a leading enterprise workflow competitor, but presents opportunities in mid-market pricing and flexible AI features.",
            swot=swot,
            opportunity_gaps=opportunity_gaps
        ),
        epic=epic
    )
