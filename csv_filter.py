from typing import List, Tuple, Union


def csv_filter_func(data: List[List[str]], headers_to_sort: List[str]) -> List[List[str]]:
    if len(data) <= 1:
        return data

    headers = data[0]
    indexes_to_filter: List[int] = []
    for index, header in enumerate(headers):
        if header in headers_to_sort:
            indexes_to_filter.append(index)

    filtered_data: List[List[str]] = []
    for row in data:
        row = [value for index, value in enumerate(
            row) if index in indexes_to_filter]
        filtered_data.append(row)
    return filtered_data
