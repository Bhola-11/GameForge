from typing import Dict, Any, List

class TeamAllocationService:
    @staticmethod
    def calculate_squad_capacity_matrix(members: List[Dict[str, Any]], working_hours_per_week: float = 40.0) -> Dict[str, Any]:
        total_nominal_hours = 0.0
        effective_capacity_hours = 0.0
        role_breakdown = {}

        for m in members:
            allocation_pct = m.get('allocation_percentage', 100) / 100.0
            member_capacity = working_hours_per_week * allocation_pct
            nominal = working_hours_per_week
            total_nominal_hours += nominal
            effective_capacity_hours += member_capacity

            role = m.get('role_in_team', 'Developer')
            role_breakdown[role] = role_breakdown.get(role, 0.0) + member_capacity

        return {
            "total_members": len(members),
            "total_nominal_hours": total_nominal_hours,
            "effective_capacity_hours": effective_capacity_hours,
            "capacity_factor": round(effective_capacity_hours / total_nominal_hours, 2) if total_nominal_hours > 0 else 1.0,
            "role_capacity_hours": role_breakdown
        }

    @staticmethod
    def detect_workload_overload(capacity_hours: float, booked_hours: float) -> Dict[str, Any]:
        burnout_risk = False
        utilization = (booked_hours / capacity_hours * 100.0) if capacity_hours > 0 else 0.0
        if utilization > 115.0:
            burnout_risk = True
            risk_level = "CRITICAL"
        elif utilization > 100.0:
            burnout_risk = True
            risk_level = "HIGH"
        elif utilization > 80.0:
            risk_level = "OPTIMAL"
        else:
            risk_level = "UNDERUTILIZED"

        return {
            "utilization_percentage": round(utilization, 1),
            "burnout_risk": burnout_risk,
            "risk_level": risk_level,
            "surplus_or_deficit_hours": round(capacity_hours - booked_hours, 1)
        }
