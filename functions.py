import os
import csv
import json
import pandas as pd
from typing import List, Tuple, Union
from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, DELIMITERS_STORAGE


def is_allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def check_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if not os.path.exists(DELIMITERS_STORAGE):
        open(DELIMITERS_STORAGE, 'a').close()


def get_csv_list() -> Tuple[Union[str, List[List[str]], str]]:
    headers: List[List[str]] = []
    delimiters: List[str] = []
    check_folder()
    files = os.listdir(UPLOAD_FOLDER)
    for filename in files:
        header = get_csv_headers(filename)
        headers.append(header)
        delimiter = get_delimiter(filename)
        delimiters.append(delimiter)
    files = (filename.split('.')[0] for filename in files)
    return zip(files, headers, delimiters)


def get_csv_file_data(filename: str, headers_to_sort: List[str], headers_to_filter: List[str]) -> Tuple[Union[List[List[str]], str]]:
    # if headers_to_filter is not empty
    if headers_to_filter != [""]:
        file_df = pd.read_csv(os.path.join(
            UPLOAD_FOLDER, filename), usecols=headers_to_filter)
    else:
        file_df = pd.read_csv(os.path.join(
            UPLOAD_FOLDER, filename))
    # if headers_to_sort is not empty
    if headers_to_sort != [""]:
        ascendings: List[bool] = []
        clean_headers_to_filter: List[str] = []
        for header in headers_to_filter:
            if header[0] == "-":
                ascendings.append(True)
                clean_headers_to_filter.append(header[1:])
            else:
                ascendings.append(False)
                clean_headers_to_filter.append(header)
        file_df.sort(clean_headers_to_filter,
                     ascending=ascendings)
    file_head = file_df.columns.tolist()
    file_body = file_df.values.tolist()
    file_data = file_head + file_body

    print(file_data)
    data = (file_data, get_delimiter(filename))
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


def delete_delimiter(filename: str) -> None:
    with open(DELIMITERS_STORAGE, "r") as json_file:
        # if file DELIMITERS_STORAGE is empty
        if os.stat(DELIMITERS_STORAGE).st_size == 0:
            file_data = []
        else:
            file_data = list(json.load(json_file))
            f_index = 0
            for index, file in enumerate(file_data):
                if list(file.keys())[0] == filename:
                    f_index = index
                    break

    file_data.pop(f_index)
    with open(DELIMITERS_STORAGE, "w") as json_file:
        json.dump(file_data, json_file, indent=4)


def delete_csv_file_data(filename: str) -> None:
    if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        delete_delimiter(filename)


def get_csv_headers(filename: str) -> List[str]:
    headers = []
    with open(os.path.join(UPLOAD_FOLDER, filename), encoding='utf-8') as csv_file:
        try:
            delimiter = get_delimiter(filename)
            reader = csv.reader(
                csv_file, delimiter=delimiter)
            headers = list(next(reader))
        except StopIteration:
            # file is empty
            pass
    return headers


def is_correct_header_list(filename: str, form_headers: List[str]) -> bool:
    form_headers = form_headers.split(" ")
    if form_headers == [""]:
        return True
    headers = get_csv_headers(filename)
    for head in form_headers:
        if head[0] == "-":
            head = head[1:]
        if head not in headers:
            return False
    return True
