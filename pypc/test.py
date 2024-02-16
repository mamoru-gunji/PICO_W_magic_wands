import csv
from tqdm import tqdm

# CSVファイルのパス
csv_file_path = "data/samples.csv"

# ラベルとサンプル数を格納するリスト
labels = []
samples = []
total_samples = 0

# CSVファイルの読み込み
with open(csv_file_path, "r") as csvfile:
    # CSVファイルを読み込む
    csvreader = csv.reader(csvfile)

    # ヘッダーをスキップ
    next(csvreader)

    # 各行のラベルとサンプル数を取得
    for row in csvreader:
        label, sample = map(int, row)
        total_samples += sample
        for i in range(sample):
            labels.append(label)
            samples.append(i)

# ラベルとサンプル数を表示
for label, sample in zip(labels, samples):
    print(f"Label: {label}, Samples: {sample}")

# サンプルの総数を計算


print(total_samples)
# サンプルの総数でループ
for i in tqdm(range(total_samples)):
    print(str(labels[i]) + "_" + str(samples[i]))
    # ここで何か処理を行う（例: ラベルごとにサンプルを処理するなど）
    # ループ内の処理を追加してください
    pass
