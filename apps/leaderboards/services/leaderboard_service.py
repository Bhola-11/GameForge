from typing import Dict, Any, List

class RankingEngineService:
    @staticmethod
    def compute_dense_ranks(entries: List[Dict[str, Any]], sort_descending: bool = True) -> List[Dict[str, Any]]:
        sorted_entries = sorted(entries, key=lambda x: x['score'], reverse=sort_descending)
        ranked_list = []
        current_rank = 1
        for idx, entry in enumerate(sorted_entries):
            if idx > 0 and entry['score'] != sorted_entries[idx - 1]['score']:
                current_rank = idx + 1
            e_copy = dict(entry)
            e_copy['rank'] = current_rank
            ranked_list.append(e_copy)
        return ranked_list
