"""
Shared Pydantic schemas for every agent's input/output contract.
Keeping these centralized enforces a strict, typed handoff between agents,
which is what lets the orchestrator chain them safely.
"""
from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# 1. Email Parser Agent
# ---------------------------------------------------------------------------
class ParsedEmail(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    intent: Literal[
        "demo_request", "pricing_inquiry", "partnership",
        "support", "general_inquiry", "career", "unknown"
    ] = "unknown"
    urgency: Literal["low", "medium", "high", "critical"] = "medium"
    pain_points: List[str] = Field(default_factory=list)
    raw_text: str = ""
    confidence_score: float = 0.0


# ---------------------------------------------------------------------------
# 2. Lead Qualification Agent (MEDDPICC)
# ---------------------------------------------------------------------------
class MeddpiccBreakdown(BaseModel):
    metrics: str = ""
    economic_buyer: str = ""
    decision_criteria: str = ""
    decision_process: str = ""
    paper_process: str = ""
    pain: str = ""
    champion: str = ""
    competition: str = ""


class QualificationResult(BaseModel):
    meddpicc: MeddpiccBreakdown
    lead_score: int = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0, le=1)
    missing_information: List[str] = Field(default_factory=list)
    reasoning: str = ""


# ---------------------------------------------------------------------------
# 3. Company Research Agent
# ---------------------------------------------------------------------------
class CompanyResearch(BaseModel):
    company_description: str = ""
    products: List[str] = Field(default_factory=list)
    industry: str = ""
    employee_count_estimate: str = ""
    locations: List[str] = Field(default_factory=list)
    funding: str = ""
    recent_news: List[str] = Field(default_factory=list)
    hiring_signals: List[str] = Field(default_factory=list)
    technology_stack: List[str] = Field(default_factory=list)
    growth_signals: List[str] = Field(default_factory=list)
    competitors: List[str] = Field(default_factory=list)
    website_summary: str = ""
    linkedin_summary: str = ""
    confidence_score: float = Field(ge=0, le=1, default=0.0)
    sources: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# 4. Buying Signal Agent
# ---------------------------------------------------------------------------
class BuyingSignal(BaseModel):
    signal_type: Literal[
        "expansion", "hiring", "funding", "digital_transformation",
        "drone_adoption", "enterprise_readiness", "buying_intent"
    ]
    detected: bool
    explanation: str = ""
    strength: Literal["weak", "moderate", "strong"] = "weak"


class BuyingSignalResult(BaseModel):
    signals: List[BuyingSignal]
    overall_buying_intent_score: int = Field(ge=0, le=100)


# ---------------------------------------------------------------------------
# 5. Case Study Matching Agent
# ---------------------------------------------------------------------------
class CaseStudyMatch(BaseModel):
    case_study_id: str
    title: str
    industry: str
    similarity_score: float = Field(ge=0, le=1)
    reasoning: str = ""


class CaseStudyResult(BaseModel):
    top_matches: List[CaseStudyMatch]
    recommended_case_study: CaseStudyMatch


# ---------------------------------------------------------------------------
# 6. GTM Recommendation Agent
# ---------------------------------------------------------------------------
class GTMRecommendation(BaseModel):
    motion: Literal["direct_ae", "partner_led", "enterprise_team", "channel_partner"]
    reasoning: str = ""
    confidence_score: float = Field(ge=0, le=1, default=0.0)
    suggested_owner_type: str = ""


# ---------------------------------------------------------------------------
# 7. Outreach Agent
# ---------------------------------------------------------------------------
class OutreachPackage(BaseModel):
    personalized_email_subject: str = ""
    personalized_email_body: str = ""
    linkedin_message: str = ""
    call_opening: str = ""
    discovery_questions: List[str] = Field(default_factory=list)
    follow_up_1: str = ""
    follow_up_2: str = ""


# ---------------------------------------------------------------------------
# 8. AE Handoff Agent
# ---------------------------------------------------------------------------
class AEHandoffSummary(BaseModel):
    lead_score: int
    research_summary: str = ""
    pain_points: List[str] = Field(default_factory=list)
    buying_signals: List[str] = Field(default_factory=list)
    recommended_demo_focus: str = ""
    recommended_case_study: str = ""
    recommended_owner: str = ""
    next_action: str = ""
    confidence_score: float = Field(ge=0, le=1, default=0.0)


# ---------------------------------------------------------------------------
# Orchestrated end-to-end result
# ---------------------------------------------------------------------------
class FullAnalysisResult(BaseModel):
    parsed_email: ParsedEmail
    qualification: QualificationResult
    research: CompanyResearch
    buying_signals: BuyingSignalResult
    case_study: CaseStudyResult
    gtm: GTMRecommendation
    outreach: OutreachPackage
    ae_handoff: AEHandoffSummary


class AnalyzeEmailRequest(BaseModel):
    email_text: str = Field(..., min_length=10)
