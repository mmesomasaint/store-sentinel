STORE-SENTINEL REPOSITORY DIRECTORY STRUCTURE

store-sentinel/
├── app/
│   ├── __init__.py
│   ├── main.py                   # App lifecycle, scheduler startup, and health metrics
│   ├── config.py                 # Strict Pydantic Settings & threshold limits
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py         # V1 API router aggregation
│   │       └── endpoints.py      # Manual check triggers, site CRUD, & report routes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py       # Async SQLAlchemy engine for store audit logs
│   │   ├── scheduler.py      # Background worker queue & cron execution engine
│   │   └── security.py       # API Key authentication & URL SSRF/Domain verification
│   ├── models/
│   │   ├── __init__.py
│   │   └── store.py              # SQLAlchemy models for Stores, Audits, & Broken Links
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── store.py              # Pydantic schemas for targets, metrics, & reports
│   ├── services/
│   │   ├── __init__.py
│   │   ├── crawler_service.py    # Recursive HTML/DOM parser & link extraction engine
│   │   ├── inspector_service.py  # Async HTTP status code & SSL certificate validator
│   │   └── alert_service.py      # Multi-channel notification dispatcher (Email/Webhook)
│   └── templates/
│       └── downtime_report.html  # High-priority alert email for store managers
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Async Pytest fixtures, mock HTTPX responses, & test DB
│   ├── test_crawler.py           # DOM parsing & SSRF validation unit tests
│   └── test_api.py               # Inspection API & scheduler integration tests
├── devops/
│   ├── docker-compose.yml        # Container stack (API, PostgreSQL, Redis, Mailpit)
│   ├── Dockerfile                # Multi-stage production container build
│   └── nginx.conf                # Reverse proxy with TLS & security headers
├── docs/
│   └── ARCHITECTURE.md           # System architecture, crawler strategy, & threat model
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md                     # Technical handover & setup documentation
└── requirements.txt              # Locked dependencies
