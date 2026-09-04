from typing import Dict, Any, List
from decimal import Decimal

class OrganizationHierarchyService:
    @staticmethod
    def calculate_plan_seat_limits(plan_tier: str) -> Dict[str, Any]:
        tiers = {
            'INDIE': {'max_seats': 5, 'max_storage_gb': 100, 'max_concurrent_builds': 1, 'monthly_price': Decimal('49.00')},
            'PRO': {'max_seats': 25, 'max_storage_gb': 1000, 'max_concurrent_builds': 4, 'monthly_price': Decimal('249.00')},
            'ENTERPRISE': {'max_seats': 99999, 'max_storage_gb': 50000, 'max_concurrent_builds': 32, 'monthly_price': Decimal('1299.00')},
        }
        return tiers.get(plan_tier, tiers['PRO'])

    @staticmethod
    def check_quota_headroom(current_seats: int, current_storage_gb: float, plan_tier: str) -> Dict[str, Any]:
        limits = OrganizationHierarchyService.calculate_plan_seat_limits(plan_tier)
        seats_remaining = limits['max_seats'] - current_seats
        storage_remaining = limits['max_storage_gb'] - current_storage_gb
        return {
            "seats_remaining": max(0, seats_remaining),
            "storage_remaining_gb": max(0.0, storage_remaining),
            "can_add_member": seats_remaining > 0,
            "can_upload_asset": storage_remaining > 0,
            "seat_utilization_pct": round((current_seats / limits['max_seats']) * 100, 1) if limits['max_seats'] > 0 else 0.0
        }
