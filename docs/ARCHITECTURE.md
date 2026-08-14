SYSTEM ARCHITECTURE & SECURITY SPECIFICATION

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
