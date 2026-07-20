"""Stub providers module for LLM calls."""

import logging

logger = logging.getLogger("providers")


async def call_model(model: str, messages: list, max_tokens: int = 1024, **kwargs) -> str:
    logger.warning("call_model stub called — no LLM backend configured")
    return "[LLM stub response]"


def resolve_persona_override(persona) -> str | None:
    return None
