from typing import Dict, Any, List

class ReleaseStageGateService:
    @staticmethod
    def verify_all_stage_gates(checklist_items: List[Dict[str, Any]], bug_blockers_count: int) -> Dict[str, Any]:
        total_items = len(checklist_items)
        passed_items = sum(1 for item in checklist_items if item.get('is_completed', False))
        has_blockers = bug_blockers_count > 0
        
        can_release = (passed_items == total_items) and (not has_blockers) and (total_items > 0)
        
        return {
            "can_deploy_to_production": can_release,
            "checklist_passed_count": passed_items,
            "checklist_total_count": total_items,
            "active_blockers": bug_blockers_count,
            "gate_status": "GO_FOR_LAUNCH" if can_release else "HOLD_BLOCKED"
        }
