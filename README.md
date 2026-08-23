\# SentiGuard



Real-time evidence-grounded product sentiment intelligence backend.



\## Quick Start



```bash

\# 1. Install

pip install -e ".\[dev]"



\# 2. Configure

cp .env.example .env



\# 3. Run (offline mode — no APIs needed)

SENTIGUARD\_OFFLINE=true uvicorn app.main:app --reload



\# 4. Test

curl http://localhost:8000/api/v1/health



curl -X POST http://localhost:8000/api/v1/analyze \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"query": "Sony WH-1000XM5"}'

```



\## Docker



```bash

docker compose up --build

```



\## Tests



```bash

pytest

pytest --cov=app

```



\## Scripts



```bash

python scripts/smoke\_test.py

python scripts/benchmark.py

python scripts/evaluate.py

```



\## Architecture



```

Input → Product Resolver → Adapters (Fixture/URL/Reddit/SerpAPI)

&#x20;    → Normalisation → Language Detection → Deduplication

&#x20;    → Quality Scoring → Sentiment (RoBERTa) → Aspect Analysis

&#x20;    → Evidence Scoring → Weighted Aggregation → Calibration

&#x20;    → Abstention Decision → JSON Response

```



\## Confidence Levels



| Level | Threshold |

|-------|-----------|

| HIGH | ≥ 0.80 |

| MODERATE | 0.55 – 0.79 |

| LOW | < 0.55 |

| INSUFFICIENT\_EVIDENCE | Abstain |

