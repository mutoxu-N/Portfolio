# 医療費集計フォームver3.1用

import os
import shutil
import pandas as pd
from openpyxl import load_workbook

# consts
DIRECTORY = "2024"
TEMPLATE_FILE_NAME = "iryouhi_form_v3.xlsx"
DATA_FILE_NAME = f"data{DIRECTORY}.csv"
OUTPUT_FILE_NAME = f"{DIRECTORY}医療費.xlsx"
HOSPITALS_FILE_NAME = "hospitals.csv"
COLUMN_NAMES = {
    "患者": "B",
    "医療機関": "C",
    "区分/診療": "D",
    "区分/医薬品": "E",
    "区分/介護": "F",
    "区分/その他": "G",
    "金額": "H",
    "補填": "I",
    "日時": "J"
}
FIRST_ROW = 9
TRANS = str.maketrans("1234567890", "１２３４５６７８９０")

# variables
cursor = FIRST_ROW  # 書き込み開始行
cost_total = 0  # 支払金額
cost_comp = 0  # 補填金額

cost_hospital = 0
cost_transport = 0
cost_misc = 0


# 文字列からセル符号を生成
def cell(column_name: str, row_num: int) -> str:
    return COLUMN_NAMES[column_name] + str(row_num)


# ワーキングディレクトリ内ファイルパス
def fi(file_name: str) -> str:
    return DIRECTORY + "/" + file_name


# 病院名を全角20文字に圧縮
def input_name(name: str, count: int = 0, is_trans=False) -> str:
    if is_trans:
        # 交通費ありのとき
        str_name = name
        name_size = 13 - len(str(count))
        if len(name) > name_size:
            str_name = name[:name_size-1] + "～"
        return str_name + f"（交通）往復{str(count).translate(TRANS)}回"

    elif len(name) > 20:
        # ファイル名が21文字以上のとき
        return name[:19] + "～"

    else:
        # ファイル名をそのまま返す
        return name


# テンプレートをコピー
if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)
shutil.copy(TEMPLATE_FILE_NAME, fi(OUTPUT_FILE_NAME))

# csv読み込み
# 入力された病院
csv_data = pd.read_csv(fi(DATA_FILE_NAME))
hospitals_remain = set(csv_data["病院"].unique())

# 登録済の病院
hospital_data = pd.read_csv(HOSPITALS_FILE_NAME)
hospitals_registered = set(
    hospital_data["病院"].unique()).intersection(hospitals_remain)

# 書き込み
out_wb = load_workbook(fi(OUTPUT_FILE_NAME))
out_ws = out_wb["医療費集計フォーム"]

# 指定医療機関
for hos_name in hospitals_registered:
    hospital = hospital_data[hospital_data["病院"] == hos_name].values[0]
    df_hos = csv_data[csv_data["病院"] == hos_name]

    # 医療機関のCSVデータを一行ずつ読み込む
    for row in df_hos.itertuples():
        cost_hospital += row.__getattribute__("費用")
        out_ws[cell("患者", cursor)] = row.__getattribute__("患者")
        out_ws[cell("医療機関", cursor)] = input_name(hos_name)
        out_ws[cell("区分/診療", cursor)] = "該当する" if (hospital[1] == 1) else ""
        out_ws[cell("区分/医薬品", cursor)] = "該当する" if (hospital[2] == 1) else ""
        out_ws[cell("区分/介護", cursor)] = "該当する" if (hospital[3] == 1) else ""
        out_ws[cell("区分/その他", cursor)] = "該当する" if (hospital[4] == 1) else ""
        out_ws[cell("金額", cursor)] = row.__getattribute__("費用")
        out_ws[cell("補填", cursor)] = 0
        out_ws[cell("日時", cursor)] = row.__getattribute__("日付")
        cursor += 1

    # 交通費が正なら
    if (hospital[5] > 0):
        cost_transport += hospital[5]*df_hos.shape[0]
        out_ws[cell("患者", cursor)] = row.__getattribute__("患者")
        out_ws[cell("医療機関", cursor)] = input_name(
            hos_name, df_hos.shape[0], True)
        out_ws[cell("区分/診療", cursor)] = ""
        out_ws[cell("区分/医薬品", cursor)] = ""
        out_ws[cell("区分/介護", cursor)] = ""
        out_ws[cell("区分/その他", cursor)] = "該当する"
        out_ws[cell("金額", cursor)] = hospital[5]*df_hos.shape[0]
        out_ws[cell("補填", cursor)] = 0
        cursor += 1

    hospitals_remain.remove(hos_name)


# 指定されていない医療機関
print("--未登録の医療機関--")
for hos_name in hospitals_remain:
    df_hos = csv_data[csv_data["病院"] == hos_name]
    print(f"{hos_name} x{df_hos.shape[0]}")

    # 医療機関のCSVデータを一行ずつ読み込む
    for row in df_hos.itertuples():
        cost_misc += row.__getattribute__("費用")
        out_ws[cell("患者", cursor)] = row.__getattribute__("患者")
        out_ws[cell("医療機関", cursor)] = input_name(hos_name)
        out_ws[cell("区分/診療", cursor)] = ""
        out_ws[cell("区分/医薬品", cursor)] = ""
        out_ws[cell("区分/介護", cursor)] = ""
        out_ws[cell("区分/その他", cursor)] = ""
        out_ws[cell("金額", cursor)] = row.__getattribute__("費用")
        out_ws[cell("補填", cursor)] = 0
        out_ws[cell("日時", cursor)] = row.__getattribute__("日付")
        cursor += 1

    # # 交通費を0で登録
    # out_ws[cell("患者", cursor)] = row.__getattribute__("患者")
    # out_ws[cell("医療機関", cursor)] = input_name(hos_name, df_hos.shape[0], True)
    # out_ws[cell("区分/診療", cursor)] = ""
    # out_ws[cell("区分/医薬品", cursor)] = ""
    # out_ws[cell("区分/介護", cursor)] = ""
    # out_ws[cell("区分/その他", cursor)] = "該当する"
    # out_ws[cell("金額", cursor)] = 0
    # out_ws[cell("補填", cursor)] = 0
    # cursor += 1


# 合計金額
out_wb.save(fi(OUTPUT_FILE_NAME))

# 合計金額
print()
print("--支払金額--")
print("  医療費: ", cost_hospital)
print("  交通費: ", cost_transport)
print("  その他: ", cost_misc)
print("  合計: ", cost_hospital + cost_transport + cost_misc)