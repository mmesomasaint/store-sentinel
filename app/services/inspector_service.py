# app/services/inspector_service.py
import httpx
import time
from typing import List, Dict, Any
from app.config import settings
from app.services.crawler_service import crawler_service

class InspectorService:
    def __init__(self):
        self.headers = {
            "User-Agent": "StoreSentinel-Inspector/1.0 (+https://optima.studio)"
        }

    async def inspect_storefront(self, store_url: str) -> Dict[str, Any]:
        """
        Executes root domain check, extracts page links, and scans for 404/500 broken links.
        """
        result = {
            "is_up": False,
            "status_code": 0,
            "response_time_ms": 0.0,
            "total_links_scanned": 0,
            "broken_links": []
        }

        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_SECONDS, follow_redirects=True) as client:
            # 1. Root Store Inspection
            start_time = time.perf_counter()
            try:
                response = await client.get(store_url, headers=self.headers)
                latency = (time.perf_counter() - start_time) * 1000
                result["status_code"] = response.status_code
                result["response_time_ms"] = round(latency, 2)
                result["is_up"] = response.status_code < 400
            except Exception as e:
                result["is_up"] = False
                result["status_code"] = 503
                return result

            if not result["is_up"]:
                return result

            # 2. Extract Links from Homepage
            links_to_check = crawler_service.extract_internal_links(store_url, response.text)
            result["total_links_scanned"] = len(links_to_check)

            # 3. Batch Check Links for Errors
            broken_details = []
            for link in list(links_to_check)[:25]: # Bounded scan size per run
                try:
                    res = await client.head(link, headers=self.headers)
                    if res.status_code >= 400:
                        broken_details.append({
                            "url": link,
                            "status_code": res.status_code,
                            "source_page": store_url
                        })
                except Exception:
                    broken_details.append({
                        "url": link,
                        "status_code": 504,
                        "source_page": store_url
                    })

            result["broken_links"] = broken_details

        return result

inspector_service = InspectorService()
