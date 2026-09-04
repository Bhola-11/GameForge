from typing import Dict, Any, List

class TelemetryAnalyticsEngine:
    @staticmethod
    def calculate_retention_cohort(installed_users: int, day_1_active: int, day_7_active: int, day_30_active: int) -> Dict[str, Any]:
        d1_pct = (day_1_active / installed_users * 100.0) if installed_users > 0 else 0.0
        d7_pct = (day_7_active / installed_users * 100.0) if installed_users > 0 else 0.0
        d30_pct = (day_30_active / installed_users * 100.0) if installed_users > 0 else 0.0
        
        return {
            "installed_users": installed_users,
            "d1_retention_pct": round(d1_pct, 1),
            "d7_retention_pct": round(d7_pct, 1),
            "d30_retention_pct": round(d30_pct, 1),
            "cohort_benchmark": "HEALTHY" if d1_pct >= 40.0 and d7_pct >= 20.0 else "SUBPAR"
        }

    @staticmethod
    def calculate_p95_p99_frametimes(frametimes_ms: List[float]) -> Dict[str, Any]:
        if not frametimes_ms:
            return {"p50": 16.6, "p95": 16.6, "p99": 16.6, "avg_fps": 60.0}
        s = sorted(frametimes_ms)
        n = len(s)
        p50 = s[int(n * 0.50)]
        p95 = s[min(n - 1, int(n * 0.95))]
        p99 = s[min(n - 1, int(n * 0.99))]
        avg = sum(s) / float(n)
        return {
            "p50_frametime_ms": round(p50, 2),
            "p95_frametime_ms": round(p95, 2),
            "p99_frametime_ms": round(p99, 2),
            "avg_fps": round(1000.0 / avg, 1) if avg > 0 else 0.0,
            "has_stutter_hitch": p99 > 33.3
        }
