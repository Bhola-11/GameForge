from typing import Dict, Any, List
import re

class DefectTriageService:
    @staticmethod
    def calculate_bug_severity_priority_matrix(severity: str, platform: str, occurrences_reported: int = 1) -> Dict[str, Any]:
        severity_score = {
            'BLOCKER': 100,
            'CRITICAL': 75,
            'MAJOR': 50,
            'MINOR': 25,
            'TRIVIAL': 10
        }.get(severity, 25)

        platform_multiplier = 1.2 if platform in ['PS5', 'XBOX_SERIES'] else 1.0
        frequency_boost = min(30, occurrences_reported * 5)
        
        total_score = (severity_score * platform_multiplier) + frequency_boost
        
        recommended_priority = "CRITICAL" if total_score >= 90 else ("HIGH" if total_score >= 60 else ("MEDIUM" if total_score >= 35 else "LOW"))

        return {
            "triage_score": round(total_score, 1),
            "recommended_priority": recommended_priority,
            "requires_hotfix": severity in ['BLOCKER', 'CRITICAL'] and platform in ['PS5', 'XBOX_SERIES', 'WIN64']
        }

    @staticmethod
    def parse_and_categorize_callstack(raw_log: str) -> Dict[str, Any]:
        categories = {
            "D3D12": "Graphics / Direct3D 12 Device Hung",
            "Vulkan": "Graphics / Vulkan Memory Crash",
            "NullReference": "Null Pointer Dereference Exception",
            "AccessViolation": "Memory Access Violation (0xC0000005)",
            "Physics": "PhysX / Chaos Physics Collision Blowup",
            "Audio": "XAudio2 / FMOD Audio Buffer Overflow",
        }
        detected = "General Exception / Unknown Crash"
        for key, desc in categories.items():
            if re.search(key, raw_log, re.IGNORECASE):
                detected = desc
                break

        return {
            "crash_signature": detected,
            "has_memory_address": bool(re.search(r"0x[0-9a-fA-F]{8,16}", raw_log)),
            "line_count": len(raw_log.splitlines())
        }
