import pytest
from utils import validate_public_url

def test_valid_public_url():
    assert validate_public_url("https://www.google.com") == "https://www.google.com"
    assert validate_public_url("http://example.org/path?q=1") == "http://example.org/path?q=1"

def test_empty_url():
    with pytest.raises(ValueError, match="empty"):
        validate_public_url("")
    with pytest.raises(ValueError, match="empty"):
        validate_public_url("   ")

def test_invalid_scheme():
    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        validate_public_url("ftp://example.com")
    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        validate_public_url("file:///etc/passwd")

def test_localhost():
    with pytest.raises(ValueError, match="Localhost is not allowed"):
        validate_public_url("http://localhost:8080")

def test_loopback_ips():
    with pytest.raises(ValueError, match="Loopback"):
        validate_public_url("http://127.0.0.1")
    with pytest.raises(ValueError, match="Loopback"):
        validate_public_url("http://[::1]")

def test_private_ips():
    with pytest.raises(ValueError, match="Private"):
        validate_public_url("https://192.168.1.100")
    with pytest.raises(ValueError, match="Private"):
        validate_public_url("http://10.0.0.1")
