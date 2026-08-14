# Store Sentinel - E-Commerce Broken Link & Website Uptime Inspector

An automated background inspection platform built with **FastAPI**, **APScheduler**, **BeautifulSoup4**, and **HTTPX**. Store Sentinel periodically crawls e-commerce storefronts, tests collection/PDP hyperlinks for 404/500 errors, measures response latency, and sends real-time email alerts to store managers before broken links disrupt revenue.

## Key Features
- **Automated Cron Crawling:** Powered by APScheduler to monitor storefront targets at set intervals.
- **Anti-SSRF Protection:** Resolves and validates target IPs against private and loopback subnets.
- **DOM Hyperlink Parsing:** Uses BeautifulSoup4 to extract same-domain product and collection links.
- **Failure Alerts:** Sends HTML email reports detailing degraded uptime or specific broken URLs.

---

## Local Setup

1. **Initialize Virtual Environment & Dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Configure Environment:**
   ```bash
   cp .env.example .env
   ```
3. **Start Mock Services & Application:**
   - Terminal 1 (Mock SMTP):
     ```bash
     python3 -m aiosmtpd -n -l localhost:1025
     ```
   - Terminal 2 (FastAPI App):
     ```bash
     uvicorn app.main:app --reload --port 8000
     ```

## Interactive Testing

1. Navigate to `http://localhost:8000/docs`.
2. Authenticate using `X-API-Key: dev_secret_api_key_12345`.
3. Register a store using `POST /api/v1/stores`:
   ```JSON
   {
      "name": "Luxury Fashion Hub",
      "url": "[https://example.com](https://example.com)",
      "manager_email": "manager@example.com"
    }
   ```
4. Trigger an instant inspection via `POST /api/v1/stores/{store_id}/inspect`.


## Run Pytest Suite

```bash
pytest -v
```
