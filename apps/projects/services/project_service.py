from typing import Dict, Any, List
from decimal import Decimal

class ProjectHealthService:
    @staticmethod
    def calculate_budget_burn_rate(allocated_budget: Decimal, total_logged_hours: float, hourly_rate_usd: float = 75.0) -> Dict[str, Any]:
        consumed_budget = Decimal(str(total_logged_hours * hourly_rate_usd))
        remaining_budget = allocated_budget - consumed_budget
        burn_pct = float(consumed_budget / allocated_budget * 100) if allocated_budget > 0 else 0.0

        return {
            "allocated_budget": float(allocated_budget),
            "consumed_budget": float(consumed_budget),
            "remaining_budget": float(remaining_budget),
            "burn_percentage": round(burn_pct, 1),
            "is_over_budget": remaining_budget < 0,
            "budget_health": "NOMINAL" if burn_pct <= 85.0 else ("WARNING" if burn_pct <= 100.0 else "CRITICAL_DEFICIT")
        }

    @staticmethod
    def evaluate_risk_contingency(risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        impact_weights = {'LOW': 1, 'MED': 3, 'HIGH': 6, 'CRITICAL': 10}
        prob_weights = {'LOW': 1, 'MED': 2, 'HIGH': 3}
        
        total_risk_score = 0
        unresolved_count = 0
        
        for r in risks:
            if not r.get('is_resolved', False):
                unresolved_count += 1
                imp = impact_weights.get(r.get('impact', 'MED'), 3)
                prb = prob_weights.get(r.get('probability', 'MED'), 2)
                total_risk_score += (imp * prb)

        return {
            "unresolved_risks_count": unresolved_count,
            "aggregate_risk_score": total_risk_score,
            "composite_risk_rating": "STABLE" if total_risk_score < 15 else ("ELEVATED" if total_risk_score < 40 else "CRITICAL")
        }
