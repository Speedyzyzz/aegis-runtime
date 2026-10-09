import time
import secrets
from typing import Dict, Optional
from pydantic import BaseModel, Field

class CapabilityToken(BaseModel):
    token: str
    action_id: str
    session_id: str
    scope: str
    expires_at_epoch: float
    consumed: bool = False

class CapabilityTokenManager:
    def __init__(self, default_ttl_seconds: int = 60):
        self.default_ttl = default_ttl_seconds
        self._tokens: Dict[str, CapabilityToken] = {}

    def issue_token(self, action_id: str, session_id: str, scope: str, ttl_seconds: Optional[int] = None) -> CapabilityToken:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        token_str = f"cap_{secrets.token_hex(16)}"
        cap = CapabilityToken(
            token=token_str,
            action_id=action_id,
            session_id=session_id,
            scope=scope,
            expires_at_epoch=time.time() + ttl,
            consumed=False
        )
        self._tokens[token_str] = cap
        return cap

    def validate_and_consume(self, token_str: str, action_id: str, scope: str) -> bool:
        cap = self._tokens.get(token_str)
        if not cap:
            return False
        if cap.consumed:
            return False  # Double-spend prevention
        if time.time() > cap.expires_at_epoch:
            return False  # Expired
        if cap.action_id != action_id or cap.scope != scope:
            return False  # Scope mismatch or parameter tampering

        cap.consumed = True
        return True
