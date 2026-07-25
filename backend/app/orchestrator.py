"""
Orchestrator
------------
The ONLY module that knows the full agent pipeline order. Each agent stays
ignorant of the others - this is what "modular AI agent architecture" means
in practice: swap, reorder, or A/B test a single agent without touching the rest.

Pipeline:
  Email --> Parser --> Qualification --> Research --> Buying Signals
        --> Case Study --> GTM --> Outreach --> AE Handoff

Error handling strategy:
  If any agent fails (LLM error / validation error after retries), the
  orchestrator raises immediately rather than silently continuing with
  partial/garbage data - a wrong downstream recommendation built on a failed
  upstream step is worse than a clear error the frontend can surface.
"""
from __future__ import annotations

import logging

from app.agents.email_parser_agent import EmailParserAgent
from app.agents.lead_qualification_agent import LeadQualificationAgent
from app.agents.company_research_agent import CompanyResearchAgent
from app.agents.buying_signal_agent import BuyingSignalAgent
from app.agents.case_study_agent import CaseStudyMatchingAgent
from app.agents.gtm_agent import GTMRecommendationAgent
from app.agents.outreach_agent import OutreachAgent
from app.agents.ae_handoff_agent import AEHandoffAgent
from app.models.schemas import FullAnalysisResult

logger = logging.getLogger("orchestrator")

_parser = EmailParserAgent()
_qualifier = LeadQualificationAgent()
_researcher = CompanyResearchAgent()
_signals = BuyingSignalAgent()
_case_study = CaseStudyMatchingAgent()
_gtm = GTMRecommendationAgent()
_outreach = OutreachAgent()
_handoff = AEHandoffAgent()


def run_full_pipeline(email_text: str) -> FullAnalysisResult:
    logger.info("Pipeline start: EmailParserAgent")
    parsed_email = _parser.run(email_text=email_text)

    logger.info("Pipeline: LeadQualificationAgent")
    qualification = _qualifier.run(parsed_email=parsed_email)

    logger.info("Pipeline: CompanyResearchAgent")
    research = _researcher.run(parsed_email=parsed_email)

    logger.info("Pipeline: BuyingSignalAgent")
    buying_signals = _signals.run(parsed_email=parsed_email, research=research)

    logger.info("Pipeline: CaseStudyMatchingAgent")
    case_study = _case_study.run(parsed_email=parsed_email, research=research)

    logger.info("Pipeline: GTMRecommendationAgent")
    gtm = _gtm.run(
        parsed_email=parsed_email, research=research,
        qualification=qualification, buying_signals=buying_signals,
    )

    logger.info("Pipeline: OutreachAgent")
    outreach = _outreach.run(
        parsed_email=parsed_email, research=research,
        qualification=qualification, case_study=case_study,
    )

    logger.info("Pipeline: AEHandoffAgent")
    ae_handoff = _handoff.run(
        parsed_email=parsed_email, research=research, qualification=qualification,
        buying_signals=buying_signals, case_study=case_study, gtm=gtm,
    )

    logger.info("Pipeline complete")
    return FullAnalysisResult(
        parsed_email=parsed_email,
        qualification=qualification,
        research=research,
        buying_signals=buying_signals,
        case_study=case_study,
        gtm=gtm,
        outreach=outreach,
        ae_handoff=ae_handoff,
    )


# Individual-agent entry points, used by the granular /qualify, /research etc. endpoints
# so the frontend can re-run a single stage without re-running the whole pipeline.
def run_parser(email_text: str):
    return _parser.run(email_text=email_text)


def run_qualification(parsed_email):
    return _qualifier.run(parsed_email=parsed_email)


def run_research(parsed_email):
    return _researcher.run(parsed_email=parsed_email)


def run_buying_signals(parsed_email, research):
    return _signals.run(parsed_email=parsed_email, research=research)


def run_case_study(parsed_email, research):
    return _case_study.run(parsed_email=parsed_email, research=research)


def run_gtm(parsed_email, research, qualification, buying_signals):
    return _gtm.run(
        parsed_email=parsed_email, research=research,
        qualification=qualification, buying_signals=buying_signals,
    )


def run_outreach(parsed_email, research, qualification, case_study):
    return _outreach.run(
        parsed_email=parsed_email, research=research,
        qualification=qualification, case_study=case_study,
    )


def run_handoff(parsed_email, research, qualification, buying_signals, case_study, gtm):
    return _handoff.run(
        parsed_email=parsed_email, research=research, qualification=qualification,
        buying_signals=buying_signals, case_study=case_study, gtm=gtm,
    )
