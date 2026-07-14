from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from . import constants
from .http_tls import default_https_context

# Discord/Cloudflare often returns 403 for the default Python-urllib User-Agent.
_USER_AGENT = (
    f"WindroseServerManager/{constants.APP_VERSION} "
    "(+https://github.com/Andrew1175/Windrose-Server-Manager-Enhanced)"
)

def is_valid_discord_webhook_url(url: str) -> bool:
    u = (url or "").strip()
    if not u or len(u) > 2048:
        return False
    try:
        parsed = urlparse(u)
    except ValueError:
        return False
    if parsed.scheme != "https":
        return False
    if parsed.netloc.lower() not in ("discord.com", "discordapp.com"):
        return False
    return parsed.path.startswith("/api/webhooks/")


def _read_error_body(err: HTTPError) -> str:
    try:
        raw = err.read(4096)
    except OSError:
        return ""
    if not raw:
        return ""
    try:
        text = raw.decode("utf-8", errors="replace").strip()
    except OSError:
        return ""
    if not text:
        return ""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return text[:500]
    message = parsed.get("message")
    code = parsed.get("code")
    if message and code:
        return f"{message} (Discord code {code})"
    if message:
        return str(message)
    return text[:500]


def send_discord_webhook(url: str, content: str, timeout: float = 12.0) -> tuple[bool, str]:
    """POST plain text content to a Discord webhook. Returns (success, error_detail)."""
    text = (content or "").strip() or "(empty)"
    if len(text) > 2000:
        text = text[:1997] + "..."
    # Without this, <@id> in content is shown as text but may not actually notify the user/role.
    # https://discord.com/developers/docs/resources/channel#allowed-mentions-object
    payload: dict = {
        "content": text,
        "allowed_mentions": {
            "parse": ["users", "roles"],
        },
    }
    body = json.dumps(payload).encode("utf-8")
    req = Request(
        url.strip(),
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": _USER_AGENT,
            "Accept": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=timeout, context=default_https_context()) as resp:
            if 200 <= resp.status < 300:
                return True, ""
            return False, f"HTTP {resp.status}"
    except HTTPError as e:
        detail = _read_error_body(e)
        return False, f"HTTP {e.code}: {detail}" if detail else f"HTTP {e.code}"
    except URLError as e:
        reason = e.reason if isinstance(e.reason, str) else getattr(e.reason, "strerror", str(e.reason))
        return False, reason or "connection error"
    except OSError as e:
        return False, str(e) or "I/O error"
