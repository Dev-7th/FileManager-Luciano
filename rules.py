def file_rules(processed_list):

    for files in processed_list:

        if files["Extension"] in [".jpg", ".png", ".jpeg", ".gif"]:
            category_key = "Images"

        elif files["Extension"] in [".pdf", ".docx", ".txt", ".pptx", ".xlsx"]:
            category_key = "Documents"

        elif files["Extension"] in [".mp3", ".wav"]:
            category_key = "Audio"

        elif files["Extension"] in [".mp4", ".mkv", ".mov"]:
            category_key = "Video"

        elif files["Extension"] in [".zip", ".rar"]:
            category_key = "Archive"

        else:
            category_key = "Others"

        files["category"] = category_key

    return processed_list
