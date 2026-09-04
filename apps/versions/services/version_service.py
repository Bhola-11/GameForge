import re
from typing import Dict, Any, Optional

class SemVerEngine:
    @staticmethod
    def parse_semver(version_str: str) -> Dict[str, Any]:
        pattern = r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:-(?P<prerelease>[a-zA-Z0-9.-]+))?$"
        match = re.match(pattern, version_str.strip())
        if not match:
            return {"is_valid": False, "major": 0, "minor": 0, "patch": 0, "prerelease": None}
        
        gd = match.groupdict()
        return {
            "is_valid": True,
            "major": int(gd['major']),
            "minor": int(gd['minor']),
            "patch": int(gd['patch']),
            "prerelease": gd['prerelease'],
            "is_production_ready": gd['prerelease'] is None and int(gd['major']) >= 1
        }

    @staticmethod
    def compare_versions(ver_a: str, ver_b: str) -> int:
        p_a = SemVerEngine.parse_semver(ver_a)
        p_b = SemVerEngine.parse_semver(ver_b)
        if not p_a['is_valid'] or not p_b['is_valid']:
            return 0
        tuple_a = (p_a['major'], p_a['minor'], p_a['patch'])
        tuple_b = (p_b['major'], p_b['minor'], p_b['patch'])
        if tuple_a < tuple_b:
            return -1
        elif tuple_a > tuple_b:
            return 1
        return 0
