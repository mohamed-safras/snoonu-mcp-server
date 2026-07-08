# Snoonu MCP Server

> Independent demo project — not affiliated with or endorsed by Snoonu.

## Architecture

```
                        AI Agent / Claude / Cursor
                                   │
                    MCP over Streamable HTTP  (/mcp)
                                   │
                    ┌──────────────▼──────────────┐
                    │         Cloud Run            │
                    │              │
                    │                              │
                    │  ┌────────────────────────┐  │
                    │  │      MCP Server         │  │
                    │  │  FastMCP · Python       │  │
                    │  │  Gunicorn · port 8080   │  │
                    │  │                         │  │
                    │  │  tools/                 │  │
                    │  │  ├─ products            │  │
                    │  │  ├─ categories          │  │
                    │  │  ├─ delivery            │  │
                    │  │  └─ orders              │  │
                    │  └────┬──────────┬─────────┘  │
                    │       │          │             │
                    │  ┌────▼───┐  ┌──▼──────┐      │
                    │  │Postgres│  │  Redis  │      │
                    │  │sidecar │  │ sidecar │      │
                    │  │  :5432 │  │  :6379  │      │
                    │  │450+    │  │ cache + │      │
                    │  │products│  │rate-lim │      │
                    │  └────────┘  └─────────┘      │
                    └──────────────────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │    GitHub Actions (CI/CD)    │
                    │  push → main → build → deploy│
                    │  auth via Workload Identity  │
                    │  Federation (no SA keys)     │
                    └──────────────────────────────┘
```

### Request flow

```
Agent calls tool
    → FastMCP routes to tools/products.py (or orders, delivery, …)
    → Repository queries Postgres (SQLAlchemy, connection pool)
    → Redis consulted first for cached responses (TTL 300 s)
    → JSON result returned to agent
```

### Key decisions

| Decision                                                       | Reason                                                                                              |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Postgres + Redis as **sidecars** (not Cloud SQL / Memorystore) | Zero extra GCP cost — stays inside Cloud Run's always-free tier                                     |
| **maxScale: 1**                                                | >1 instances = each gets its own isolated Postgres/Redis, breaking consistency and the rate limiter |
| **Non-persistent Postgres**                                    | Cold start re-seeds from baked-in SQL dump — acceptable for a demo catalog                          |
| `stateless_http=True`                                          | Multiple Gunicorn workers can serve any request; avoids MCP session pinning across workers          |
| **Workload Identity Federation**                               | No long-lived service account keys stored in GitHub secrets                                         |

### Layers

```
src/
├── server.py              FastMCP app — registers tools, mounts health/ready/metrics
├── tools/                 MCP tool definitions — depend only on api.client
├── api/
│   ├── base.py            Port interfaces the tools depend on
│   └── database/          Postgres adapter (repositories + SQLAlchemy models)
├── cache.py               Redis TTL cache decorator
├── order_rate_limit.py    Redis-backed per-session order rate limiter
├── metrics.py             Prometheus counters, per-tool instrumentation
└── middleware.py          Structured JSON request logging

deploy/gcloud/
├── service.yaml.tpl       Cloud Run multi-container spec (MCP + Postgres + Redis)
├── deploy.sh              One-command setup / build / deploy
└── db/
    ├── 01-schema.sql      Schema — products, categories, orders, cities
    └── 02-seed-data.sql   450+ real Qatar/GCC products (Baladna, Almarai, Rayyan …)
```
