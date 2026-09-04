import uuid
import hmac
import hashlib
from typing import Dict, Any

class ApiKeyService:
    @staticmethod
    def generate_api_key_pair(user_id: int) -> Dict[str, str]:
        public_id = f"gf_live_{uuid.uuid4().hex[:16]}"
        secret_key = f"gfk_{uuid.uuid4().hex}{uuid.uuid4().hex}"
        return {
            "public_key": public_id,
            "secret_key": secret_key,
            "masked_key": f"{public_id[:8]}...{public_id[-4:]}"
        }

    @staticmethod
    def verify_request_signature(secret: str, payload: str, signature: str) -> bool:
        expected = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
