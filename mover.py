import os
import shutil
from datetime import datetime
import json


def mover_func(original_path, processed_list):

    summary_lines = []
    history_data = []
    for files in processed_list:
        year = files["Date"].split("-")[0]
        month = datetime.strptime(files["Date"], "%Y-%m-%d").strftime("%B")
        current_path = os.path.join(original_path, files["FileName"])
        if not os.path.exists(current_path):
            summary_lines.append(
                f"SKIP: {files['FileName']} not found (maybe already moved?)")
            continue
        category_folder = os.path.join(
            original_path, files["category"], year, month)

        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        destination_path = os.path.join(category_folder, files["FileName"])

        try:
            shutil.move(current_path, destination_path)
            summary_lines.append(
                f"SUCCESS: Moved {files['FileName']} to {files['category']} - {year} - {month}")

            before_after_log = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": files["FileName"],
                "old_path": current_path,
                "new_path": destination_path
            }
            history_data.append(before_after_log)

        except Exception as e:
            summary_lines.append(
                f"ERROR: Could not move {files['FileName']} - {e}")

    total_moved = len(summary_lines)
    final_summary = f"Total Files Processed: {total_moved}\n\n" + "\n".join(
        summary_lines)

    with open(f"history-log/history{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json", "w") as f:
        json.dump(history_data, f, indent=4)

    return final_summary
