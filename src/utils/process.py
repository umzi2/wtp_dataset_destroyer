import os


def del_all_file(folder: str, file_list: list):
    if len(file_list) > 0:
        for file_name in file_list:
            file_folder = os.path.join(folder, file_name)
            os.remove(file_folder)
