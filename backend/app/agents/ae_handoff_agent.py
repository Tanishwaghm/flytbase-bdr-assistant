from app.agents.base_agent import BaseAgent
from app.models.schemas import (
    ParsedEmail, CompanyResearch, QualificationResult,
    BuyingSignalResult, CaseStudyResult, GTMRecommendation, AEHandoffSummary,
)


class AEHandoffAgent(BaseAgent):
    """
    Agent 8 of 8 - the final step of the pipeline.
    Synthesizes everything the previous 7 agents produced into a single CRM-ready
    note. This is deliberately the ONLY agent allowed to read all upstream outputs
    at once - every other agent only sees what it strictly needs, keeping the
    architecture modular and each prompt's context small and cheap.
    """

    name = "AEHandoffAgent"
    output_schema = AEHandoffSummary

    system_prompt = """You are a Sales Operations analyst writing a CRM handoff note \
from an SDR/AI pipeline to a human Account Executive at FlytBase.

Write it the way a sharp SDR would write real CRM notes: dense, factual, skimmable in \
under 30 seconds, zero fluff. research_summary should be 2-3 sentences max. pain_points \
and buying_signals should be short bullet phrases (reuse/condense upstream data, don't \
re-derive). recommended_demo_focus should be one specific, concrete demo angle (not \
"give a general demo"). next_action should be one concrete next step with a rough timeframe.

confidence_score = overall confidence across the pipeline (average the qualification and \
research confidence scores, adjusted by your judgment).

Respond ONLY with JSON matching:
{
  "lead_score": number, "research_summary": string, "pain_points": string[],
  "buying_signals": string[], "recommended_demo_focus": string,
  "recommended_case_study": string, "recommended_owner": string,
  "next_action": string, "confidence_score": number
}"""

    def _build_user_prompt(
        self,
        parsed_email: ParsedEmail,
        research: CompanyResearch,
        qualification: QualificationResult,
        buying_signals: BuyingSignalResult,
        case_study: CaseStudyResult,
        gtm: GTMRecommendation,
    ) -> str:
        return f"""Parsed email: {parsed_email.model_dump_json()}
Research: {research.model_dump_json()}
Qualification: {qualification.model_dump_json()}
Buying signals: {buying_signals.model_dump_json()}
Case study match: {case_study.model_dump_json()}
GTM recommendation: {gtm.model_dump_json()}

Return the JSON AE handoff summary."""
