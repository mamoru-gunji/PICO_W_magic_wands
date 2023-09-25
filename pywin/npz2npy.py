import numpy as np

# npzファイルの読み込み
npz_file = np.load("LSTM_parameter.npz")

# npzファイル内の各配列を個別にnpyファイルとして保存
for array_name in npz_file.files:
    np.save(f"{array_name}.npy", npz_file[array_name])
