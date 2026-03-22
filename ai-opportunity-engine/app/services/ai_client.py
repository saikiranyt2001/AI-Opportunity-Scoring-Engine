import httpx


async def call_openai(prompt: str) -> dict[str, int | str]:
    async with httpx.AsyncClient(timeout=10) as client:
        _ = client
        return {"model": "openai", "score": 80}


async def call_anthropic(prompt: str) -> dict[str, int | str]:
    async with httpx.AsyncClient(timeout=10) as client:
        _ = client
        return {"model": "anthropic", "score": 75}
