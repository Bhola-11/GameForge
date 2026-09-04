import hashlib
import secrets
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationService:
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        score = 0
        feedback = []
        if len(password) >= 8:
            score += 25
        else:
            feedback.append("Password must be at least 8 characters long.")
        if any(c.isupper() for c in password):
            score += 25
        else:
            feedback.append("Include at least one uppercase letter.")
        if any(c.isdigit() for c in password):
            score += 25
        else:
            feedback.append("Include at least one numeric digit.")
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 25
        else:
            feedback.append("Include at least one special character.")

        return {
            "score": score,
            "is_valid": score >= 75,
            "feedback": feedback,
            "strength_tier": "STRONG" if score >= 100 else ("MEDIUM" if score >= 75 else "WEAK")
        }

    @staticmethod
    def generate_session_token(user_id: int, salt: Optional[str] = None) -> str:
        salt_val = salt or secrets.token_hex(16)
        payload = f"{user_id}:{datetime.now(timezone.utc).timestamp()}:{salt_val}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    @staticmethod
    def calculate_session_expiry(remember_me: bool = False) -> datetime:
        days = 30 if remember_me else 1
        return datetime.now(timezone.utc) + timedelta(days=days)

    @staticmethod
    def check_brute_force_lockout(failed_attempts: int, last_attempt_time: Optional[datetime]) -> Dict[str, Any]:
        if failed_attempts >= 5:
            if last_attempt_time:
                cooldown_expiry = last_attempt_time + timedelta(minutes=15)
                if datetime.now(timezone.utc) < cooldown_expiry:
                    remaining_seconds = int((cooldown_expiry - datetime.now(timezone.utc)).total_seconds())
                    return {
                        "is_locked": True,
                        "remaining_lockout_seconds": remaining_seconds,
                        "message": f"Account temporarily locked. Retry in {remaining_seconds // 60} minutes."
                    }
        return {"is_locked": False, "remaining_lockout_seconds": 0, "message": "OK"}
