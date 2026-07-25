# FlytBase Inbound BDR Assistant

An AI-agent pipeline that automates the work of a human Inbound BDR: parse an inbound
contact-form email, qualify the lead (MEDDPICC), research the company from live web
data, detect buying signals, match the best FlytBase case study, recommend a GTM
motion, generate outreach copy, and produce an AE handoff summary — end to end.

Built for the **FlytBase Inbound BDR Hiring Hackathon**.

> See `docs/SUBMISSION.md` for the full writeup (architecture, reasoning, trade-offs)
> and `docs/WALKTHROUGH_SCRIPT.md` for the 5-minute demo script.

---

## 1. Architecture at a glance

```
Inbound Email
   │
   ▼
[1] Email Parser Agent           → structured company/contact/intent JSON
   │
   ▼
[2] Lead Qualification Agent     → MEDDPICC + lead score
   │
   ▼
[3] Company Research Agent       → live web research (Tavily) + synthesis
   │
   ▼
[4] Buying Signal Agent          → 7-category signal detection
   │
   ▼
[5] Case Study Matching Agent    → top-3 FlytBase case studies + reasoning
   │
   ▼
[6] GTM Recommendation Agent     → Direct AE / Partner-led / Enterprise / Channel
   │
   ▼
[7] Outreach Agent               → email, LinkedIn, call opening, follow-ups
   │
   ▼
[8] AE Handoff Agent             → CRM-ready summary
```

Each agent is a standalone Python class (`backend/app/agents/*.py`) with its own
system prompt and a strict Pydantic output schema. The `orchestrator.py` module is
the *only* place that knows the pipeline order — agents never call each other
directly. This is what makes the system modular: you can reorder, replace, or
A/B test a single agent without touching the rest.

Full system design write-up (data flow, error handling, retries, caching, rate
limiting, logging) is in `docs/SUBMISSION.md`.

---

## 2. Folder structure

```
flytbase-bdr-assistant/
├── backend/
│   ├── main.py                     # FastAPI entrypoint
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
│       ├── config.py                # typed settings from env
│       ├── agents/                  # 8 modular AI agents
│       │   ├── base_agent.py
│       │   ├── email_parser_agent.py
│       │   ├── lead_qualification_agent.py
│       │   ├── company_research_agent.py
│       │   ├── buying_signal_agent.py
│       │   ├── case_study_agent.py
│       │   ├── gtm_agent.py
│       │   ├── outreach_agent.py
│       │   └── ae_handoff_agent.py
│       ├── services/
│       │   ├── llm_service.py       # provider-agnostic LLM call layer (retry/cache/rate-limit)
│       │   └── search_service.py    # live web research (Tavily)
│       ├── models/schemas.py        # Pydantic contracts between agents
│       ├── data/case_studies.py     # FlytBase case study library
│       ├── api/routes.py            # REST endpoints
│       └── orchestrator.py          # pipeline wiring
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx                 # landing page
│   │   ├── dashboard/page.tsx       # main dashboard
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── components/                  # one component per dashboard card
│   ├── lib/api.ts                   # typed API client
│   ├── types/index.ts               # TS mirror of backend schemas
│   └── package.json
│
└── docs/
    ├── README.md (this file's counterpart, if split)
    ├── SUBMISSION.md
    ├── WALKTHROUGH_SCRIPT.md
    ├── mindmap.html                 # standalone interactive mind map
    └── diagrams/                    # Mermaid: flowchart, sequence, mindmap, architecture
```

---

## 3. Running locally

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set OPENAI_API_KEY (or GEMINI_API_KEY + LLM_PROVIDER=gemini)
# Optional but recommended: set TAVILY_API_KEY for live company research
uvicorn main:app --reload --port 8000
```

Backend now runs at `http://localhost:8000`. Interactive API docs at `/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
npm run dev
```

Frontend runs at `http://localhost:3000`. Open `/dashboard`, paste an inbound email
(or click a sample), and click **Analyze Inbound Lead**.

---

## 4. API reference

| Endpoint             | Method | Description                                             |
|-----------------------|--------|-----------------------------------------------------------|
| `/api/analyze-email`  | POST   | Full 8-agent pipeline. Primary endpoint used by the dashboard. |
| `/api/qualify`        | POST   | Parser → Qualification only.                              |
| `/api/research`       | POST   | Parser → Company Research only.                           |
| `/api/case-study`     | POST   | Parser → Research → Case Study Matching.                  |
| `/api/recommend`      | POST   | Parser → Research → Qualification → Signals → GTM.        |
| `/api/generate-email` | POST   | Parser → Research → Qualification → Case Study → Outreach.|
| `/api/handoff`        | POST   | Full pipeline, returns only the AE handoff summary.        |
| `/api/health`         | GET    | Health check.                                              |

All POST endpoints accept `{ "email_text": "..." }`.

---

## 5. Deployment

### Frontend → Vercel
1. Push this repo to GitHub.
2. Import the `frontend/` directory as a new Vercel project (set root directory to `frontend`).
3. Add environment variable `NEXT_PUBLIC_API_BASE_URL` pointing at your deployed backend.
4. Deploy.

### Backend → Render
1. New **Web Service** on Render, root directory `backend`.
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env.example` (`OPENAI_API_KEY`, `TAVILY_API_KEY`, `CORS_ORIGINS` set to your Vercel URL, etc.).
5. Deploy, then update the frontend's `NEXT_PUBLIC_API_BASE_URL` to the Render URL.

---

## 6. Environment variables

See `backend/.env.example` for the full list — LLM provider selection, API keys,
CORS origins, cache TTL, rate limit, and retry configuration are all environment-driven
so behavior can be tuned per-environment without code changes.

---

## License

MIT — see `LICENSE`.
