from typing import Dict, Any
from datetime import datetime, timezone, timedelta

class TicketSlaManager:
    @staticmethod
    def compute_sla_breach_status(created_at: datetime, priority: str, is_resolved: bool) -> Dict[str, Any]:
        sla_hours = {
            'CRITICAL': 2,
            'HIGH': 8,
            'MEDIUM': 24,
            'LOW': 48,
        }.get(priority, 24)

        if is_resolved:
            return {"is_breached": False, "remaining_hours": 0, "status": "RESOLVED_ON_TIME"}

        deadline = created_at + timedelta(hours=sla_hours)
        now = datetime.now(timezone.utc)
        is_breached = now > deadline
        rem_hours = round((deadline - now).total_seconds() / 3600.0, 1)

        return {
            "is_breached": is_breached,
            "sla_target_hours": sla_hours,
            "remaining_hours": rem_hours if not is_breached else 0.0,
            "breach_severity": "BREACHED" if is_breached else "IN_SLA"
        }
