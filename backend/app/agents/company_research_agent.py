from app.agents.base_agent import BaseAgent
from app.models.schemas import ParsedEmail, CompanyResearch
from app.services.search_service import research_company


class CompanyResearchAgent(BaseAgent):
    """
    Agent 3 of 8.
    Grounds its output in real web search results (via search_service.research_company)
    rather than relying purely on the LLM's training data, which would go stale and
    risks hallucinated funding/employee numbers - exactly the kind of claim a BDR
    cannot afford to get wrong in front of a prospect.

    If no search API key is configured, this degrades honestly: confidence_score
    is capped low and website/linkedin summaries explicitly say research was
    not performed live, rather than fabricating detail.
    """

    name = "CompanyResearchAgent"
    output_schema = CompanyResearch

    system_prompt = """You are a B2B sales research analyst. You are given a company name \
and a set of raw web search snippets about that company. Synthesize them into a structured \
research profile for a drone-technology sales team (FlytBase).

Rules:
- Base every field on the provided snippets. Do not invent funding amounts, employee counts, \
or news that are not supported by the snippets.
- If the snippets are empty or insufficient, fill fields with best-effort general reasoning \
from the industry/context given, and set confidence_score <= 0.3, and explicitly note in \
website_summary/linkedin_summary that live research data was unavailable.
- growth_signals and hiring_signals should be short bullet-style phrases inferred from the \
snippets (e.g., "expanding into 3 new countries", "hiring 12 engineering roles").
- sources should list the URLs of snippets actually used.

Respond ONLY with JSON matching:
{
  "company_description": string, "products": string[], "industry": string,
  "employee_count_estimate": string, "locations": string[], "funding": string,
  "recent_news": string[], "hiring_signals": string[], "technology_stack": string[],
  "growth_signals": string[], "competitors": string[], "website_summary": string,
  "linkedin_summary": string, "confidence_score": number, "sources": string[]
}"""

    def _build_user_prompt(self, parsed_email: ParsedEmail) -> str:
        company = parsed_email.company_name or "Unknown Company"
        industry = parsed_email.industry or ""
        results = research_company(company, industry)

        if results:
            snippets_text = "\n\n".join(
                f"[{i+1}] {r['title']} ({r['url']})\n{r['content'][:600]}"
                for i, r in enumerate(results)
            )
        else:
            snippets_text = "(No live search results available - reason with caution and cap confidence_score <= 0.3.)"

        return f"""Company to research: {company}
Industry hint from inbound email: {industry or "unknown"}
Country hint: {parsed_email.country or "unknown"}

Web search snippets:
{snippets_text}

Return the JSON research profile."""
