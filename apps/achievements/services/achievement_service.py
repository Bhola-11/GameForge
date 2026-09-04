from typing import Dict, Any, List

class TrophyEngineService:
    @staticmethod
    def compute_gamer_score_tier(unlocked_points: int) -> Dict[str, Any]:
        tiers = [
            (2500, "MYTHIC_LEGEND", "#FFD700"),
            (1500, "DIAMOND_CHAMPION", "#B9F2FF"),
            (800, "PLATINUM_VETERAN", "#E5E4E2"),
            (300, "GOLD_ADEPT", "#F59E0B"),
            (100, "SILVER_APPRENTICE", "#94A3B8"),
            (0, "BRONZE_NOVICE", "#CD7F32"),
        ]
        badge_name, color = "BRONZE_NOVICE", "#CD7F32"
        for thresh, name, clr in tiers:
            if unlocked_points >= thresh:
                badge_name, color = name, clr
                break

        return {
            "points": unlocked_points,
            "tier_badge": badge_name,
            "badge_color": color
        }
