import csv
import ast
import os


def find_nth_occurrence(string, substring, sample_index):
    start = string.find(substring)
    while start >= 0 and sample_index > 0:
        start = string.find(substring, start + 1)
        sample_index -= 1
    return start


def new_dir(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_next_num(file_path, data_index):
    if os.path.exists(file_path):
        with open(file_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if row[0] == str(data_index):
                    return int(row[1]) + 1
    else:
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["label", "samples"])

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([data_index, 0])
        return 0


def write_new_num(file_path, data_index, num):
    data = []
    with open(file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
            if row[0] == str(data_index):
                index_to_replace = len(data) - 1
    if 0 <= index_to_replace < len(data):
        data[index_to_replace] = [data_index, num]
    # print(data)

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def save_data_to_csv(data, data_index, sample_index, directory):
    csv_file_name = os.path.join(directory, f"{data_index}_{sample_index}.csv")
    with open(csv_file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["time", "X", "Y", "Z", "ROLL", "PITCH", "YAW"])
        for row in data:
            writer.writerow(row)


def save_data(received_data, data_index):
    current_directory = os.getcwd()
    new_dir("data")

    samples_path = "data/samples.csv"
    # if os.path.exists(samples_path):
    #     print("ファイルが存在します")
    # else:
    #     print("ファイルは存在しません")

    # print(old_num)

    for sample_index in range(received_data.count("[[")):
        if get_next_num(samples_path, data_index):
            num = get_next_num(samples_path, data_index)
        else:
            num = 0
        print(num)
        start_index = find_nth_occurrence(received_data, "[[", sample_index)
        end_index = find_nth_occurrence(received_data, "]]", sample_index) + 2
        extracted_data = received_data[start_index:end_index]

        data_list = ast.literal_eval(extracted_data)
        # print(data_list)
        save_data_to_csv(
            data_list,
            data_index,
            num,
            os.path.join(current_directory, "data"),
        )
        write_new_num(samples_path, data_index, num)
        print(f"新しいデータ{[data_index, num]}を CSV ファイルに保存しました。")


if __name__ == "__main__":
    save_data(
        "[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]..[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]].",
        1,
    )
