from live_mode import (
    load_live_mode_settings,
    is_live_mode_configured,
    is_live_request_authorized,
    build_live_workflow_input,
    LiveModeSettings
)

# 1. Settings load correctly from an injected mapping.
def test_settings_load_correctly():
    env = {
        "OPENAI_API_KEY": "openai-123",
        "TAVILY_API_KEY": "tavily-456",
        "OPENAI_MODEL": "gpt-4",
        "LIVE_RESEARCH_ACCESS_CODE": "access-789"
    }
    settings = load_live_mode_settings(env)
    assert settings.openai_api_key == "openai-123"
    assert settings.tavily_api_key == "tavily-456"
    assert settings.model_name == "gpt-4"
    assert settings.live_research_access_code == "access-789"

# 2. Default model name becomes gpt-4o-mini when OPENAI_MODEL is absent or empty.
def test_default_model_name():
    # Absent
    env1 = {
        "OPENAI_API_KEY": "openai-123",
        "TAVILY_API_KEY": "tavily-456",
        "LIVE_RESEARCH_ACCESS_CODE": "access-789"
    }
    settings1 = load_live_mode_settings(env1)
    assert settings1.model_name == "gpt-4o-mini"

    # Empty
    env2 = {
        "OPENAI_API_KEY": "openai-123",
        "TAVILY_API_KEY": "tavily-456",
        "OPENAI_MODEL": "",
        "LIVE_RESEARCH_ACCESS_CODE": "access-789"
    }
    settings2 = load_live_mode_settings(env2)
    assert settings2.model_name == "gpt-4o-mini"

# 3. Missing configuration is detected without revealing secret values.
def test_missing_configuration_detected():
    # Missing OpenAI key
    env1 = {
        "TAVILY_API_KEY": "tavily-456",
        "LIVE_RESEARCH_ACCESS_CODE": "access-789"
    }
    settings1 = load_live_mode_settings(env1)
    assert is_live_mode_configured(settings1) is False

    # Missing Tavily key
    env2 = {
        "OPENAI_API_KEY": "openai-123",
        "LIVE_RESEARCH_ACCESS_CODE": "access-789"
    }
    settings2 = load_live_mode_settings(env2)
    assert is_live_mode_configured(settings2) is False

    # Missing access code
    env3 = {
        "OPENAI_API_KEY": "openai-123",
        "TAVILY_API_KEY": "tavily-456"
    }
    settings3 = load_live_mode_settings(env3)
    assert is_live_mode_configured(settings3) is False

    # Complete configuration
    env_complete = {
        "OPENAI_API_KEY": "openai-123",
        "TAVILY_API_KEY": "tavily-456",
        "LIVE_RESEARCH_ACCESS_CODE": "access-789"
    }
    settings_complete = load_live_mode_settings(env_complete)
    assert is_live_mode_configured(settings_complete) is True

# 4. Correct access code is accepted.
def test_correct_access_code_accepted():
    assert is_live_request_authorized("my-code", "my-code") is True

# 5. Incorrect, blank, and missing access codes are rejected.
def test_incorrect_and_invalid_access_codes_rejected():
    # Incorrect
    assert is_live_request_authorized("wrong-code", "expected-code") is False
    # Blank submitted
    assert is_live_request_authorized("", "expected-code") is False
    assert is_live_request_authorized("   ", "expected-code") is False
    # Blank expected
    assert is_live_request_authorized("my-code", "") is False
    assert is_live_request_authorized("my-code", "   ") is False
    # Both blank
    assert is_live_request_authorized("", "") is False

# 6. Workflow input contains expected internal state fields.
def test_workflow_input_contains_expected_fields():
    settings = LiveModeSettings(
        openai_api_key="op-key",
        tavily_api_key="tv-key",
        model_name="gpt-4o-mini",
        live_research_access_code="ac-code"
    )
    context = "Target B2B product context"
    wf_input = build_live_workflow_input("https://competitor.com", settings, context)

    assert wf_input["url"] == "https://competitor.com"
    assert wf_input["tavily_api_key"] == "tv-key"
    assert wf_input["openai_api_key"] == "op-key"
    assert wf_input["model_name"] == "gpt-4o-mini"
    assert wf_input["target_product_context"] == context
    assert wf_input["sources"] is None
    assert wf_input["analysis"] is None
    assert wf_input["epic"] is None
    assert wf_input["error"] is None
    assert wf_input["stage"] == "not_started"

# 7. Workflow input contains no UI-specific fields.
def test_workflow_input_contains_no_ui_specific_fields():
    settings = LiveModeSettings(
        openai_api_key="op-key",
        tavily_api_key="tv-key",
        model_name="gpt-4o-mini",
        live_research_access_code="ac-code"
    )
    wf_input = build_live_workflow_input("https://competitor.com", settings, "Target product context")

    # Assert no access code or UI state variables are inside the workflow input dictionary
    assert "live_research_access_code" not in wf_input
    assert "access_code" not in wf_input
    assert "submitted" not in wf_input

# 8. No test depends on a local .env file.
# Handled by passing explicit dictionary values to `load_live_mode_settings` in all tests.
