import csv
import datetime
from os import path

POINT_FILEPATH = "point.csv"
POINT_HEADER = ["date", "point"]
BORDER_FILEPATH = "border.csv"
BORDER_HEADER = ["date", "point"]


def main():
    print("Checking fine existence...")
    create_file(POINT_FILEPATH, POINT_HEADER)
    create_file(BORDER_FILEPATH, BORDER_HEADER)

    while True:
        output_list = []
        input_list = input(">>> ").split(" ")
        if input_list[0].isdigit():
            output_list.append(datetime.datetime.now().isoformat())
            output_list.append(int(input_list[0]))
            append_line(POINT_FILEPATH, output_list)


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
            print(f"Write {line}")
        return
    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    main()