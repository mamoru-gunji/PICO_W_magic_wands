import numpy as np

# npzファイルの読み込み
npz_file = np.load("LSTM_parameter.npz")

# npzファイル内の各配列を個別にnpyファイルとして保存
for array_name in npz_file.files:
    if npz_file[array_name].shape == ():
        with open(f"{array_name}.txt", 'w') as file:
            file.write(str(npz_file[array_name]))
    else:
        np.save(f"{array_name}.npy", npz_file[array_name])
