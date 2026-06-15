from __future__ import annotations

import json
import os
from urllib import error, request


def _offline_response(question: str) -> str:
    return (
        "AI Copilot (Offline Mode): Set `OPENROUTER_API_KEY` or `COPILOT_API_KEY` "
        "to enable live answers.\n\n"
        f"Recommendation: For your query '{question}', check current machine health "
        "metrics (93%) and the positive trend in revenue forecasts ($1.2M)."
    )


def ask_copilot(question):
    api_key = (
        os.getenv("OPENROUTER_API_KEY")
        or os.getenv("COPILOT_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    )
    if not api_key:
        return _offline_response(question)

    if os.getenv("GEMINI_API_KEY") and not os.getenv("OPENROUTER_API_KEY") and not os.getenv("COPILOT_API_KEY"):
        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(question)
            return response.text
        except Exception as exc:
            return f"AI Copilot: Gemini error ({exc})."

    payload = {
        "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a concise decision support copilot for a business analytics dashboard."
                ),
            },
            {"role": "user", "content": question},
        ],
    }

    req = request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
            "X-Title": os.getenv("OPENROUTER_APP_NAME", "Self-Learning AI Decision Support Ecosystem"),
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        choices = data.get("choices") or []
        if choices:
            message = choices[0].get("message") or {}
            content = message.get("content")
            if content:
                return content.strip()
        return _offline_response(question)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        return f"AI Copilot: OpenRouter HTTP error {exc.code}. {body}".strip()
    except Exception as exc:
        return f"AI Copilot: OpenRouter error ({exc})."
