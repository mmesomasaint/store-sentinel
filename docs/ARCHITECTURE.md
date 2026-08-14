# SYSTEM ARCHITECTURE & SECURITY SPECIFICATION

```Plaintext
[ Store Sentinel Scheduler ]
                        (APScheduler Cron every N mins)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          Inspector Pipeline                             │
│                                                                         │
│  1. SSRF Protection: Validate Target IP against Local/Private Subnets   │
│  2. Head Ping: Validate root domain status code & latency threshold     │
│  3. HTML Crawler: Extract collection links, product PDPs, & cart buttons│
│  4. Async Concurrent Validator: Check batch links with HTTPX Pool       │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
   ┌─────────────────────────────┐     ┌─────────────────────────────┐
   │    PostgreSQL Audit Log     │     │    Alert Dispatcher Engine  │
   │  - Store Uptime Record      │     │  - Immediate Email Report   │
   │  - Broken Link Mapping      │     │  - Webhook Notification     │
   │  - Response Latency Graph   │     └─────────────────────────────┘
   └─────────────────────────────┘
```

## Threat Model & Defense-in-Depth Architecture
1. **Anti-SSRF (Server-Side Request Forgery) Guard:** To prevent attackers from registering internal network addresses (e.g., `[http://127.0.0.1](http://127.0.0.1), [http://169.254.169.254](http://169.254.169.254)`), all target domain hostnames are resolved to IP addresses prior to execution and checked against `ipaddress.is_private / ipaddress.is_loopback` blocks.
2. **Controlled User-Agent & Rate Limiting:** Crawling external merchant sites can inadvertently look like a `DDoS` attack. Requests are dispatched with an configurable rate limiter (`max 10 concurrent HTTP requests per domain`) and identify the agent cleanly via a custom `User-Agent` string.
3. **Loop Prevention & Depth Bounding:** Crawling is strictly bounded to a maximum recursion depth (`default: 2`) and same-domain links only, preventing infinite loops on bad redirects or dynamic infinite-scroll collection pages.
