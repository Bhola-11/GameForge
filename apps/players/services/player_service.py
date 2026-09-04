from typing import Dict, Any
import math

class PlayerProgressionService:
    @staticmethod
    def calculate_xp_level_curve(current_xp: int) -> Dict[str, Any]:
        level = int(math.floor(math.sqrt(current_xp / 100.0))) + 1
        xp_for_current = (level - 1) ** 2 * 100
        xp_for_next = level ** 2 * 100
        progress_in_level = current_xp - xp_for_current
        needed_for_next = xp_for_next - xp_for_current
        pct = (progress_in_level / needed_for_next * 100.0) if needed_for_next > 0 else 0.0

        return {
            "calculated_level": level,
            "current_xp": current_xp,
            "xp_in_level": progress_in_level,
            "xp_required_for_next": needed_for_next,
            "level_progress_percentage": round(pct, 1)
        }
