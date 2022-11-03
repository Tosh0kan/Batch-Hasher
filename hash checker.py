import hashlib
from os import walk
from os.path import join


def file_hash(file_path: str):
    h = hashlib.sha256()

    with open(file_path, "rb") as f:
        fb = f.read(64000)
        while len(fb) > 0:
            h.update(fb)
            fb = f.read(64000)

    return h.hexdigest()


def folder_hash(folder_path: str):  # hashes all files in a folder and its subfolders
    hash_filename_pair = {}

    for root, dirs, files in walk(folder_path):
        for name in files:
            path_hash = join(root, name)
            hashed = file_hash(path_hash)
            hash_filename_pair.setdefault(hashed, []).append(name)

    return hash_filename_pair


def dupe_scry(folder_path: str):
    hash_filename_pair = folder_hash(folder_path)

    for key, value in hash_filename_pair.items():
        if len(value) > 1:
            dupe_text = ""
            loop_cnt = 0
            for e in value:
                if loop_cnt != value.index(e):
                    dupe_text += e
                    loop_cnt += 1

                else:
                    dupe_text += e + " and "

            dupe_text += " are dupes."
            print(dupe_text)


if __name__ == "__main__":
    while True:
        mode_choice = input("Do you wish do hash a single file or all files in a folder?").lower()
        if "file" in mode_choice:
            f_user_path = input("What's the file path w/o quotations?")
            f_hash = file_hash(f_user_path)
            print(f_hash)

        elif "folder" in mode_choice:
            f_user_path = input("What's the folder path w/o quotations?")

            comp_input = input("Do you wish to look for dupes?").lower()
            if "no" in comp_input:
                folder_results = folder_hash(f_user_path)
                for key, value in folder_results.items():
                    for e in value:
                        print(e, " / ", key)

            elif "yes" in comp_input:
                folder_results = folder_hash(f_user_path)
                for key, value in folder_results.items():
                    for e in value:
                        print(e, " / ", key)

                dupe_scry(f_user_path)

        else:
            quit()
