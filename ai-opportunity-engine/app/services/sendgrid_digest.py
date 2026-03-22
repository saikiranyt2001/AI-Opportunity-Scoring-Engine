import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.digest_dispatch import DigestDispatch


def render_weekly_digest(opportunities: list[dict[str, object]]) -> str:
    lines = ["<h1>Weekly Opportunity Digest</h1>", "<ul>"]
    for item in opportunities:
        lines.append(
            f"<li>{item['product']}: score {item['score']}</li>"
        )
    lines.append("</ul>")
    return "".join(lines)


async def send_weekly_digest(
    to_email: str,
    subject: str,
    html: str,
    api_key: str,
    session: AsyncSession | None = None,
) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": "digest@dealqx.example"},
        "subject": subject,
        "content": [{"type": "text/html", "value": html}],
    }

    provider_message_id = ""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=payload,
            headers=headers,
        )
        if response.status_code not in (200, 202):
            raise RuntimeError("SendGrid request failed")
        provider_message_id = response.headers.get("X-Message-Id", "")

    if session is not None:
        session.add(
            DigestDispatch(
                subscriber_email=to_email,
                subject=subject,
                status="sent",
                provider_message_id=provider_message_id,
            )
        )
        await session.commit()

    return {
        "status": "sent",
        "provider_message_id": provider_message_id,
    }
