import hashlib
import json
from typing import Dict, Any, List

class AuditIntegrityChain:
    @staticmethod
    def generate_log_hash_signature(previous_hash: str, user_id: int, action: str, timestamp_iso: str, payload_json: str) -> str:
        record_block = f"{previous_hash}|{user_id}|{action}|{timestamp_iso}|{payload_json}"
        return hashlib.sha256(record_block.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_audit_chain_integrity(records: List[Dict[str, Any]]) -> Dict[str, Any]:
        prev_hash = "GENESIS_ROOT_HASH_GAMEFORGE_2026"
        tampered_indices = []
        for idx, r in enumerate(records):
            calc = AuditIntegrityChain.generate_log_hash_signature(
                prev_hash,
                r.get('user_id', 0),
                r.get('action', ''),
                r.get('timestamp', ''),
                r.get('payload', '')
            )
            if r.get('hash') and r.get('hash') != calc:
                tampered_indices.append(idx)
            prev_hash = calc

        return {
            "is_valid": len(tampered_indices) == 0,
            "tampered_records": tampered_indices,
            "records_audited": len(records)
        }
