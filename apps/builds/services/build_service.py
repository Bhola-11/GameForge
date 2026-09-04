from typing import Dict, Any
from decimal import Decimal

class BuildPipelineService:
    @staticmethod
    def calculate_binary_compression_efficiency(uncompressed_size_mb: float, compressed_package_mb: float) -> Dict[str, Any]:
        ratio = (compressed_package_mb / uncompressed_size_mb) if uncompressed_size_mb > 0 else 1.0
        savings_pct = (1.0 - ratio) * 100.0
        
        return {
            "uncompressed_mb": uncompressed_size_mb,
            "package_mb": compressed_package_mb,
            "compression_ratio": round(ratio, 3),
            "bandwidth_savings_pct": round(savings_pct, 1),
            "patcher_streamable": ratio <= 0.65
        }

    @staticmethod
    def evaluate_smoke_test_pass_criteria(failed_test_count: int, blocker_bug_count: int, platform: str) -> Dict[str, Any]:
        can_certify = (failed_test_count == 0) and (blocker_bug_count == 0)
        return {
            "platform": platform,
            "can_pass_certification": can_certify,
            "status": "APPROVED" if can_certify else "REJECTED",
            "reason": "All smoke and cert checks passed" if can_certify else f"Found {failed_test_count} failed tests and {blocker_bug_count} blockers"
        }
