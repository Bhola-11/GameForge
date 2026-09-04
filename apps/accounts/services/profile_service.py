from typing import Dict, Any, List
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileService:
    @staticmethod
    def compute_developer_profile_completeness(user: Any) -> Dict[str, Any]:
        fields = [
            ('first_name', 10),
            ('last_name', 10),
            ('email', 15),
            ('job_title', 15),
            ('department', 10),
            ('bio', 15),
            ('github_handle', 10),
            ('discord_tag', 10),
            ('avatar', 5),
        ]
        completed_score = 0
        missing_fields = []
        for field, weight in fields:
            val = getattr(user, field, None)
            if val:
                completed_score += weight
            else:
                missing_fields.append(field)

        return {
            "percentage": completed_score,
            "missing_fields": missing_fields,
            "badge": "PRO" if completed_score >= 80 else ("STANDARD" if completed_score >= 50 else "INCOMPLETE")
        }

    @staticmethod
    def get_role_hierarchy_level(role: str) -> int:
        hierarchy = {
            User.Role.SUPER_ADMIN: 100,
            User.Role.ORG_ADMIN: 90,
            User.Role.PROJECT_MANAGER: 80,
            User.Role.LEAD_DEVELOPER: 75,
            User.Role.DEVELOPER: 50,
            User.Role.DESIGNER: 50,
            User.Role.QA_TESTER: 45,
            User.Role.MARKETING_MANAGER: 40,
            User.Role.SUPPORT_AGENT: 35,
            User.Role.VIEWER: 10,
        }
        return hierarchy.get(role, 0)
