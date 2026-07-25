from __future__ import annotations

import hashlib
import json
import logging
import time
from collections import deque
from typing import Any, Optional

from app.config import get_settings

logger = logging.getLogger("llm_service")

settings = get_settings()


class RateLimiter:
    def __init__(self, max_calls_per_minute: int):
        self.max_calls = max_calls_per_minute
        self.calls = deque()

    def acquire(self):
        now = time.time()

        while self.calls and now - self.calls[0] > 60:
            self.calls.popleft()

        if len(self.calls) >= self.max_calls:
            sleep_for = 60 - (now - self.calls[0])
            logger.warning(f"Sleeping {sleep_for:.2f}s")
            time.sleep(max(sleep_for, 0))

        self.calls.append(time.time())


class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self.store = {}

    def get(self, key):
        item = self.store.get(key)

        if item is None:
            return None

        ts, value = item

        if time.time() - ts > self.ttl:
            del self.store[key]
            return None

        return value

    def set(self, key, value):
        self.store[key] = (time.time(), value)


_rate_limiter = RateLimiter(settings.rate_limit_per_minute)
_cache = TTLCache(settings.cache_ttl_seconds)


class LLMError(Exception):
    pass


def _cache_key(system_prompt, user_prompt, model):
    raw = f"{model}::{system_prompt}::{user_prompt}"
    return hashlib.sha256(raw.encode()).hexdigest()


# ---------------- OPENAI ----------------

def _call_openai(system_prompt, user_prompt):
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content or "{}"


# ---------------- GEMINI ----------------

def _call_gemini(system_prompt, user_prompt):
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)

    model = genai.GenerativeModel(
        settings.gemini_model,
        system_instruction=system_prompt,
        generation_config={
            "response_mime_type": "application/json"
        },
    )

    response = model.generate_content(user_prompt)

    return response.text or "{}"


# ---------------- GROQ ----------------

def _call_groq(system_prompt, user_prompt):
    from groq import Groq

    client = Groq(
        api_key=settings.groq_api_key
    )

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
        response_format={
            "type": "json_object"
        },
    )

    return response.choices[0].message.content or "{}"


def generate_json(system_prompt, user_prompt, model_hint=""):
    provider = settings.llm_provider.lower()

    if provider == "openai":
        model_name = settings.openai_model

    elif provider == "gemini":
        model_name = settings.gemini_model

    elif provider == "groq":
        model_name = settings.groq_model

    else:
        raise LLMError(f"Unknown provider {provider}")

    key = _cache_key(
        system_prompt,
        user_prompt,
        model_name,
    )

    cached = _cache.get(key)

    if cached is not None:
        return cached

    last_error = None

    for attempt in range(1, settings.max_retries + 1):

        try:
            _rate_limiter.acquire()

            if provider == "openai":
                raw = _call_openai(system_prompt, user_prompt)

            elif provider == "gemini":
                raw = _call_gemini(system_prompt, user_prompt)

            elif provider == "groq":
                raw = _call_groq(system_prompt, user_prompt)

            parsed = json.loads(raw)

            _cache.set(key, parsed)

            return parsed

        except json.JSONDecodeError as e:
            last_error = e

            user_prompt += (
                "\nReturn ONLY valid JSON."
            )

        except Exception as e:
            last_error = e
            logger.warning(f"[attempt {attempt}] {e}")

        if attempt < settings.max_retries:
            time.sleep(settings.retry_backoff_seconds * attempt)

    raise LLMError(
        f"LLM call failed after {settings.max_retries} attempts: {last_error}"
    )