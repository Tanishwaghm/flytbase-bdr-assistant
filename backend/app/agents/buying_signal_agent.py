from app.agents.base_agent import BaseAgent
from app.models.schemas import ParsedEmail, CompanyResearch, BuyingSignalResult


class BuyingSignalAgent(BaseAgent):
    """
    Agent 4 of 8.
    Cross-references the parsed email + company research to flag concrete buying
    signals across 7 fixed categories. Every signal must be explained - a BDR/AE
    should never see "buying_intent: true" without a reason they can repeat to
    the prospect or use to write a smarter follow-up.
    """

    name = "BuyingSignalAgent"
    output_schema = BuyingSignalResult

    system_prompt = """You are a B2B sales intelligence analyst identifying buying signals \
for FlytBase, an autonomous drone fleet management / BVLOS software company.

Evaluate the lead across exactly these 7 signal types:
expansion, hiring, funding, digital_transformation, drone_adoption, enterprise_readiness, buying_intent

For each: set detected (true/false), strength (weak/moderate/strong), and a 1-2 sentence \
explanation grounded in the actual parsed email or research data provided - never invent evidence.

Then compute overall_buying_intent_score (0-100), weighting "buying_intent" and "drone_adoption" \
most heavily, informed by how many other signals are strong/detected.

Respond ONLY with JSON matching:
{
  "signals": [
    {"signal_type": string, "detected": boolean, "explanation": string, "strength": string}, ...
  ],
  "overall_buying_intent_score": number
}
Include all 7 signal_types even if detected=false."""

    def _build_user_prompt(self, parsed_email: ParsedEmail, research: CompanyResearch) -> str:
        return f"""Parsed inbound email:
{parsed_email.model_dump_json(indent=2)}

Company research profile:
{research.model_dump_json(indent=2)}

Return the JSON buying signal analysis."""
