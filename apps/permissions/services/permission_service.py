from typing import Dict, Any, List
from apps.accounts.models import User

class RbacPolicyEngine:
    @staticmethod
    def evaluate_user_action_permission(user_role: str, module: str, action: str) -> bool:
        if user_role == User.Role.SUPER_ADMIN:
            return True
        if user_role == User.Role.ORG_ADMIN:
            return True
        if user_role == User.Role.PROJECT_MANAGER:
            return action in ['view', 'create', 'edit', 'approve']
        if user_role in [User.Role.LEAD_DEVELOPER, User.Role.DEVELOPER]:
            if module in ['games', 'projects', 'tasks', 'bugs', 'builds', 'assets', 'versions']:
                return action in ['view', 'create', 'edit']
            return action == 'view'
        if user_role == User.Role.QA_TESTER:
            if module in ['bugs', 'builds', 'tasks']:
                return action in ['view', 'create', 'edit']
            return action == 'view'
        if user_role == User.Role.DESIGNER:
            if module in ['assets', 'tasks', 'games']:
                return action in ['view', 'create', 'edit']
            return action == 'view'
        if user_role == User.Role.VIEWER:
            return action == 'view'
        return action == 'view'
