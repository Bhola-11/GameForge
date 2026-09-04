import json
import csv
import io
from typing import Dict, Any, List

class ExecutiveReportExporter:
    @staticmethod
    def export_dataset_to_csv_string(headers: List[str], rows: List[List[Any]]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        for r in rows:
            writer.writerow(r)
        return output.getvalue()

    @staticmethod
    def format_json_summary_package(metrics: Dict[str, Any]) -> str:
        return json.dumps(metrics, indent=2, default=str)
