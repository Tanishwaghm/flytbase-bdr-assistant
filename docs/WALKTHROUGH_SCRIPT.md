# Demo Walkthrough Script (5 minutes)

*Target runtime: ~5 minutes. Timestamps are guides, not hard cuts.*

---

### 0:00 – 0:40 | The Problem

"Every inbound lead that hits FlytBase's contact form today needs a human BDR
to do five things before they can even reply: read the email, research the
company, qualify it against a framework like MEDDPICC, decide who should own
it — a direct AE, an enterprise team, or a partner — and then write
personalized outreach. That's 20-30 minutes of manual work per lead, and
quality depends entirely on which BDR picks it up.

I built an AI agent pipeline that does all of that in under a minute, and
surfaces every step so a human still reviews and owns the final call."

---

### 0:40 – 1:30 | Architecture (30-45 sec)

*[Show `docs/diagrams/architecture.mmd` rendered, or the interactive `docs/mindmap.html`]*

"It's 8 independent AI agents, not one giant prompt — that was a deliberate
constraint. Each agent has one job and a strict typed output: a Parser, a
MEDDPICC Qualifier, a Company Researcher that's grounded in live web search
— not hallucinated — a Buying Signal detector, a Case Study matcher that can
only pick from FlytBase's real case study library, a GTM router, an Outreach
generator, and an AE Handoff summarizer that's the only agent that sees
everything upstream.

One orchestrator wires them together — the agents themselves don't know
about each other, which means I can swap or re-test any single one without
touching the rest."

---

### 1:30 – 3:30 | Live Demo (2 min)

*[Switch to the running dashboard at `/dashboard`]*

"Let's paste in a realistic inbound email." *[Click the "European BVLOS Drone
Inspection Co." sample, click Analyze]*

"While that runs — under the hood this is hitting `/api/analyze-email`, which
chains all 8 agents server-side." *[Point out loading skeletons]*

*[Results land]*

"First, the Qualification card — full MEDDPICC breakdown, an honest lead
score, and critically, it tells the AE exactly what's still unknown and needs
to be asked on the discovery call, instead of pretending to know things a
single email can't tell you.

Next, Company Research — this isn't the LLM guessing, it's grounded in real
web search results, with a visible confidence score that drops if live data
wasn't available.

Buying Signals — seven categories, each with a strength rating and a
one-line explanation tied back to actual evidence in the email or research.

Case Study Match — matched against FlytBase's real case study library, with
a similarity score and reasoning for why this specific case study fits this
specific lead.

GTM Recommendation — direct AE, enterprise team, partner-led, or channel
partner, with the reasoning spelled out, not just a label.

Outreach — a ready-to-send email, LinkedIn message, call opening, discovery
questions, and two follow-ups, every one referencing something specific
about this lead, not a generic template.

And finally, the AE Handoff card — the single note a human AE actually
needs, exportable in one click."

*[Click "Copy all" / "Export" on the AE Handoff card]*

---

### 3:30 – 4:15 | Why This Matters / Why It's Better

"Three things make this more than a wrapper around an LLM:

First — it's grounded. Research is backed by live search, and case-study
matching can't hallucinate a case study that doesn't exist, because the
agent only ever sees the real library.

Second — it's honest about uncertainty. Confidence scores and 'missing
information' aren't cosmetic — they're what makes this actually trustworthy
enough for a human AE to act on without re-doing the work themselves.

Third — it's genuinely modular. Every agent is independently testable,
independently swappable, and the orchestrator is the only place that knows
the pipeline order — which is exactly how you'd want this to evolve into a
production system."

---

### 4:15 – 5:00 | Close

"This is a full-stack, production-shaped submission: Next.js and FastAPI,
typed contracts shared between frontend and backend, retry/cache/rate-limit
built into the LLM layer, and deployment-ready for Vercel and Render today.

Everything you just saw — the code, the architecture diagrams, and this
script — is in the repo. Thanks for watching."

---

## Presenter Notes

- If the API key isn't configured during a live judged demo, have the sample
  JSON response ready to paste manually so the UI can still be demonstrated
  end-to-end without a live LLM call.
- Keep one browser tab on `/dashboard` and one on `docs/mindmap.html` so you
  can switch to the interactive architecture view if asked a system-design
  question.
- If asked "why not one big prompt" — the answer is testability and cost:
  a 200-line mega-prompt is unreviewable and expensive to iterate on; 8 small
  prompts can each be unit-tested and improved independently.
