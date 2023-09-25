import pandas as pd
import OpenEXR
import numpy as np
import os
import Imath


def load_exr_as_array(file_path):
    # OpenEXRファイルを開く
    exr_file = OpenEXR.InputFile(file_path)

    # ヘッダー情報を取得
    header = exr_file.header()
    width, height = header['dataWindow'].max.x + 1, header['dataWindow'].max.y + 1

    # RGBチャンネルを読み取る
    red_str = exr_file.channel('R', Imath.PixelType(Imath.PixelType.FLOAT))
    green_str = exr_file.channel('G', Imath.PixelType(Imath.PixelType.FLOAT))
    blue_str = exr_file.channel('B', Imath.PixelType(Imath.PixelType.FLOAT))

    # ピクセルデータをNumPy配列に変換
    red_data = np.frombuffer(red_str, dtype=np.float32).reshape(height, width)
    green_data = np.frombuffer(green_str, dtype=np.float32).reshape(height, width)
    blue_data = np.frombuffer(blue_str, dtype=np.float32).reshape(height, width)

    # RGBデータを結合して3チャンネルの配列にする
    image_data = np.dstack((red_data, green_data, blue_data))

    #image_data = np.transpose(image_data, (0, 2, 1))
    image_data = image_data.reshape(image_data.shape[0], image_data.shape[1]*image_data.shape[2])

    return image_data


# CSVファイルのパス
directory_path = os.path.join(os.getcwd(), "data-folder")
data_file = os.path.join(directory_path,"data.csv")


# CSVファイルを読み込む
df = pd.read_csv(data_file)

# データを格納するためのリストを初期化
data_list = []


# 各行のデータを処理
for index, row in df.iterrows():
    label = row['label']
    data_file = os.path.join(directory_path,row['data'])

    try:
        # EXRファイルを読み込む
        rgb_data = load_exr_as_array(data_file)       
        
        # ラベルとデータをタプルとしてリストに追加
        data_list.append((label, rgb_data))
    
    except Exception as e:
        print(f"エラー: {e}")

# データリストをNumPy配列に変換
data_array = np.array(data_list, dtype=object)