import numpy as np
from collections import defaultdict
from pprint import pprint
from copy import deepcopy
import time

# 初期設定
num = 9  # 一辺の問題のサイズ
num_sqrt = int(np.sqrt(num))  # 一辺の問題のサイズの平方根
num_all_set = set([i + 1 for i in range(num)])  # 1~numの集合

# 共通で使用する変数
no_cnt = 0  # 解がない場合のカウント
ans_cnt = 0  # 解の数のカウント
ans_list = []  # 解のリスト
start_time = 0  # 処理時間の計測開始
solve_cnt = 0  # ループの回数


def solve_number_place(number_list, column_list, row_list, area_list):
    """ナンプレを解く

    Args:
        number_list (numpy.array): 数字のリスト
        column_list (list): 各列の候補となる数字の集合が入ったリスト
        row_list (list): 各行の候補となる数字の集合が入ったリスト
        area_list (list): 各エリアの候補となる数字の集合が入ったリスト
    """
    global no_cnt, solve_cnt
    solve_cnt += 1
    # 各マスの候補となる数字の集合が入ったリストを取得
    possibility_list = deepcopy(
        get_possibility_list(number_list, column_list, row_list, area_list)
    )
    # まだ決定していない座標のリストを取得
    possibility_num_list = get_possibility_place_list(possibility_list)

    # まだ決定していない座標がない場合、ナンプレが正しいかどうかを判定する
    if len(possibility_num_list) == 0:
        flag = is_correct_array(number_list)
        if not flag:
            no_cnt += 1
            return
        output_answer(number_list)
        return

    # 候補が1つしかない座標のリストを取得
    possibility_1_place_list = get_possibility_1_place_list(possibility_list)

    # 候補が1つしかない座標がある場合、その座標を埋めて再帰処理を行う
    if len(possibility_1_place_list) > 0:
        for i_, col_, row_ in possibility_1_place_list:
            number_list[row_][col_] = i_
            column_list[col_].discard(i_)
            row_list[row_].discard(i_)
            area_list[row_ // num_sqrt][col_ // num_sqrt].discard(i_)
        solve_number_place(
            deepcopy(number_list),
            deepcopy(column_list),
            deepcopy(row_list),
            deepcopy(area_list),
        )
        return

    # 候補が1つしかない座標がない場合、候補の中から1つ数字を選んで再帰処理を行う
    row = possibility_num_list[0] // num
    col = possibility_num_list[0] % num

    # 候補の中から1つ数字を選んで再帰処理を行う
    for i in possibility_list[row][col]:
        number_list[row][col] = i
        new_column_list = deepcopy(column_list)
        new_column_list[col].discard(i)
        new_row_list = deepcopy(row_list)
        new_row_list[row].discard(i)
        new_area_list = deepcopy(area_list)
        new_area_list[row // num_sqrt][col // num_sqrt].discard(i)
        solve_number_place(
            deepcopy(number_list),
            deepcopy(new_column_list),
            deepcopy(new_row_list),
            deepcopy(new_area_list),
        )

def is_correct_array(number_list):
    """ナンプレが正しいかどうかを判定する

    Args:
        number_list (numpy.array): 数字のリスト

    Returns:
        bool: 正しければTrue、正しくなければFalse
    """
    column_list = deepcopy(get_column_list(number_list))
    for col in column_list:
        if col:
            return False
    row_list = deepcopy(get_row_list(number_list))
    for row in row_list:
        if row:
            return False
    area_list = deepcopy(get_area_list(number_list))
    for area in sum(area_list, []):
        if area:
            return False
    return True


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


def get_possibility_place_list(possibility_list):
    """各マスの候補となる数字の集合の数が最小となるマスの座標のリストを返す
    座標のリストは、行番号 * num + 列番号で表してる

    Args:
        possibility_list (list of list): 各マスの候補となる数字の集合が入ったリスト

    Returns:
        list: 各マスの候補となる数字の集合の数が最小となるマスの座標のリスト
    """

    flag = False
    dic = defaultdict(list)
    for row in range(num):
        for col in range(num):
            possibility_num = len(possibility_list[row][col])
            if possibility_num == 0:
                continue
            flag = True
            dic[possibility_num].append(row * num + col)
    return dic[min(dic.keys())] if flag else []


def get_possibility_1_place_list(possibility_list):
    """候補が1つしかない座標のリストを返却する

    Args:
        possibility_list (list of list): 各マスの候補となる数字の集合が入ったリスト

    Returns:
        list: 候補が1つしかない座標のリスト
    """
    global num_sqrt
    base_list = []
    for row in range(num):
        for col in range(num):
            if len(possibility_list[row][col]) != 1:
                continue
            i = list(possibility_list[row][col])[0]
            c_list = [i, col, row]
            if c_list not in base_list:
                base_list.append(c_list)
    return base_list


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

def output_answer(number_list):
    """答えを出力する

    Args:
        number_list (numpy.array): 数字のリスト
    """
    global solve_cnt, no_cnt, ans_cnt
    ans_cnt += 1
    ans_list.append(number_list)
    print(number_list)
    print(f'time : {"{:.3f}".format(time.time() - start_time)}s')
    print(f"count:{solve_cnt}")
    print(f"no_cnt: {no_cnt}")
    print(f"ans_cnt: {ans_cnt}")

def main():
    global start_time, ans_list
    # ナンプレの問題が入った81桁の文字列を入力
    input_string = input()
    # 処理時間の計測開始
    start_time = time.time()
    # 文字列をリストに変換したall_number_listを作成
    all_number_list = deepcopy(set_all_number_list(input_string))
    # 各列、各行、各エリアの候補となる数字の集合が入ったリストを作成
    column_list = deepcopy(get_column_list(all_number_list))
    row_list = deepcopy(get_row_list(all_number_list))
    area_list = deepcopy(get_area_list(all_number_list))
    # ナンプレを解く
    solve_number_place(all_number_list, column_list, row_list, area_list)

    print("---result---")
    output_answer(ans_list[0])


if __name__ == "__main__":
    main()
