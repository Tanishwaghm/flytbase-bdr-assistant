"""
REST API routes.

Design note: the granular endpoints (/qualify, /research, /case-study, /recommend,
/generate-email, /handoff) are stateless - each accepts the raw email_text and
internally re-runs only the agents it needs (via the orchestrator's per-agent
functions). This keeps the API simple (no server-side session/DB required for
the hackathon submission) while still exposing each agent as its own endpoint,
as required. The LLM response cache in llm_service means re-parsing the same
email for each granular call is cheap (cache hit) rather than re-billed.
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.schemas import AnalyzeEmailRequest, FullAnalysisResult
from app.agents.base_agent import AgentError
from app import orchestrator as orch

logger = logging.getLogger("api")
router = APIRouter()


class EmailTextRequest(BaseModel):
    email_text: str


def _handle(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except AgentError as e:
        logger.error(str(e))
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:  # noqa: BLE001
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@router.post("/analyze-email", response_model=FullAnalysisResult, tags=["pipeline"])
def analyze_email(payload: AnalyzeEmailRequest):
    """Runs the FULL 8-agent pipeline end-to-end. Primary endpoint used by the dashboard."""
    return _handle(orch.run_full_pipeline, payload.email_text)


@router.post("/qualify", tags=["agents"])
def qualify(payload: EmailTextRequest):
    """Runs Parser -> Qualification only."""
    parsed = _handle(orch.run_parser, payload.email_text)
    qualification = _handle(orch.run_qualification, parsed)
    return {"parsed_email": parsed, "qualification": qualification}


@router.post("/research", tags=["agents"])
def research(payload: EmailTextRequest):
    """Runs Parser -> Company Research only."""
    parsed = _handle(orch.run_parser, payload.email_text)
    result = _handle(orch.run_research, parsed)
    return {"parsed_email": parsed, "research": result}


@router.post("/case-study", tags=["agents"])
def case_study(payload: EmailTextRequest):
    """Runs Parser -> Research -> Case Study Matching."""
    parsed = _handle(orch.run_parser, payload.email_text)
    research_result = _handle(orch.run_research, parsed)
    match = _handle(orch.run_case_study, parsed, research_result)
    return {"parsed_email": parsed, "research": research_result, "case_study": match}


@router.post("/recommend", tags=["agents"])
def recommend(payload: EmailTextRequest):
    """Runs the full chain needed to produce a GTM recommendation."""
    parsed = _handle(orch.run_parser, payload.email_text)
    research_result = _handle(orch.run_research, parsed)
    qualification = _handle(orch.run_qualification, parsed)
    signals = _handle(orch.run_buying_signals, parsed, research_result)
    gtm = _handle(orch.run_gtm, parsed, research_result, qualification, signals)
    return {
        "parsed_email": parsed, "research": research_result,
        "qualification": qualification, "buying_signals": signals, "gtm": gtm,
    }


@router.post("/generate-email", tags=["agents"])
def generate_email(payload: EmailTextRequest):
    """Runs the chain needed to produce the outreach package."""
    parsed = _handle(orch.run_parser, payload.email_text)
    research_result = _handle(orch.run_research, parsed)
    qualification = _handle(orch.run_qualification, parsed)
    case_study_result = _handle(orch.run_case_study, parsed, research_result)
    outreach = _handle(orch.run_outreach, parsed, research_result, qualification, case_study_result)
    return {"parsed_email": parsed, "case_study": case_study_result, "outreach": outreach}


@router.post("/handoff", tags=["agents"])
def handoff(payload: EmailTextRequest):
    """Runs the full pipeline and returns just the final AE handoff summary."""
    result = _handle(orch.run_full_pipeline, payload.email_text)
    return {"ae_handoff": result.ae_handoff}


@router.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
