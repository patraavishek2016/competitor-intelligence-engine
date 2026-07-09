import pytest
from agent_logic import (
    ResearchError,
    build_research_query,
    research_competitor,
    get_canonical_domain,
    is_subdomain_of
)
from schemas import EvidenceSource

class FakeTavilyClient:
    def __init__(self, search_response=None, should_raise=False, responses_list=None):
        self.search_response = search_response
        self.should_raise = should_raise
        self.responses_list = responses_list or []
        self.calls = []

    def search(self, query, max_results=5, include_domains=None):
        self.calls.append({
            "query": query,
            "max_results": max_results,
            "include_domains": include_domains
        })
        if self.should_raise:
            raise Exception("Simulated Tavily API Exception")

        if len(self.responses_list) >= len(self.calls):
            return self.responses_list[len(self.calls) - 1]

        return self.search_response

def test_build_research_query():
    query = build_research_query("https://www.example.com/test")
    assert "www.example.com" in query
    assert "Public product positioning" in query

def test_get_canonical_domain():
    assert get_canonical_domain("https://www.miro.com/pricing") == "miro.com"
    assert get_canonical_domain("https://miro.com") == "miro.com"
    assert get_canonical_domain("https://help.miro.com") == "help.miro.com"
    assert get_canonical_domain("http://WWW.MIRO.COM") == "miro.com"

def test_is_subdomain_of():
    assert is_subdomain_of("miro.com", "miro.com") is True
    assert is_subdomain_of("www.miro.com", "miro.com") is True
    assert is_subdomain_of("help.miro.com", "miro.com") is True
    assert is_subdomain_of("sub.help.miro.com", "miro.com") is True
    assert is_subdomain_of("unrelatedmiro.com", "miro.com") is False
    assert is_subdomain_of("miro.com.attacker.com", "miro.com") is False

def test_valid_mocked_response():
    mock_data = {
        "results": [
            {"title": "Nimble Pricing", "url": "https://nimble.com/pricing", "content": "Nimble pricing information."},
            {"title": "Nimble Features", "url": "https://nimble.com/features", "content": "Nimble features details."}
        ]
    }
    client = FakeTavilyClient(search_response=mock_data)
    sources = research_competitor("https://nimble.com", client=client)

    assert len(sources) == 2
    assert isinstance(sources[0], EvidenceSource)
    assert isinstance(sources[1], EvidenceSource)

    # Stable IDs SRC-1, SRC-2
    assert sources[0].source_id == "SRC-1"
    assert sources[1].source_id == "SRC-2"

    # Live sources have is_fictional=False
    assert sources[0].is_fictional is False
    assert sources[1].is_fictional is False

    assert sources[0].title == "Nimble Pricing"
    assert sources[0].url == "https://nimble.com/pricing"
    assert sources[0].excerpt == "Nimble pricing information."

def test_duplicate_urls_deduplicated():
    mock_data = {
        "results": [
            {"title": "Nimble Pricing 1", "url": "https://nimble.com/pricing", "content": "Pricing 1"},
            {"title": "Nimble Pricing 2", "url": "https://nimble.com/pricing", "content": "Pricing 2"},
            {"title": "Nimble Features", "url": "https://nimble.com/features", "content": "Features info"}
        ]
    }
    client = FakeTavilyClient(search_response=mock_data)
    sources = research_competitor("https://nimble.com", client=client)

    assert len(sources) == 2
    assert sources[0].source_id == "SRC-1"
    assert sources[0].url == "https://nimble.com/pricing"
    assert sources[0].title == "Nimble Pricing 1"
    assert sources[1].source_id == "SRC-2"
    assert sources[1].url == "https://nimble.com/features"

def test_empty_or_unusable_results_raise_error():
    client_empty = FakeTavilyClient(search_response={"results": []})
    with pytest.raises(ResearchError, match="Public research did not return enough relevant first-party competitor evidence"):
        research_competitor("https://nimble.com", client=client_empty)

    client_unusable = FakeTavilyClient(search_response={
        "results": [
            {"title": "Localhost URL", "url": "http://localhost", "content": "Not public"},
            {"title": "", "url": "https://nimble.com/pricing", "content": ""},
        ]
    })
    with pytest.raises(ResearchError, match="Public research did not return enough relevant first-party competitor evidence"):
        research_competitor("https://nimble.com", client=client_unusable)

