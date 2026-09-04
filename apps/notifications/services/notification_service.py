from typing import Dict, Any, List

class AlertDispatcherService:
    @staticmethod
    def format_discord_webhook_payload(title: str, message: str, alert_level: str = 'INFO') -> Dict[str, Any]:
        colors = {
            'INFO': 3901686,      # Blue
            'SUCCESS': 1096065,   # Green
            'WARNING': 16101131,  # Amber
            'CRITICAL': 15680068, # Red
        }
        return {
            "username": "GameForge Operations Bot",
            "avatar_url": "https://gameforge.io/static/img/bot-avatar.png",
            "embeds": [{
                "title": f"[{alert_level}] {title}",
                "description": message,
                "color": colors.get(alert_level, 3901686),
                "footer": {"text": "GameForge Studio Operations Hub"}
            }]
        }
