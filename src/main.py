import csv
import datetime
from os import path

POINT_FILEPATH = "point.csv"
POINT_HEADER = ["date", "point", "life", "comment"]
BORDER_FILEPATH = "border.csv"
BORDER_HEADER = ["date", "point"]
NOT_MULTI_LIST = ["チャレライ", "調整", "オート"] # 次の行のポイントを時速計算から除外したいコメント


def main():
    print("Checking fine existence...")
    create_file(POINT_FILEPATH, POINT_HEADER)
    create_file(BORDER_FILEPATH, BORDER_HEADER)

    life = 5
    while True:
        input_str = input(">>> ")
        if input_str.isdigit():
            output_list = [datetime.datetime.now().isoformat(), int(input_str), life]
            append_line(POINT_FILEPATH, output_list)
        else:
            if input_str == "comment":
                comment = input(">>> [comment] ")
                output_list = [datetime.datetime.now().isoformat(), "NA", "NA", comment]
                append_line(POINT_FILEPATH, output_list)
            elif input_str == "life":
                while  True:
                    new_life = input(">>> [life] ")
                    if new_life == "cancel":
                        break
                    if not new_life.isdigit():
                        print("[ERROR] Inbalid input: Input life number or 'cancel' to exit life mode")
                    else:
                        new_life = int(new_life)
                        if new_life <= 0 or new_life > 10:
                            print("[ERROR] Inbalid input: Life number is 1 or more and 10 or less")
                        else:
                            print(f"Set life number to {new_life}")
                            life = new_life
                            break
            elif input_str == "border":
                while  True:
                    border = input(">>> [border] ")
                    if border == "cancel":
                        break
                    if not border.isdigit():
                        print("[ERROR] Inbalid input: Input border number or 'cancel' to exit border mode")
                    else:
                        output_list = [datetime.datetime.now().isoformat(), int(border)]
                        append_line(BORDER_FILEPATH, output_list)
                        break
            elif input_str == "show":
                now_time = datetime.datetime.now()
                print(now_time)
                try:
                    with open(POINT_FILEPATH, "r") as file_object:
                        reader = csv.reader(file_object)
                        csv_list = list(reader)
                        csv_list.pop(0) # remove header
                        sum = sum_points(csv_list)
                        print(f"Total point:\n\t{sum}")
                        per_hour, time = calculate_per_hour(csv_list)
                        print(f"Total play time:\n\t{time}")
                        print(f"Average point per hour:\n\t{per_hour}\n")
                except Exception as e:
                    raise Exception(e)
                try:
                    with open(BORDER_FILEPATH, "r") as file_object:
                        reader = csv.reader(file_object)
                        csv_list = list(reader)
                        csv_list.pop(0) # remove header
                        recent_border = int(csv_list[-1][1])
                        recent_time = datetime.datetime.fromisoformat(csv_list[-1][0])
                        print(f"Recent actual border:\n\t{recent_border} ({now_time - recent_time} ago)")
                        border_per_hour = calculate_border_per_hour(csv_list)
                        print(f"Border point per hour:\n\t{border_per_hour}")
                        estimate_border = recent_border + border_per_hour * (now_time - recent_time).total_seconds() / 3660
                        print(f"Current Border estimate:\n\t{int(estimate_border)}")
                except Exception as e:
                    raise Exception(e)
            elif input_str == "exit":
                return
            else:
                print("[ERROR] Invalid input: Input point number or following command")
                print("        'comment', 'life', 'border', 'show', 'exit'")


def sum_points(csv_list):
    sum = 0
    for line in csv_list:
        if line[1].isdigit():
            sum += int(line[1])
    return sum


def calculate_per_hour(csv_list):
    sum_point = 0
    time = datetime.datetime.fromisoformat(csv_list[0][0])
    sum_time = datetime.timedelta()
    exclusion_flag = False
    for line in csv_list:
        prev_time = time
        time = datetime.datetime.fromisoformat(line[0])
        if line[1].isdigit():
            if exclusion_flag:
                exclusion_flag = False
                continue
            sum_point += int(line[1])
            sum_time += time - prev_time
        else:
            comment = line[-1]
            if comment in NOT_MULTI_LIST:
                exclusion_flag = True # 次の行のポイントを時速計算から除外
    sum_seconds = sum_time.total_seconds()
    per_hour = sum_point / sum_seconds * 3660
    return per_hour, sum_time


def calculate_border_per_hour(csv_list):
    start_time = datetime.datetime.fromisoformat(csv_list[0][0])
    start_point = int(csv_list[0][1])
    recent_time = datetime.datetime.fromisoformat(csv_list[-1][0])
    recent_point = int(csv_list[-1][1])
    sum_seconds = (recent_time - start_time).total_seconds()
    per_hour = (recent_point - start_point) / sum_seconds * 3660
    return per_hour


def create_file(filepath,headers_list):
    if path.exists(filepath):
        print(f"\t{filepath} already exists")
        return
    try:
        print(f"\tCreate {filepath}")
        with open(filepath, "wt", encoding="utf-8", newline="") as file_object:
            writer = csv.writer(file_object)
            writer.writerow(headers_list)
        return
    except Exception as e:
        raise Exception(e)
    

def append_line(filepath, line):
    try:
        with open(filepath, "a", encoding="utf-8", newline="") as file_object:
            writer = csv.writer(file_object)
            writer.writerow(line)
            print(f"Write to {filepath} {line}")
        return
    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    main()