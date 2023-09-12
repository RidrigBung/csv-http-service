from typing import List, Tuple, Union


def csv_sort_multiparam(data: List[List[str]], headers_to_sort: List[str]) -> List[List[str]]:
    if len(data) <= 1:
        return data
    headers = data[0]
    rows = data[1:]

    indexes_to_sort, reverse = get_info_how_to_sort(
        headers, headers_to_sort)

    sorted_data = quicksort_multiparam(
        rows, indexes_to_sort, reverse)
    sorted_data.insert(0, headers)
    return sorted_data


def get_info_how_to_sort(headers: List[str], headers_to_sort: List[str]) -> Tuple[Tuple[Union[int, bool]]]:
    indexes_to_sort: List[int] = []
    reverse: List[bool] = []
    for header_to_sort in headers_to_sort:
        if header_to_sort[0] == "-":
            reverse.append(True)
            header_to_sort = header_to_sort[1:]
        else:
            reverse.append(False)
        for index, head in enumerate(headers):
            if head == header_to_sort:
                indexes_to_sort.append(index)
    return tuple((indexes_to_sort, reverse))


def requrcive_compare(row1: List[str], row2: List[str], indexes_to_sort: List[int], reverse: List[bool]) -> int:
    if len(indexes_to_sort) == 0:
        return 2

    # if column with index indexes_to_sort[0] should not be sorted reversed
    if reverse[0]:
        # asc
        if row1[indexes_to_sort[0]] > row2[indexes_to_sort[0]]:
            return 1

        elif row1[indexes_to_sort[0]] == row2[indexes_to_sort[0]]:
            if len(indexes_to_sort) > 1:
                # 1 - row1 < row2, 2 - row1 == row2, 3 - row1 > row2
                return requrcive_compare(
                    row1, row2, indexes_to_sort[1:], reverse[1:])
            # row1 == row2
            return 2

        # row1[indexes_to_sort[0]] < row2[indexes_to_sort[0]]:
        return 3
    else:
        # desc
        if row1[indexes_to_sort[0]] < row2[indexes_to_sort[0]]:
            return 1

        elif row1[indexes_to_sort[0]] == row2[indexes_to_sort[0]]:
            if len(indexes_to_sort) > 1:
                # 1 - row1 < row2, 2 - row1 == row2, 3 - row1 > row2
                return requrcive_compare(
                    row1, row2, indexes_to_sort[1:], reverse[1:])
            # row1 == row2
            return 2

        # row1[indexes_to_sort[0]] > row2[indexes_to_sort[0]]:
        return 3


def quicksort_multiparam(rows: List[List[str]], indexes_to_sort: List[int], reverse: List[bool]) -> List[List[str]]:
    less = []
    equal = []
    greater = []

    if len(rows) > 1:
        pivot = rows[0]
        for row in rows:
            # 1 - row < pivot, 2 - row == pivot, 3 - row > pivot
            compare: int = requrcive_compare(
                row, pivot, indexes_to_sort, reverse)
            if compare == 1:
                less.append(row)
            elif compare == 2:
                equal.append(row)
            else:
                # compare == 3
                greater.append(row)
        return quicksort_multiparam(less, indexes_to_sort, reverse) + equal + quicksort_multiparam(greater, indexes_to_sort, reverse)
    return rows
