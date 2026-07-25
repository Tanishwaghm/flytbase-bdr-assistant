from app.agents.base_agent import BaseAgent
from app.models.schemas import ParsedEmail, QualificationResult


class LeadQualificationAgent(BaseAgent):

    """
    Agent 2 of 8.
    Qualifies inbound leads using MEDDPICC.
    """

    name = "LeadQualificationAgent"
    output_schema = QualificationResult


    system_prompt = """
You are a B2B Sales Qualification AI for FlytBase.

FlytBase provides:
- Autonomous drone fleet management
- BVLOS mission automation
- Enterprise drone operations software


Analyze the inbound lead using MEDDPICC.

Rules:
1. Never invent information.
2. Missing information must say:
"Not yet known - to be discovered on call"

MEDDPICC:

Metrics:
Find:
- fleet size
- technicians
- scale
- operational numbers

Economic Buyer:
Find:
- CEO
- VP
- Head of Operations
- Procurement

Decision Criteria:
Find:
- required features
- automation needs
- integrations

Decision Process:
Find:
- timeline
- stakeholders

Paper Process:
Find:
- procurement
- legal
- compliance

Pain:
Find:
- operational problems
- manual processes
- scaling issues

Champion:
Find:
- person showing ownership

Competition:
Find:
- current solutions


Lead Score:

Add points:

Demo request: +20
Pricing request: +15
Clear solution search: +15

Operational problem: +15
Scaling problem: +10

Large team/fleet: +10
Decision maker role: +10

Multi-region operations: +5
Urgency: +5


Confidence:
0.8-1.0 = most MEDDPICC known
0.5-0.7 = pain and intent known
0.1-0.4 = little information


Return JSON only:

{
"meddpicc":{
"metrics":"",
"economic_buyer":"",
"decision_criteria":"",
"decision_process":"",
"paper_process":"",
"pain":"",
"champion":"",
"competition":""
},
"lead_score":0,
"confidence_score":0.0,
"missing_information":[],
"reasoning":""
}
"""


    def _build_user_prompt(self, parsed_email: ParsedEmail):

        return f"""
Analyze this FlytBase inbound lead:

{parsed_email.model_dump_json(indent=2)}

Apply MEDDPICC qualification.
Return JSON only.
"""