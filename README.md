\# SentiGuard



Real-time evidence-grounded product sentiment intelligence backend.



## Quick Start

1. Clone the repository:
   `git clone https://github.com/mithuhacktive/Sentiment-Analysis-System.git`

2. Enter the project:
   `cd Sentiment-Analysis-System`

3. Create virtual environment:
   `python -m venv .venv`

4. Activate virtual environment:
   `.\.venv\Scripts\Activate.ps1`

5. Install backend dependencies:
   `pip install -e ".[dev]"`

6. Start backend:
   `$env:SENTIGUARD_OFFLINE="false"`
   `uvicorn app.main:app --reload`

7. Open a new terminal and enter frontend:
   `cd frontend`

8. Install frontend dependencies:
   `npm install`

9. Start frontend:
   `npm run dev`

10. Open the application:
    `http://localhost:5173`

Backend:
`http://127.0.0.1:8000`

Health check:
`http://localhost:8000/api/v1/health`

Run tests:
`pytest`


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

