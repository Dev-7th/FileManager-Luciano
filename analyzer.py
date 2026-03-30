import os
from datetime import datetime


def file_analyzer(path, files):
    file_data = []

    for item in files:
        full_path = os.path.join(path, item)

        if os.path.isfile(full_path):
            name, ext = os.path.splitext(item)
            m_time = os.path.getmtime(full_path)
            date_str = datetime.fromtimestamp(m_time).strftime("%Y-%m-%d")

            file_info = {
                "FileName": item,
                "Name": name,
                "Extension": ext.lower(),
                "Date": date_str
            }
            file_data.append(file_info)
    return file_data
