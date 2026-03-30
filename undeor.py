import json
import os
import shutil


def undeor(full_log_path):
    with open(full_log_path, "r") as f:
        moved_data = json.load(f)

    summary_lines = []
    for files in reversed(moved_data):
        current_path = files["new_path"]
        if not os.path.exists(current_path):
            summary_lines.append(
                f"SKIP: {files['filename']} not found (maybe already moved?)")
            continue

        destination_path = files["old_path"]

        try:
            shutil.move(current_path, destination_path)
            summary_lines.append(
                f"SUCCESSFULLY MOVED: Filename: {files['filename']} from: {current_path} to: {destination_path}")

        except Exception as e:
            summary_lines.append(
                f"ERROR: Could not move {files['filename']} - {e}")
    os.remove(full_log_path)
    total_moved = len(summary_lines)
    final_summary = f"Total Files Processed: {total_moved}\n\n" + "\n".join(
        summary_lines)

    return final_summary
