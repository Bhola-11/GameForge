from typing import Dict, Any

class AssetVaultInspectionService:
    @staticmethod
    def validate_polycount_budget(category: str, poly_count: int, target_lod: str = 'LOD0') -> Dict[str, Any]:
        budgets = {
            'HERO_CHARACTER': {'LOD0': 85000, 'LOD1': 45000, 'LOD2': 20000, 'LOD3': 8000},
            'WEAPON': {'LOD0': 25000, 'LOD1': 12000, 'LOD2': 5000, 'LOD3': 1500},
            'VEHICLE': {'LOD0': 150000, 'LOD1': 75000, 'LOD2': 30000, 'LOD3': 10000},
            'ENVIRONMENT_PROP': {'LOD0': 15000, 'LOD1': 7000, 'LOD2': 2500, 'LOD3': 800},
        }
        ref_budget = budgets.get(category, budgets['HERO_CHARACTER']).get(target_lod, 50000)
        is_within = poly_count <= ref_budget
        
        return {
            "target_budget": ref_budget,
            "actual_polys": poly_count,
            "is_within_budget": is_within,
            "overage_percentage": max(0.0, round(((poly_count - ref_budget) / ref_budget) * 100.0, 1))
        }

    @staticmethod
    def validate_texture_resolution(resolution_str: str) -> Dict[str, Any]:
        valid_resolutions = ['512x512', '1024x1024', '2048x2048', '4096x4096', '8192x8192']
        clean_res = resolution_str.strip().lower()
        is_power_of_two = clean_res in [r.lower() for r in valid_resolutions]
        
        return {
            "resolution": resolution_str,
            "is_power_of_two": is_power_of_two,
            "supports_streaming_mipmaps": is_power_of_two,
            "vram_estimate_mb": 21.3 if '4096' in clean_res else (5.3 if '2048' in clean_res else 1.3)
        }
