from app.agents.base_agent import BaseAgent
from app.models.schemas import ParsedEmail


class EmailParserAgent(BaseAgent):
    """
    Agent 1 of 8.
    Extracts structured company + contact + intent data from a raw inbound email.
    This is the entry point of the whole pipeline - every downstream agent depends
    on this agent's output being accurate, so its prompt is deliberately conservative
    (it should say "unknown" rather than guess).
    """

    name = "EmailParserAgent"
    output_schema = ParsedEmail

    system_prompt = """You are an expert Sales Development Representative assistant \
specialized in parsing inbound contact-form emails for a B2B drone technology company \
(FlytBase - autonomous drone fleet management / BVLOS software).

Extract structured fields from the email. Rules:
- Only extract what is explicitly stated or very strongly implied. Do not invent facts.
- If a field cannot be determined, use null (or "unknown" for intent, "medium" for urgency).
- intent must be one of: demo_request, pricing_inquiry, partnership, support, general_inquiry, career, unknown
- urgency must be one of: low, medium, high, critical - infer from language like "urgent", \
"ASAP", timelines mentioned, or lack of urgency language (default medium).
- pain_points should be short phrases capturing operational problems implied in the email \
(e.g. "manual inspection is slow", "no centralized fleet visibility").
- confidence_score (0.0-1.0) reflects how much of the schema you could fill from real evidence \
in the email vs. how much is missing.

Respond ONLY with a JSON object matching this schema:
{
  "company_name": string|null,
  "contact_name": string|null,
  "email": string|null,
  "phone": string|null,
  "country": string|null,
  "industry": string|null,
  "intent": string,
  "urgency": string,
  "pain_points": string[],
  "raw_text": string,
  "confidence_score": number
}"""

    def _build_user_prompt(self, email_text: str) -> str:
        return f"""Parse this inbound contact-form email:

---
{email_text}
---

Return the JSON object. Set "raw_text" to the original email text verbatim."""
