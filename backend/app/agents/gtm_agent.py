from app.agents.base_agent import BaseAgent
from app.models.schemas import (
    ParsedEmail, CompanyResearch, QualificationResult,
    BuyingSignalResult, GTMRecommendation,
)


class GTMRecommendationAgent(BaseAgent):
    """
    Agent 6 of 8.
    Decides the go-to-market motion: direct_ae, partner_led, enterprise_team, or channel_partner.

    Heuristics this agent is prompted to weigh (mirrors how FlytBase's real sales org
    likely segments inbound: company size/enterprise-readiness -> enterprise_team,
    lead_score + strong buying_intent -> direct_ae, a lead that is itself a
    software/service reseller in the drone space -> channel_partner or partner_led,
    ambiguous/low-confidence/early-stage -> partner_led as a lower-touch motion).
    """

    name = "GTMRecommendationAgent"
    output_schema = GTMRecommendation

    system_prompt = """You are a Revenue Operations strategist deciding the go-to-market \
motion for an inbound lead at FlytBase (enterprise drone fleet management / BVLOS software).

Choose exactly one motion:
- direct_ae: high lead_score, clear enterprise buyer, strong buying intent -> route to an Account Executive now.
- enterprise_team: large/complex organization (government, large enterprise, multi-site, \
regulated industry) needing a specialized enterprise sales motion.
- partner_led: the lead is itself a software/service company or systems integrator that would \
white-label or build on top of FlytBase, or the deal is lower-touch/early-stage.
- channel_partner: the lead is best served by an existing regional/distribution partner \
(e.g. strong regional presence, hardware reseller, or region FlytBase serves via partners).

Explain WHY in 2-4 sentences citing specific evidence (company type, region, lead_score, \
buying signals). Also give suggested_owner_type (e.g. "Enterprise AE - EMEA", "Partner Manager").
confidence_score reflects how clear-cut the decision is given available data.

Respond ONLY with JSON matching:
{"motion": string, "reasoning": string, "confidence_score": number, "suggested_owner_type": string}"""

    def _build_user_prompt(
        self,
        parsed_email: ParsedEmail,
        research: CompanyResearch,
        qualification: QualificationResult,
        buying_signals: BuyingSignalResult,
    ) -> str:
        return f"""Parsed email:
{parsed_email.model_dump_json(indent=2)}

Company research:
{research.model_dump_json(indent=2)}

Qualification (MEDDPICC):
{qualification.model_dump_json(indent=2)}

Buying signals:
{buying_signals.model_dump_json(indent=2)}

Return the JSON GTM recommendation."""
