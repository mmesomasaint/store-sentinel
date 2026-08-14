# tests/test_crawler.py
from app.services.crawler_service import crawler_service
from app.core.security import validate_url_against_ssrf

def test_link_extraction():
    html = """
    <html>
        <body>
            <a href="/products/silk-dress">Silk Dress</a>
            <a href="https://otherdomain.com/ad">External Ad</a>
        </body>
    </html>
    """
    links = crawler_service.extract_internal_links("https://myfashionstore.com", html)
    assert "https://myfashionstore.com/products/silk-dress" in links
    assert "https://otherdomain.com/ad" not in links

def test_ssrf_protection():
    assert validate_url_against_ssrf("http://127.0.0.1") is False
    assert validate_url_against_ssrf("http://169.254.169.254") is False
    assert validate_url_against_ssrf("https://myfashionstore.com") is True
