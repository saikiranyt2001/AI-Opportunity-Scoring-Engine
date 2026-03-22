import asyncio
import httpx
from typing import Any

from app.core.config import settings


TIMEOUT_SECONDS = 8


async def safe_call(fn, prompt: str) -> Any:
    try:
        return await asyncio.wait_for(fn(prompt), timeout=TIMEOUT_SECONDS)
    except Exception:
        return None


async def call_gpt4o(prompt: str) -> dict[str, int | str]:
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        return {"model": "gpt-4o", "score": 80}


async def call_gemini(prompt: str) -> dict[str, int | str]:
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        return {"model": "gemini", "score": 78}


async def call_grok(prompt: str) -> dict[str, int | str]:
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        return {"model": "grok", "score": 76}


def reconcile_shadow_scores(results: list[dict[str, int | str]]) -> dict[str, float | int]:
    scores = [int(item["score"]) for item in results if "score" in item]

    if not scores:
        return {
            "models_responded": 0,
            "average_score": 0.0,
            "score_spread": 0.0,
        }

    return {
        "models_responded": len(scores),
        "average_score": round(sum(scores) / len(scores), 2),
        "score_spread": float(max(scores) - min(scores)),
    }


async def run_shadow_reconciliation(prompt: str) -> dict[str, Any]:
    tasks = [
        safe_call(call_gpt4o, prompt),
        safe_call(call_gemini, prompt),
        safe_call(call_grok, prompt),
    ]

    results = await asyncio.gather(*tasks)

    valid_results: list[dict[str, int | str]] = []
    failures = 0

    for result in results:
        if result is None:
            failures += 1
            continue
        valid_results.append(result)

    return {
        "results": valid_results,
        "reconciliation": reconcile_shadow_scores(valid_results),
        "failures": failures,
        "phase1_subscriber_visible": False,
        "timezone": settings.scheduler_timezone,
    }


async def run_shadow_models(prompt: str) -> list[dict[str, int | str]]:
    shadow_payload = await run_shadow_reconciliation(prompt)
    return shadow_payload.get("results", [])