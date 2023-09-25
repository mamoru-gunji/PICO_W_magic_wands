import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import subprocess
from bilinear_interpolation import resize_matrix
import tqdm
import csv
import matplotlib.pyplot as plt


np.random.seed(0)
samples = 0
features = []
input_dim = 6
seq_length = 30
noise_factor = 1e-2

input = []
labels = []

# データ読み込み

directory_path = os.path.join(os.getcwd(), "data-folder")
data_file = os.path.join(directory_path, "data.csv")
df = pd.read_csv(data_file)


def interpolate_data(data, seq_length):
    interpolated_data = []
    interpolated_data = resize_matrix(data, seq_length, input_dim)
    return interpolated_data


data_list = []


# 各行のデータを処理
for index, row in tqdm.tqdm(
    df.iterrows(), desc="proc1", postfix="range", ncols=80, total=df.shape[0]
):
    label = row["label"]
    if label not in features:
        features.append(label)
    data_file = os.path.join(directory_path, row["data"])

    try:
        data = []
        with open(data_file, newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                data.append(row)
        data = np.array(data, dtype=float)
        # print(data.shape)
        data = interpolate_data(data, seq_length)
        # print(data)
        # for i in range(6):
        #     plt.plot(data[:, i])
        # plt.show()
        data_list.append((label, data))
        samples += 1

    except Exception as e:
        print(f"エラー: {e}")

data_array = np.array(data_list, dtype=object)

for label, data in data_array:
    input.append(data)
    labels.append(label)


num_features = len(features)
indices = np.arange(samples)
np.random.shuffle(indices)

input = np.array(input)
labels = np.array(labels)
input = input[indices]
labels = labels[indices]
num_train = int(samples * 0.5)
X_train, X_test = input[:num_train], input[num_train + 1 :]
y_train, y_test = labels[:num_train], labels[num_train + 1 :]

for i in range(1000):
    # print(
    #     X_train.shape,
    #     X_train[i].shape,
    #     (X_train[i] + np.random.normal(0, noise_factor, size=data.shape)).reshape(1,seq_length, input_dim).shape,
    # )
    X_train = np.append(
        X_train,
        (X_train[i] + np.random.normal(0, noise_factor, size=data.shape)).reshape(
            1, seq_length, input_dim
        ),
        axis=0,
    )
    y_train = np.append(y_train, y_train[i])

hidden_size = 64

# LSTMモデルの作成
custom_optimizer = Adam(learning_rate=1e-5)
model = Sequential()
model.add(LSTM(hidden_size, input_shape=(seq_length, input_dim)))
model.add(Dense(num_features, activation="softmax"))
model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer=custom_optimizer,
    metrics=["accuracy"],
)
history = model.fit(
    X_train, y_train, epochs=512, batch_size=64, validation_data=(X_test, y_test)
)
model.summary()

y_hat_keras = model.predict(X_test)

# モデルの評価
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss}, Test Accuracy: {test_accuracy}")

# LSTMモデルの重みを取得
model_weights = model.get_weights()

W, U, b, W_out, b_out = model.get_weights()
Wi = W[:, 0:hidden_size]
Wf = W[:, hidden_size : 2 * hidden_size]
Wc = W[:, 2 * hidden_size : 3 * hidden_size]
Wo = W[:, 3 * hidden_size :]
Ui = U[:, 0:hidden_size]
Uf = U[:, hidden_size : 2 * hidden_size]
Uc = U[:, 2 * hidden_size : 3 * hidden_size]
Uo = U[:, 3 * hidden_size :]
bi = b[0:hidden_size]
bf = b[hidden_size : 2 * hidden_size]
bc = b[2 * hidden_size : 3 * hidden_size]
bo = b[3 * hidden_size :]

np.savez(
    "LSTM_parameter.npz",
    seq_length=seq_length,
    num_features=num_features,
    input_dim=input_dim,
    hidden_size=hidden_size,
    Wi=Wi,
    Wf=Wf,
    Wc=Wc,
    Wo=Wo,
    Ui=Ui,
    Uf=Uf,
    Uc=Uc,
    Uo=Uo,
    bi=bi,
    bf=bf,
    bc=bc,
    bo=bo,
    W_out=W_out,
    b_out=b_out,
)


def sigmoid(input):
    return 1.0 / (1.0 + np.exp(-input))


input = X_test
n = input.shape[0]

ht_1 = np.zeros(n * hidden_size).reshape(n, hidden_size)
Ct_1 = np.zeros(n * hidden_size).reshape(n, hidden_size)

ht_list = []

for t in np.arange(input.shape[1]):
    xt = np.array(input[:, t, :])
    it = sigmoid(np.dot(xt, Wi) + np.dot(ht_1, Ui) + bi)
    Ct_tilda = np.tanh(np.dot(xt, Wc) + np.dot(ht_1, Uc) + bc)
    ft = sigmoid(np.dot(xt, Wf) + np.dot(ht_1, Uf) + bf)
    Ct = it * Ct_tilda + ft * Ct_1
    ot = sigmoid(np.dot(xt, Wo) + np.dot(ht_1, Uo) + bo)
    ht = ot * np.tanh(Ct)
    ht_list.append(ht)

    ht_1 = ht
    Ct_1 = Ct

my_y_hat = np.dot(ht, W_out) + b_out


y_pred_reconstructed = np.argmax(my_y_hat, axis=1)
accuracy = np.mean(y_pred_reconstructed == y_test)
print(f"Approximation Accuracy: {accuracy}")

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# 学習曲線のプロット
acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]
epochs = range(len(acc))

# 1) Accracy Plt
plt.plot(epochs, acc, "bo", label="training acc")
plt.plot(epochs, val_acc, "b", label="validation acc")
plt.title("Training and Validation acc")
plt.legend()

plt.figure()
plt.semilogy(epochs, loss, "ro", label="training loss")
plt.semilogy(epochs, val_loss, "r", label="validation loss")
plt.title("Training and Validation loss")
plt.legend()

# 混同行列の計算
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
confusion_mtx = confusion_matrix(y_test, y_pred_classes)

# 混同行列の可視化
ConfusionMatrixDisplay(confusion_mtx, display_labels=list(range(num_features))).plot(
    cmap="Blues", values_format="d"
)
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Confusion Matrix")
plt.show()

confusion_mtx_reconstructed = confusion_matrix(y_test, y_pred_reconstructed)

# 再現モデルの混同行列の可視化
ConfusionMatrixDisplay(
    confusion_mtx_reconstructed, display_labels=list(range(num_features))
).plot(cmap="Blues", values_format="d")
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Reconstructed Model Confusion Matrix")
plt.show()


subprocess.run(["python", "npz2npy.py"])
subprocess.run(["python", "LSTM_np.py"])
