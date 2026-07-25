"""
BaseAgent
---------
Every agent in this system is a thin, single-responsibility wrapper around:
  1. A system prompt (its "job description")
  2. A user-prompt builder (turns typed input into an LLM prompt)
  3. A Pydantic output schema (enforces the contract with the orchestrator)

This is the core of the "don't build everything inside one prompt" requirement:
each agent only knows about its own input type and output type. The orchestrator
is the only thing that knows the full pipeline order.
"""
from __future__ import annotations

import logging
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

from app.services.llm_service import generate_json, LLMError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AgentError(Exception):
    """Raised when an agent cannot produce a valid, schema-conformant result."""


class BaseAgent:
    name: str = "BaseAgent"
    system_prompt: str = "You are a helpful assistant. Always reply with valid JSON."
    output_schema: Type[BaseModel]

    def _build_user_prompt(self, **kwargs) -> str:  # pragma: no cover - overridden
        raise NotImplementedError

    def run(self, **kwargs) -> BaseModel:
        user_prompt = self._build_user_prompt(**kwargs)
        try:
            raw = generate_json(self.system_prompt, user_prompt, model_hint=self.name)
        except LLMError as e:
            logger.error(f"[{self.name}] LLM call failed: {e}")
            raise AgentError(f"{self.name} failed to get a response from the LLM: {e}") from e

        try:
            return self.output_schema.model_validate(raw)
        except ValidationError as e:
            logger.error(f"[{self.name}] Output failed schema validation: {e}")
            raise AgentError(f"{self.name} produced output that failed validation: {e}") from e
