import httpx

from app.core.config import settings
from app.exceptions.llm import LlmUnavailableException


def chat(content: str) -> dict:
    url = settings.ollama_base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": settings.ollama_model,
        "messages": [{"role": "user", "content": content}],
    }

    try:
        response = httpx.post(url, json=payload, timeout=60.0)
        response.raise_for_status()
        data = response.json()
    except (httpx.RequestError, httpx.HTTPStatusError):
        raise LlmUnavailableException()

    usage = data.get("usage") or {}

    return {
        "output": data["choices"][0]["message"]["content"],
        "usage": {
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
        },
    }