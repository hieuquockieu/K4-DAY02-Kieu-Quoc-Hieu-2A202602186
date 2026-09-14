import json

with open("/Users/kieuquochieu/Downloads/day2_detection_quality_schemafix.ipynb", "r") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell.get("source", []))
        if "cross-iou-comparison" in cell.get("id", "") or "audit-comparison-export" in cell.get("id", "") or "cross_iou_comparison" in source or "audit_comparison_export" in source or "5c" in source or "5b" in source:
            print(f"--- Cell ID: {cell.get('id', 'N/A')} ---")
            for output in cell.get("outputs", []):
                if output.get("output_type") == "stream":
                    print(output.get("text", []))
                elif output.get("output_type") == "execute_result" or output.get("output_type") == "display_data":
                    if "text/plain" in output.get("data", {}):
                        print(output["data"]["text/plain"])
                    if "application/json" in output.get("data", {}):
                        print(output["data"]["application/json"])
