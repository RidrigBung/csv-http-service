import os
import csv
from typing import List, Union
from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


def is_allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def check_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)


def get_csv_list() -> List[Union[str, List[str]]]:
    headers: List[List[str]] = []
    check_folder()
    files = os.listdir(UPLOAD_FOLDER)
    for filename in files:
        with open(os.path.join(UPLOAD_FOLDER, filename), encoding='utf-8') as csvfile:
            print(os.path.join(UPLOAD_FOLDER, filename))
            try:
                reader = csv.reader(csvfile, delimiter=',')
                headers.append(list(next(reader)))
            except StopIteration:
                headers.append([])
    files = [filename.split('.')[0] for filename in files]
    return zip(files, headers)


def get_csv_file_data(filename: str) -> List[List[str]]:
    data = []
    with open(os.path.join(UPLOAD_FOLDER, filename), encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
    return data


def is_exists(filename: str) -> bool:
    check_folder()
    files = os.listdir(UPLOAD_FOLDER)
    for file in files:
        if file == filename:
            return True
    return False
