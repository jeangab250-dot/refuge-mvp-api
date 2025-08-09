
import os
from typing import Optional
from twilio.rest import Client

ENABLED = os.getenv("NOTIFICATIONS_ENABLED", "false").lower() == "true"
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
FROM_SMS = os.getenv("TWILIO_FROM_SMS", "")
FROM_WA = os.getenv("TWILIO_FROM_WHATSAPP", "")

_client: Optional[Client] = None

def _get_client() -> Optional[Client]:
    global _client
    if not ENABLED:
        return None
    if _client is None and ACCOUNT_SID and AUTH_TOKEN:
        _client = Client(ACCOUNT_SID, AUTH_TOKEN)
    return _client

def send_sms(to: str, body: str) -> bool:
    client = _get_client()
    if not client or not FROM_SMS or not to:
        return False
    try:
        client.messages.create(from_=FROM_SMS, to=to, body=body)
        return True
    except Exception:
        return False

def send_whatsapp(to: str, body: str) -> bool:
    client = _get_client()
    if not client or not FROM_WA or not to:
        return False
    try:
        if not to.startswith("whatsapp:"):
            to = "whatsapp:" + to
        client.messages.create(from_=FROM_WA, to=to, body=body)
        return True
    except Exception:
        return False
