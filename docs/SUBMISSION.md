# Submission — FlytBase Inbound BDR Assistant

## 1. Project Overview

An AI-agent system that takes a single inbound contact-form email and performs
the full first-touch workload of a human Inbound BDR: parsing, MEDDPICC
qualification, live company research, buying-signal detection, case-study
matching, GTM routing, outreach drafting, and AE handoff — delivered as a
Next.js dashboard backed by a FastAPI multi-agent pipeline.

## 2. Business Problem

FlytBase's inbound funnel loses time and consistency at the first-touch stage:
a BDR must read every inbound email, manually research the company, apply a
qualification framework, decide which case study and GTM motion fits, and
write personalized outreach — all before the SLA clock on "time to first
response" runs out. Quality varies by BDR experience, and thorough company
research is often skipped under volume. The result is slower response times
and inconsistent qualification quality on deals that are handed to AEs.

## 3. Solution

An 8-agent pipeline, each agent a single-responsibility module with its own
prompt and strict output schema, orchestrated by one thin coordination layer.
The dashboard surfaces every agent's output as its own card so a human BDR/AE
can verify, edit, or override any stage rather than trusting a black box.

Design principles applied throughout:
- **Modularity over a mega-prompt.** The brief explicitly warns against
  building everything in one prompt. Every agent here only sees the inputs it
  needs (e.g. the Outreach Agent never sees raw buying-signal data it doesn't
  use) — this keeps prompts small, cheap, and independently testable.
- **Grounded, not hallucinated.** The Company Research Agent is retrieval-
  augmented: it's given real web search snippets (via Tavily) and explicitly
  instructed to cap its confidence score and flag missing data rather than
  invent funding numbers or employee counts. The Case Study Matching Agent is
  given FlytBase's actual case-study library in-context and can only select
  from it — it cannot invent a case study that doesn't exist.
- **Honest uncertainty.** The Lead Qualification Agent explicitly lists
  `missing_information` per MEDDPICC dimension rather than guessing — this is
  what actually makes AI qualification useful to a human seller, since a real
  discovery call needs to know what's unknown.

## 4. Architecture

See `docs/diagrams/architecture.mmd` for the full component diagram and
`docs/mindmap.html` for an interactive explorer. Summary:

```
Next.js (Vercel) --REST--> FastAPI (Render) --> Orchestrator --> 8 Agents --> LLM Service --> OpenAI/Gemini
                                                                            └-> Search Service --> Tavily
```

## 5. AI Agent Workflow

1. **Email Parser Agent** — structured extraction (company, contact, intent, urgency, pain points).
2. **Lead Qualification Agent** — MEDDPICC breakdown + 0-100 lead score + missing info.
3. **Company Research Agent** — live web search synthesis into a structured company profile.
4. **Buying Signal Agent** — 7-category signal detection (expansion, hiring, funding, digital
   transformation, drone adoption, enterprise readiness, buying intent), each with an explanation.
5. **Case Study Matching Agent** — retrieval-augmented top-3 match against FlytBase's case study
   library with similarity scores and reasoning.
6. **GTM Recommendation Agent** — routes to Direct AE / Enterprise Team / Partner-led / Channel
   Partner with explicit reasoning.
7. **Outreach Agent** — personalized email, LinkedIn message, call opening, 5 discovery questions,
   2 follow-ups — every message required to reference a specific fact from the lead, not filler.
8. **AE Handoff Agent** — the only agent that reads all upstream outputs; produces a dense,
   CRM-ready note (research summary, pain points, signals, demo focus, next action).

Full pipeline order and per-agent contracts: `backend/app/orchestrator.py` and
`backend/app/models/schemas.py`.

## 6. Technology Stack

| Layer      | Choice                                                        |
|------------|-----------------------------------------------------------------|
| Frontend   | Next.js 14 (App Router), TypeScript, TailwindCSS, lucide-react |
| Backend    | FastAPI, Python 3.11+, Pydantic v2                              |
| LLM        | OpenAI (`gpt-4o-mini` default) or Gemini — swappable via env var |
| Research   | Tavily search API (LLM-agent-oriented web search)               |
| Deployment | Frontend → Vercel, Backend → Render                              |

## 7. System Flow

Inbound email → Parser → {Qualification, Research (parallel in principle)} →
Buying Signals (needs Research) → Case Study (needs Research) → GTM (needs
Qualification + Research + Signals) → Outreach (needs Case Study) → AE
Handoff (needs everything). See `docs/diagrams/sequence.mmd` for the full
call sequence including LLM and search-API round trips.

**Error handling:** every agent call is wrapped by `BaseAgent.run()`, which
raises a typed `AgentError` on LLM failure or schema-validation failure after
retries — the orchestrator does not silently continue the pipeline on
partial/invalid data. The FastAPI layer converts `AgentError` to a clean
`502` with the underlying reason instead of a raw stack trace.

