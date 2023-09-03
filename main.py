import numpy as np
from pprint import pprint
from copy import deepcopy

# 初期設定
num = 9  # 一辺の問題のサイズ
num_sqrt = int(np.sqrt(num))  # 一辺の問題のサイズの平方根
num_all_set = set([i + 1 for i in range(num)])  # 1~numの集合


def solve_number_place(number_list, column_list, row_list, area_list):
    possibility_list = deepcopy(
        get_possibility_list(number_list, column_list, row_list, area_list)
    )
    pprint(possibility_list)
    pass


def get_possibility_list(number_list, column_list, row_list, area_list):
    """各マスの候補となる数字の集合が入ったリストを返す

    Args:
        number_list (numpy.array): 数字のリスト
        column_list (list): 各列の候補となる数字の集合が入ったリスト
        row_list (list): 各行の候補となる数字の集合が入ったリスト
        area_list (list): 各エリアの候補となる数字の集合が入ったリスト

    Returns:
        list of list: 各マスの候補となる数字の集合が入ったリスト
    """
    global num_sqrt
    possibility_list = [[set() for _ in range(num)] for _ in range(num)]
    for row in range(num):
        for col in range(num):
            p_num = number_list[row][col]
            if p_num != 0:
                continue
            area_set = set(area_list[row // num_sqrt][col // num_sqrt])
            column_set = set(column_list[col])
            row_set = set(row_list[row])
            possibility_set = area_set.intersection(
                column_set,
                row_set,
            )
            possibility_list[row][col] = possibility_set
    return possibility_list


def set_all_number_list(input_string):
    """数字の文字列をnumpyのリスト型に変換する

    Args:
        input_string (string): 数字の文字列

    Returns:
        numpy.array: 数字のリスト
    """
    return np.array(
        [[int(input_string[num * i + j]) for j in range(num)] for i in range(0, num)]
    )


def get_column_list(number_list):
    """各列の候補となる数字の集合が入ったリストを返す

    Args:
        number_list (numpy.array): 数字のリスト

    Returns:
        list: 各列の候補となる数字の集合が入ったリスト
    """
    column_list = [num_all_set - set(number_list[:, col]) for col in range(num)]
    return column_list


def get_row_list(number_list):
    """各行の候補となる数字の集合が入ったリストを返す

    Args:
        number_list (numpy.array): 数字のリスト

    Returns:
        list: 各行の候補となる数字の集合が入ったリスト
    """
    row_list = [num_all_set - set(number_list[row, :]) for row in range(num)]
    return row_list


def get_area_list(number_list):
    """各エリアの候補となる数字の集合が入ったリストを返す

    Args:
        number_list (numpy.array): 数字のリスト

    Returns:
        list: 各エリアの候補となる数字の集合が入ったリスト
    """
    area_list = [
        [
            num_all_set
            - set(
                list(
                    number_list[
                        row_ * num_sqrt : (row_ + 1) * num_sqrt,
                        col_ * num_sqrt : (col_ + 1) * num_sqrt,
                    ].ravel()
                )
            )
            for col_ in range(num_sqrt)
        ]
        for row_ in range(num_sqrt)
    ]
    return area_list


def main():
    # ナンプレの問題が入った81桁の文字列を入力
    input_string = input()
    # 文字列をリストに変換したall_number_listを作成
    all_number_list = deepcopy(set_all_number_list(input_string))
    # 各列、各行、各エリアの候補となる数字の集合が入ったリストを作成
    column_list = deepcopy(get_column_list(all_number_list))
    row_list = deepcopy(get_row_list(all_number_list))
    area_list = deepcopy(get_area_list(all_number_list))
    # ナンプレを解く
    solve_number_place(all_number_list, column_list, row_list, area_list)


if __name__ == "__main__":
    main()
