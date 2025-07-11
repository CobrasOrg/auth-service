from typing import Dict
from datetime import datetime, timezone

class RevokedTokenStore:
    def __init__(self):
        self.revoked_tokens: Dict[str, datetime] = {}

    def revoke(self, token: str, expires_at: datetime):
        self.revoked_tokens[token] = expires_at

    def is_revoked(self, token: str) -> bool:
        now = datetime.now(timezone.utc)
        if token in self.revoked_tokens:
            if self.revoked_tokens[token] > now:
                return True
            else:
                del self.revoked_tokens[token]
        return False

    def reset(self):
        self.revoked_tokens.clear()

revoked_store = RevokedTokenStore()