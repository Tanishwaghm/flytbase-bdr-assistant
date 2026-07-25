"""
Search Service
---------------
Thin wrapper around a real web-search API so the Company Research Agent can
ground its output in actual public information instead of hallucinating.

Provider: Tavily (https://tavily.com) - purpose-built for LLM agent research,
generous free tier, simple REST API. Swap-in SerpAPI/Bing by replacing `search()`.

If no TAVILY_API_KEY is configured (e.g. local dev without a key), this
gracefully degrades to an empty result set and the Company Research Agent
falls back to clearly-labeled low-confidence LLM-only reasoning - it never
silently pretends to have done real research.
"""
from __future__ import annotations

import logging
import os
from typing import List, TypedDict

import requests

logger = logging.getLogger(__name__)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
TAVILY_URL = "https://api.tavily.com/search"


class SearchResult(TypedDict):
    title: str
    url: str
    content: str


def search(query: str, max_results: int = 5) -> List[SearchResult]:
    if not TAVILY_API_KEY:
        logger.warning("TAVILY_API_KEY not set - skipping live web research (degraded mode).")
        return []

    try:
        resp = requests.post(
            TAVILY_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "search_depth": "advanced",
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        return [
            {"title": r.get("title", ""), "url": r.get("url", ""), "content": r.get("content", "")}
            for r in data.get("results", [])
        ]
    except Exception as e:  # noqa: BLE001
        logger.error(f"Search API call failed: {e}")
        return []


def research_company(company_name: str, industry_hint: str = "") -> List[SearchResult]:
    """Runs a small batch of targeted queries and merges results."""
    queries = [
        f"{company_name} company overview",
        f"{company_name} funding news",
        f"{company_name} careers hiring",
        f"{company_name} {industry_hint} products".strip(),
    ]
    merged: List[SearchResult] = []
    seen_urls = set()
    for q in queries:
        for r in search(q, max_results=3):
            if r["url"] and r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                merged.append(r)
    return merged