def test_provider_exception_becomes_safe_error():
    client = FakeTavilyClient(should_raise=True)
    with pytest.raises(ResearchError) as exc_info:
        research_competitor("https://nimble.com", client=client)

    assert "Simulated Tavily API Exception" not in str(exc_info.value)
    assert "Public research could not be completed. Please try another public product URL." in str(exc_info.value)

def test_invalid_url_fails_before_search():
    client = FakeTavilyClient(search_response={"results": []})

    with pytest.raises(ValueError, match="empty"):
        research_competitor("   ", client=client)
    assert len(client.calls) == 0

    with pytest.raises(ValueError, match="Localhost is not allowed"):
        research_competitor("http://localhost/something", client=client)
    assert len(client.calls) == 0

    with pytest.raises(ValueError, match="Private IP addresses"):
        research_competitor("http://192.168.1.1", client=client)
    assert len(client.calls) == 0

def test_tavily_query_contents():
    client = FakeTavilyClient(search_response={
        "results": [
            {"title": "Title", "url": "https://nimble.com/features", "content": "content"},
            {"title": "Pricing", "url": "https://nimble.com/pricing", "content": "pricing info"}
        ]
    })
    research_competitor("https://nimble.com/subpath?arg=1", client=client)

    assert len(client.calls) == 1
    query = client.calls[0]["query"]
    assert "nimble.com" in query
    assert any(keyword in query.lower() for keyword in ["pricing", "features", "positioning", "updates", "proposition"])

def test_missing_api_key_raises_error():
    with pytest.raises(ResearchError, match="Tavily API key is required when no client is provided"):
        research_competitor("https://nimble.com", tavily_api_key=None, client=None)
    with pytest.raises(ResearchError, match="Tavily API key is required when no client is provided"):
        research_competitor("https://nimble.com", tavily_api_key="   ", client=None)

# New Test Cases for First-Party Evidence Relevance Gate & Fallback

def test_tavily_call_receives_include_domains():
    client = FakeTavilyClient(search_response={
        "results": [
            {"title": "Miro 1", "url": "https://miro.com/features", "content": "content 1"},
            {"title": "Miro 2", "url": "https://www.miro.com/pricing", "content": "content 2"}
        ]
    })
    research_competitor("https://www.miro.com/product", client=client)
    assert len(client.calls) == 1
    assert client.calls[0]["include_domains"] == ["miro.com"]

def test_valid_subdomains_retained():
    mock_data = {
        "results": [
            {"title": "Miro Main", "url": "https://miro.com/features", "content": "content"},
            {"title": "Miro Help", "url": "https://help.miro.com/pricing", "content": "content"},
            {"title": "Miro Blog", "url": "https://blog.miro.com/updates", "content": "content"},
            {"title": "Miro WWW", "url": "https://www.miro.com/about", "content": "content"}
        ]
    }
    client = FakeTavilyClient(search_response=mock_data)
    sources = research_competitor("https://miro.com", client=client)
    # All 4 sources should be retained since they are valid subdomains
    assert len(sources) == 4
    urls = [s.url for s in sources]
    assert "https://miro.com/features" in urls
    assert "https://help.miro.com/pricing" in urls
    assert "https://blog.miro.com/updates" in urls
    assert "https://www.miro.com/about" in urls

def test_third_party_domains_discarded():
    mock_data = {
        "results": [
            {"title": "Miro Main", "url": "https://miro.com/features", "content": "content"},
            {"title": "Unrelated competitor", "url": "https://mural.co/features", "content": "mural features Miro alternative"},
            {"title": "Miro Help", "url": "https://help.miro.com/pricing", "content": "content"},
            {"title": "Unrelated review site", "url": "https://g2.com/miro-reviews", "content": "miro reviews here"}
        ]
    }
    client = FakeTavilyClient(search_response=mock_data)
    sources = research_competitor("https://miro.com", client=client)
    # The 2 unrelated domains should be discarded even if they mention Miro in title/content
    assert len(sources) == 2
    urls = [s.url for s in sources]
    assert "https://miro.com/features" in urls
    assert "https://help.miro.com/pricing" in urls
    assert "https://mural.co/features" not in urls
    assert "https://g2.com/miro-reviews" not in urls

