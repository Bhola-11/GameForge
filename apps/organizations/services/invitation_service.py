import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

class InvitationWorkflowService:
    @staticmethod
    def create_invite_token_payload(email: str, org_id: int, role: str) -> Dict[str, Any]:
        return {
            "token": str(uuid.uuid4()),
            "email": email.strip().lower(),
            "organization_id": org_id,
            "role": role,
            "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
            "is_expired": False
        }

    @staticmethod
    def validate_invite_token(expires_at: datetime, status: str) -> Dict[str, Any]:
        is_active = (status == 'PENDING') and (datetime.now(timezone.utc) <= expires_at)
        return {
            "is_valid": is_active,
            "reason": "OK" if is_active else ("Invitation already used" if status != 'PENDING' else "Invitation token has expired")
        }
