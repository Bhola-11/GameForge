from typing import Dict, Any, List
from decimal import Decimal

class GameEngineProfileService:
    @staticmethod
    def get_recommended_target_framerate(engine: str, platform: str) -> Dict[str, Any]:
        profiles = {
            'UNREAL_5': {
                'PS5': {'target_fps': 60, 'resolution': '1440p dynamic (Lumen + Nanite)', 'preset': 'Performance'},
                'XBOX_SERIES': {'target_fps': 60, 'resolution': '1440p dynamic (Lumen + Nanite)', 'preset': 'Performance'},
                'WIN64': {'target_fps': 120, 'resolution': '4K Native / DLSS 3.5 Frame Gen', 'preset': 'Epic'},
                'NINTENDO_SWITCH': {'target_fps': 30, 'resolution': '720p Mobile Docked', 'preset': 'Low'},
            },
            'UNITY_6': {
                'PS5': {'target_fps': 60, 'resolution': '4K Native URP', 'preset': 'High'},
                'WIN64': {'target_fps': 144, 'resolution': '4K Native HDR', 'preset': 'Ultra'},
                'NINTENDO_SWITCH': {'target_fps': 60, 'resolution': '1080p Docked', 'preset': 'Medium'},
            },
            'GODOT_4': {
                'WIN64': {'target_fps': 144, 'resolution': '4K Vulkan Renderer', 'preset': 'Ultra'},
                'LINUX_X64': {'target_fps': 90, 'resolution': '1280x800 Steam Deck', 'preset': 'Medium'},
            }
        }
        engine_data = profiles.get(engine, profiles['UNREAL_5'])
        return engine_data.get(platform, {'target_fps': 60, 'resolution': '1080p', 'preset': 'Standard'})

    @staticmethod
    def compute_milestone_critical_path(milestones: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_milestones = len(milestones)
        completed = sum(1 for m in milestones if m.get('is_completed', False))
        completion_rate = (completed / total_milestones * 100.0) if total_milestones > 0 else 0.0
        
        return {
            "total_milestones": total_milestones,
            "completed_milestones": completed,
            "completion_rate_pct": round(completion_rate, 1),
            "production_phase": "GOLD_MASTER" if completion_rate == 100.0 else ("BETA" if completion_rate >= 75.0 else "ALPHA")
        }
