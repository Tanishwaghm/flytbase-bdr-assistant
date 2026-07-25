import json

from app.agents.base_agent import BaseAgent
from app.data.case_studies import CASE_STUDIES
from app.models.schemas import ParsedEmail, CompanyResearch, CaseStudyResult


class CaseStudyMatchingAgent(BaseAgent):
    """
    Agent 5 of 8.
    Matches the lead against FlytBase's case study library (app/data/case_studies.py).

    Deliberately retrieval-augmented rather than free-generation: the agent is given
    the FULL case study library in-context and asked to select/score/rank from it,
    so it can never recommend a case study that doesn't exist.
    """

    name = "CaseStudyMatchingAgent"
    output_schema = CaseStudyResult

    system_prompt = """You are a solutions consultant matching an inbound lead to the \
most relevant FlytBase customer case study.

You will be given:
1. The lead's parsed email + company research
2. The FULL list of available FlytBase case studies (id, title, industry, use_case, tags)

Select the TOP 3 most relevant case studies from the provided list ONLY - never invent \
a case study that isn't in the list. Score similarity_score 0.0-1.0 based on overlap in \
industry, use case (BVLOS, inspection, surveillance, mapping, fleet management, etc.), \
region, and company type. Explain the reasoning for each in 1-2 sentences referencing \
specific overlapping details.

recommended_case_study must be the single highest-scoring match from top_matches.

Respond ONLY with JSON matching:
{
  "top_matches": [
    {"case_study_id": string, "title": string, "industry": string,
     "similarity_score": number, "reasoning": string}, ...
  ],
  "recommended_case_study": {same shape as one top_matches entry}
}"""

    def _build_user_prompt(self, parsed_email: ParsedEmail, research: CompanyResearch) -> str:
        return f"""Lead data:
{parsed_email.model_dump_json(indent=2)}

Company research:
{research.model_dump_json(indent=2)}

Available FlytBase case studies (choose ONLY from this list):
{json.dumps(CASE_STUDIES, indent=2)}

Return the JSON case study match result."""
