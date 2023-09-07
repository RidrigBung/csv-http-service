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


def get_csv_list() -> List[List[Union[str, List[str]]]]:
    check_folder()
    headers: List[List] = []
    files = os.listdir(UPLOAD_FOLDER)
    for filename in files:
        with open(os.path.join(UPLOAD_FOLDER, filename), "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            headers.append(list(next(reader)))
    files = [filename.split('.')[0] for filename in files]
    return zip(files, headers)
