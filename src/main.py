import csv
import datetime
from os import path

POINT_FILEPATH = "point.csv"
POINT_HEADER = ["date", "point", "comment"]
BORDER_FILEPATH = "border.csv"
BORDER_HEADER = ["date", "point"]


def main():
    print("Checking fine existence...")
    create_file(POINT_FILEPATH, POINT_HEADER)
    create_file(BORDER_FILEPATH, BORDER_HEADER)

    while True:
        output_list = []
        input_str = input(">>> ")
        if input_str.isdigit():
            output_list.append(datetime.datetime.now().isoformat())
            output_list.append(int(input_str))
            append_line(POINT_FILEPATH, output_list)
        else:
            if input_str == "comment":
                comment = input(">>> [comment] ")
                output_list.append(datetime.datetime.now().isoformat())
                output_list.append("NA")
                output_list.append(comment)
                append_line(POINT_FILEPATH, output_list)
            elif input_str == "border":
                while  True:
                    border = input(">>> [border] ")
                    if border == "cancel":
                        break
                    if not border.isdigit():
                        print("[ERROR] Inbalid input: Input border number or 'cancel' to exit border mode")
                    else:
                        output_list.append(datetime.datetime.now().isoformat())
                        output_list.append(int(border))
                        append_line(BORDER_FILEPATH, output_list)
                        break
            elif input_str == "end":
                return
            else:
                print("[ERROR] Invalid input: Input point number or following command")
                print("        'comment', 'border', 'end'")


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