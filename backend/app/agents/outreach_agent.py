from app.agents.base_agent import BaseAgent
from app.models.schemas import (
    ParsedEmail, CompanyResearch, QualificationResult,
    CaseStudyResult, OutreachPackage,
)


class OutreachAgent(BaseAgent):
    """
    Agent 7 of 8.
    Generates every piece of outbound copy an SDR/AE needs to actually work the lead:
    reply email, LinkedIn message, call opening, discovery questions, and two follow-ups.

    Personalization is anchored to real extracted facts (pain points, research, case study)
    rather than generic templates - the prompt explicitly forbids filler like "I hope this
    email finds you well" and requires at least one specific, concrete reference per message.
    """

    name = "OutreachAgent"
    output_schema = OutreachPackage

    system_prompt = """You are a top-performing SDR at FlytBase (enterprise drone fleet \
management / BVLOS automation software) writing outreach for a qualified inbound lead.

Voice: confident, concise, consultative - never generic or salesy. Avoid filler openers \
like "I hope this email finds you well" or "I wanted to reach out". Every message must \
reference at least one SPECIFIC fact from the lead data (their stated need, industry, \
pain point, or the recommended case study).

Generate:
- personalized_email_subject: short, specific, not clickbait
- personalized_email_body: 120-180 words, references their stated need + the recommended \
case study by name + a clear single CTA (proposed demo time framing)
- linkedin_message: <300 characters, casual but specific
- call_opening: 2-3 sentences a rep would say in the first 15 seconds of a call
- discovery_questions: 5 sharp MEDDPICC-informed questions tailored to this lead's gaps
- follow_up_1: short, sent ~3 days later if no reply, adds one new piece of value \
(e.g. a relevant stat or the case study link)
- follow_up_2: short, sent ~7 days later, lower-pressure "break-up" style nudge

Respond ONLY with JSON matching:
{
  "personalized_email_subject": string, "personalized_email_body": string,
  "linkedin_message": string, "call_opening": string,
  "discovery_questions": string[], "follow_up_1": string, "follow_up_2": string
}"""

    def _build_user_prompt(
        self,
        parsed_email: ParsedEmail,
        research: CompanyResearch,
        qualification: QualificationResult,
        case_study: CaseStudyResult,
    ) -> str:
        return f"""Lead:
{parsed_email.model_dump_json(indent=2)}

Company research:
{research.model_dump_json(indent=2)}

MEDDPICC qualification (use missing_information to sharpen discovery questions):
{qualification.model_dump_json(indent=2)}

Recommended case study to reference by name:
{case_study.recommended_case_study.model_dump_json(indent=2)}

Return the JSON outreach package."""
