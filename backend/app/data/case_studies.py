"""
FlytBase case study library.

In production this would be pulled from a CMS / vector DB (e.g. flytbase.com/case-studies
scraped + embedded). For the hackathon submission we ship a representative, realistic
dataset so the Case Study Matching Agent has real material to reason over instead of
hallucinating case studies.
"""

CASE_STUDIES = [
    {
        "id": "cs_bvlos_infra_inspection",
        "title": "Autonomous BVLOS Power-Line Inspection at Scale",
        "industry": "Energy & Utilities",
        "use_case": "BVLOS inspection, drone-in-a-box, fleet automation",
        "summary": (
            "A European utility deployed FlytBase-powered drone-in-a-box stations to "
            "run autonomous BVLOS inspections of transmission infrastructure, cutting "
            "manual inspection time significantly while improving fault-detection turnaround."
        ),
        "tags": ["BVLOS", "energy", "utilities", "inspection", "autonomous", "fleet management", "europe"],
    },
    {
        "id": "cs_port_security_surveillance",
        "title": "24/7 Autonomous Perimeter Surveillance for Port Operations",
        "industry": "Logistics & Ports",
        "use_case": "Autonomous surveillance, remote operations, fleet management",
        "summary": (
            "A port operator automated perimeter and yard surveillance using scheduled "
            "autonomous drone missions orchestrated through FlytBase, replacing ad-hoc "
            "manual patrol flights with a always-on remote operations model."
        ),
        "tags": ["surveillance", "security", "ports", "logistics", "remote operations", "enterprise"],
    },
    {
        "id": "cs_construction_progress",
        "title": "Automated Construction Site Progress Monitoring",
        "industry": "Construction & Real Estate",
        "use_case": "Mapping, progress tracking, multi-site fleet coordination",
        "summary": (
            "A multi-site construction firm standardized weekly progress capture across "
            "sites using scheduled autonomous missions, feeding orthomosaic maps directly "
            "into their project management stack via FlytBase APIs."
        ),
        "tags": ["construction", "mapping", "progress monitoring", "multi-site", "integration"],
    },
    {
        "id": "cs_drone_inspection_saas",
        "title": "Drone Inspection SaaS Platform Fleet Orchestration",
        "industry": "Drone Software / Inspection Services",
        "use_case": "Fleet management, BVLOS, multi-tenant drone-in-a-box orchestration",
        "summary": (
            "A drone inspection software company operating across multiple European "
            "countries used FlytBase as the underlying fleet orchestration and BVLOS "
            "automation layer to scale their own SaaS offering to enterprise clients "
            "without building flight-ops infrastructure in-house."
        ),
        "tags": ["drone software", "BVLOS", "fleet management", "europe", "saas", "inspection", "partner"],
    },
    {
        "id": "cs_mining_stockpile",
        "title": "Autonomous Stockpile Volumetrics for Mining Operations",
        "industry": "Mining & Natural Resources",
        "use_case": "Volumetric analysis, autonomous mapping, remote sites",
        "summary": (
            "A mining operator replaced manual survey flights with autonomous, scheduled "
            "stockpile-volume missions, integrating results directly into their ERP for "
            "near-real-time inventory reconciliation."
        ),
        "tags": ["mining", "volumetrics", "remote operations", "autonomous mapping"],
    },
    {
        "id": "cs_public_safety_response",
        "title": "First-Responder Drone-as-First-Responder Program",
        "industry": "Public Safety & Government",
        "use_case": "Rapid response, remote piloting, enterprise readiness",
        "summary": (
            "A public safety agency built a drone-as-first-responder program on FlytBase, "
            "enabling dispatch-triggered autonomous launches from rooftop docks with sub-90-second "
            "response times."
        ),
        "tags": ["public safety", "government", "rapid response", "enterprise readiness", "autonomous"],
    },
]
