import os
import csv
import json
from typing import List, Union
from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, DELIMITERS_STORAGE


def is_allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def check_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if not os.path.exists(DELIMITERS_STORAGE):
        open(DELIMITERS_STORAGE, 'a').close()


def get_csv_list() -> List[Union[str, List[List[str]], str]]:
    headers: List[List[str]] = []
    delimiters: List[str] = []
    check_folder()
    files = os.listdir(UPLOAD_FOLDER)
    for filename in files:
        with open(os.path.join(UPLOAD_FOLDER, filename), encoding='utf-8') as csv_file:
            try:
                delimiter = get_delimiter(filename)
                reader = csv.reader(
                    csv_file, delimiter=delimiter)
                headers.append(list(next(reader)))
                delimiters.append(delimiter)
            except StopIteration:
                # file is empty
                headers.append([])
                delimiters.append("")
    files = [filename.split('.')[0] for filename in files]
    return zip(files, headers, delimiters)


def get_csv_file_data(filename: str) -> List[List[str]]:
    data = []
    with open(os.path.join(UPLOAD_FOLDER, filename), encoding='utf-8') as csv_file:
        try:
            reader = csv.reader(csv_file, delimiter=get_delimiter(filename))
            data = list(reader)
        except StopIteration:
            # file is empty
            pass
    return data


def is_exists(filename: str) -> bool:
    check_folder()
    files = os.listdir(UPLOAD_FOLDER)
    for file in files:
        if file == filename:
            return True
    return False


def save_delimiter(filename: str, delimiter: str) -> None:
    merge_file_deli = {filename: delimiter}
    with open(DELIMITERS_STORAGE, "r") as json_file:
        # if file DELIMITERS_STORAGE is empty
        if os.stat(DELIMITERS_STORAGE).st_size == 0:
            file_data = []
        else:
            file_data = list(json.load(json_file))

    file_data.append(merge_file_deli)
    with open(DELIMITERS_STORAGE, "w") as json_file:
        json.dump(file_data, json_file, indent=4)


def get_delimiter(filename: str) -> str:
    delimiter = ","
    with open(DELIMITERS_STORAGE, "r") as json_file:
        merges = json.load(json_file)
        for merge in merges:
            i_filename, i_delimiter = list(merge.items())[0]
            if i_filename == filename:
                delimiter = i_delimiter
                break
    return delimiter