def test_source_ids_sequential_after_filtering():
    mock_data = {
        "results": [
            {"title": "Miro Main", "url": "https://miro.com/features", "content": "content"},
            {"title": "Unrelated", "url": "https://g2.com/miro", "content": "unrelated content"},
            {"title": "Miro Help", "url": "https://help.miro.com/pricing", "content": "content"}
        ]
    }
    client = FakeTavilyClient(search_response=mock_data)
    sources = research_competitor("https://miro.com", client=client)
    assert len(sources) == 2
    assert sources[0].source_id == "SRC-1"
    assert sources[0].url == "https://miro.com/features"
    assert sources[1].source_id == "SRC-2"
    assert sources[1].url == "https://help.miro.com/pricing"

def test_fewer_than_two_sources_raises_error():
    # Only 1 valid source returned after filtering out unrelated domains
    mock_data = {
        "results": [
            {"title": "Miro Main", "url": "https://miro.com/features", "content": "content"},
            {"title": "Unrelated", "url": "https://g2.com/miro", "content": "unrelated content"}
        ]
    }
    client = FakeTavilyClient(search_response=mock_data)
    with pytest.raises(ResearchError, match="Public research did not return enough relevant first-party competitor evidence"):
        research_competitor("https://miro.com", client=client)

# Multi-Query Fallback tests

def test_no_fallback_when_first_query_sufficient():
    mock_data = {
        "results": [
            {"title": "Miro 1", "url": "https://miro.com/features", "content": "content 1"},
            {"title": "Miro 2", "url": "https://www.miro.com/pricing", "content": "content 2"}
        ]
    }
    client = FakeTavilyClient(search_response=mock_data)
    sources = research_competitor("https://miro.com", client=client)
    assert len(client.calls) == 1
    assert len(sources) == 2

def test_fallback_executed_sequentially():
    res1 = {"results": [{"title": "Miro 1", "url": "https://miro.com/1", "content": "c1"}]}
    res2 = {"results": [{"title": "Miro 2", "url": "https://miro.com/2", "content": "c2"}]}
    client = FakeTavilyClient(responses_list=[res1, res2])
    sources = research_competitor("https://miro.com", client=client)
    assert len(client.calls) == 2
    assert len(sources) == 2
    assert sources[0].source_id == "SRC-1"
    assert sources[1].source_id == "SRC-2"
    assert sources[0].url == "https://miro.com/1"
    assert sources[1].url == "https://miro.com/2"
    assert "miro.com" in client.calls[0]["query"]
    assert "site:miro.com" in client.calls[1]["query"]
    assert "product features pricing" in client.calls[1]["query"]

def test_fallback_discards_third_party():
    res1 = {"results": [{"title": "Miro 1", "url": "https://miro.com/1", "content": "c1"}]}
    res2 = {"results": [
        {"title": "Miro 2", "url": "https://miro.com/2", "content": "c2"},
        {"title": "G2", "url": "https://g2.com/miro", "content": "c3"}
    ]}
    client = FakeTavilyClient(responses_list=[res1, res2])
    sources = research_competitor("https://miro.com", client=client)
    assert len(client.calls) == 2
    assert len(sources) == 2
    assert sources[0].url == "https://miro.com/1"
    assert sources[1].url == "https://miro.com/2"
    assert all("g2.com" not in s.url for s in sources)

def test_fallback_fails_safely_when_insufficient():
    res1 = {"results": [{"title": "Miro 1", "url": "https://miro.com/1", "content": "c1"}]}
    res2 = {"results": []}
    res3 = {"results": []}
    client = FakeTavilyClient(responses_list=[res1, res2, res3])
    with pytest.raises(ResearchError, match="Public research did not return enough relevant first-party competitor evidence"):
        research_competitor("https://miro.com", client=client)
    assert len(client.calls) == 3
    assert "site:miro.com" in client.calls[2]["query"]
    assert "help docs release notes" in client.calls[2]["query"]

def test_all_calls_use_include_domains():
    res1 = {"results": []}
    res2 = {"results": []}
    res3 = {"results": []}
    client = FakeTavilyClient(responses_list=[res1, res2, res3])
    with pytest.raises(ResearchError):
        research_competitor("https://help.miro.com", client=client)
    assert len(client.calls) == 3
    for call in client.calls:
        assert call["include_domains"] == ["help.miro.com"]
