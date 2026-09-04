from typing import Dict, Any
from decimal import Decimal

class VirtualEconomyEngine:
    @staticmethod
    def calculate_arpu_and_ltv(total_revenue: Decimal, total_players: int, paying_players: int) -> Dict[str, Any]:
        arpu = (float(total_revenue) / float(total_players)) if total_players > 0 else 0.0
        arppu = (float(total_revenue) / float(paying_players)) if paying_players > 0 else 0.0
        payer_conversion_pct = (paying_players / total_players * 100.0) if total_players > 0 else 0.0

        return {
            "arpu_usd": round(arpu, 2),
            "arppu_usd": round(arppu, 2),
            "payer_conversion_pct": round(payer_conversion_pct, 2),
            "gross_revenue": float(total_revenue)
        }
