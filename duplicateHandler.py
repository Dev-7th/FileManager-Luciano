import os
import hashlib


def file_hash(path):
    hash_obj = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


folder = "C:/Users/ralph/Downloads"
hashes = {}
file_sizes = {}
for root, dirs, files in os.walk(folder, topdown=False):
    for file in files:
        fullpath = os.path.join(root, file)
        current_file_size = os.path.getsize(fullpath)
        if (current_file_size in file_sizes):

            h = file_hash(fullpath)
            first_file_path = file_sizes[current_file_size]

            if (first_file_path not in hashes.values()):
                h_first = file_hash(first_file_path)
                hashes[h_first] = first_file_path

            if h in hashes:
                print("Duplicate file has found")
                print(fullpath, "==", hashes[h])
            else:
                hashes[h] = fullpath

        else:
            file_sizes[current_file_size] = fullpath

    if (len(dirs) == 0 and len(files) == 0):
        try:
            os.rmdir(root)
            print(f"Folder: {root} deleted successfully.")
        except FileNotFoundError:
            print("Folder not found.")
        except OSError as e:
            print(f"Error: {e.strerror}. The folder might not be empty.")