**Retry strategy:** `llm_service.generate_json()` retries up to
`MAX_RETRIES` (default 3) with linear backoff; a JSON-parse failure appends a
stricter "JSON only" instruction on retry rather than just repeating the same
prompt.

**Caching:** an in-memory TTL cache (`TTLCache`, default 1hr) keyed on a hash
of `(model, system_prompt, user_prompt)` avoids re-billing identical calls —
useful both for the granular per-agent endpoints (which re-parse the same
email) and for repeated dashboard refreshes during a demo.

**Rate limiting:** a sliding-window `RateLimiter` throttles outbound LLM
calls to `RATE_LIMIT_PER_MINUTE` (default 20) to protect the OpenAI/Gemini
quota from a runaway loop.

**Logging:** structured request logging middleware in `main.py` logs every
HTTP call with method, path, status, and duration; each agent logs its stage
in the orchestrator for pipeline-level tracing.

## 8. Evidence from Codebase

- Agent modularity: `backend/app/agents/*.py` — 8 files, each <100 lines, single system prompt, single schema.
- Grounded research: `backend/app/services/search_service.py::research_company()` called from
  `company_research_agent.py::_build_user_prompt()` before any LLM call.
- Retrieval-constrained case studies: `case_study_agent.py` passes the full
  `CASE_STUDIES` list from `backend/app/data/case_studies.py` into the prompt and
  instructs the model to select "ONLY from this list."
- Reliability layer: `backend/app/services/llm_service.py` (`RateLimiter`, `TTLCache`, retry loop).
- Typed contracts: `backend/app/models/schemas.py` mirrored exactly in `frontend/types/index.ts`.
- The frontend was verified to type-check and build successfully with `next build` before submission
  (zero TypeScript errors across all 8 dashboard components).

## 9. Results

Given the sample "European BVLOS drone inspection company" inbound email, the
pipeline produces: a fully-populated MEDDPICC breakdown with an appropriately
*moderate* lead score (single inbound email — most MEDDPICC dimensions are
correctly flagged as unknown), a company research profile, a buying-signal
set correctly flagging `drone_adoption` and `buying_intent` as strong, a top
case-study match against the "Drone Inspection SaaS Platform Fleet
Orchestration" case study (closest match: European drone-software company,
BVLOS use case), a `partner_led` or `direct_ae` GTM call depending on framing,
and full outreach copy referencing the matched case study by name.

## 10. Approach

Built backend-first: schemas → base agent → 8 agents → orchestrator → routes,
validating each layer (syntax + route registration) before moving to the
frontend, then building the frontend against the exact typed contract the
backend already exposed — this is why the TS types in `frontend/types/index.ts`
are a direct mirror of `backend/app/models/schemas.py` rather than a
best-guess shape.

## 11. Challenges

- **Balancing agent independence vs. shared context.** Several agents (GTM,
  Outreach, AE Handoff) genuinely need multiple upstream outputs. The
  resolution was to let the *orchestrator* own the fan-in, not the agents
  themselves — each agent's `_build_user_prompt()` still only accepts the
  specific typed objects it needs, so it stays testable in isolation.
- **Grounding research without a live key at build/eval time.** Solved by
  making `search_service.py` degrade explicitly and visibly (capped confidence
  score, explicit "no live data" note) rather than letting the LLM quietly
  fill the gap with plausible-sounding invented facts.
- **Keeping the granular per-endpoint API stateless** without a database,
  while still exposing every agent as its own REST endpoint — solved via the
  LLM response cache, so re-running the Parser inside `/qualify`, `/research`,
  etc. is a cache hit, not a re-billed call.

## 12. Trade-offs

- In-memory cache/rate-limiter instead of Redis — correct for a hackathon
  demo and single-instance deploy; would need to move to Redis for a
  multi-instance production deployment (noted in Future Improvements).
- No persistent database/CRM integration — the AE Handoff Agent produces a
  CRM-ready *note*, but actually writing to a CRM (Salesforce/HubSpot) was
  scoped out to keep the core agent reasoning the focus of the submission.
- Case study library is a static, hand-curated file rather than a live
  scrape/vector index of flytbase.com/case-studies — chosen deliberately so
  the matching agent's recommendations are 100% verifiable against a fixed,
  inspectable source rather than a black-box retrieval index.

## 13. Future Improvements

- Swap the static case-study file for a vector-indexed version of FlytBase's
  real case study library (scraped + embedded), so new case studies don't
  require a code change.
- Add a lightweight persistence layer (Postgres) to power true search history,
  a leads table, and direct CRM handoff (Salesforce/HubSpot API) instead of a
  copy/export text block.
- Parallelize independent agent calls (Qualification and Research have no
  dependency on each other) using `asyncio.gather` to cut end-to-end latency.
- Add automated evals: a small labeled set of sample inbound emails with
  expected MEDDPICC/GTM outputs, run in CI against the live prompts to catch
  prompt-regression before merge.
- Move the in-memory cache/rate-limiter to Redis for multi-instance deploys.
