# app/services/crawler_service.py
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set, Dict, List
from app.config import settings

class CrawlerService:
    @staticmethod
    def extract_internal_links(base_url: str, html_content: str) -> Set[str]:
        """Parses DOM and extracts unique same-domain hyperlinks."""
        soup = BeautifulSoup(html_content, "html.parser")
        base_domain = urlparse(base_url).netloc
        extracted_links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            # Ignore JavaScript anchors or mailto links
            if href.startswith(("javascript:", "mailto:", "tel:", "#")):
                continue
                
            full_url = urljoin(base_url, href)
            parsed_href = urlparse(full_url)

            # Restrict crawling to same domain and HTTP(S) protocol
            if parsed_href.netloc == base_domain and parsed_href.scheme in ("http", "https"):
                extracted_links.add(full_url)

        return extracted_links

crawler_service = CrawlerService()
