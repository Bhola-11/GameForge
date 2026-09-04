from typing import Dict, Any, List

class KanbanWorkflowService:
    @staticmethod
    def validate_state_transition(current_status: str, target_status: str) -> Dict[str, Any]:
        valid_transitions = {
            'BACKLOG': ['TODO', 'CANCELLED'],
            'TODO': ['IN_PROGRESS', 'BACKLOG', 'CANCELLED'],
            'IN_PROGRESS': ['REVIEW', 'TODO', 'CANCELLED'],
            'REVIEW': ['TESTING', 'IN_PROGRESS'],
            'TESTING': ['COMPLETED', 'IN_PROGRESS'],
            'COMPLETED': ['TODO', 'IN_PROGRESS'],
            'CANCELLED': ['BACKLOG', 'TODO'],
        }
        allowed = valid_transitions.get(current_status, [])
        is_valid = target_status in allowed
        
        return {
            "is_valid": is_valid,
            "current_status": current_status,
            "target_status": target_status,
            "allowed_next_states": allowed
        }

    @staticmethod
    def calculate_sprint_velocity(completed_story_hours: float, sprint_duration_days: int = 14) -> Dict[str, Any]:
        daily_velocity = completed_story_hours / float(sprint_duration_days) if sprint_duration_days > 0 else 0.0
        return {
            "total_hours_delivered": completed_story_hours,
            "sprint_days": sprint_duration_days,
            "daily_velocity_hours": round(daily_velocity, 2),
            "estimated_next_sprint_capacity": round(daily_velocity * sprint_duration_days, 1)
        }
