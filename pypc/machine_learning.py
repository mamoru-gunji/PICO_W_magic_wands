import os
import csv
import subprocess
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


np.random.seed(0)
samples = 0
features = []
input_dim = 7
seq_length = 30
noise_factor = 5e-2
hidden_size = 16
batch_size = 2**5
epochs = 2**20
bulk_train = 100
bulk_test = 10
criterion = 0.7
patience = 1000
threshold = 0.95
train_rate = 0.25

input = []
labels = []

# データ読み込み

directory_path = os.path.join(os.getcwd(), "data")
data_file = os.path.join(directory_path, "samples.csv")
labels = []
samples = []
total_samples = 0
total_labels = 0

# CSVファイルの読み込み
with open(data_file, "r") as csvfile:
    # CSVファイルを読み込む
    csvreader = csv.reader(csvfile)

    # ヘッダーをスキップ
    next(csvreader)

    # 各行のラベルとサンプル数を取得

    for row in csvreader:
        try:
            label, sample = map(int, row)
            total_samples += sample
            total_labels += 1
            for i in range(sample):
                labels.append(label)
                samples.append(i)
        except Exception:
            pass


# 各行のデータを処理
data_list = []
for i in tqdm(range(total_samples)):
    if labels[i] not in features:
        features.append(label)
    data_file = os.path.join(
        directory_path, str(labels[i]) + "_" + str(samples[i]) + ".csv"
    )

    try:
        data = []
        with open(data_file, newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                data.append(row)
        data = np.array(data, dtype=float)
        # print(data.shape)
        # print(data)
        # for i in range(6):
        #     plt.plot(data[:, i])
        # plt.show()
        data_list.append((label, data))

    except Exception as e:
        print(f"エラー: {e}")

data_array = np.array(data_list, dtype=object)

for label, data in data_array:
    input.append(data)
    labels.append(label)

indices = np.arange(total_samples)
np.random.shuffle(indices)

input = np.array(input)
labels = np.array(labels)
input = input[indices]
labels = labels[indices]
num_train = int(total_samples * train_rate)
X_train, X_test = input[:num_train], input[num_train:]
y_train, y_test = labels[:num_train], labels[num_train:]

for i in range(bulk_train):
    X_train = np.append(
        X_train,
        (
            X_train[i]
            + np.hstack(
                (
                    np.random.normal(0, noise_factor**2, size=(data.shape[0], 1)),
                    np.random.normal(
                        0, noise_factor, size=(data.shape[0], data.shape[1] - 1)
                    ),
                )
            )
        ).reshape(1, seq_length, input_dim),
        axis=0,
    )
    y_train = np.append(y_train, y_train[i])

for i in range(bulk_test):
    X_test = np.append(
        X_test,
        (
            X_test[i]
            + np.hstack(
                (
                    np.random.normal(0, noise_factor**2, size=(data.shape[0], 1)),
                    np.random.normal(
                        0, noise_factor, size=(data.shape[0], data.shape[1] - 1)
                    ),
                )
            )
        ).reshape(1, seq_length, input_dim),
        axis=0,
    )
    y_test = np.append(y_test, y_test[i])

checkpoint_filepath = "model_checkpoint.h5"

# チェックポイントを保存するコールバックを定義
checkpoint_callback = ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,  # モデルの重みのみを保存
    monitor="val_accuracy",  # 監視する指標（ここでは検証データの正解率）
    mode="max",  # 監視する指標の最大化を目指す
    save_best_only=True,  # 最も良いモデルのみ保存
)


points = np.array(
    [
        (0, epochs / 2),
        (criterion, patience),
        (0.5 * (1 + criterion), patience / 10),
        (1, 1),
    ]
)


def gaussian_func(x, A, B, C, D):
    return A * np.exp(B * x**2) + C * np.exp(D * x)


# Fitting
params, covariance = curve_fit(
    gaussian_func, points[:, 0], points[:, 1], maxfev=2000000000
)


def dynamic_patience(accuracy):
    return int(gaussian_func(accuracy, params[0], params[1], params[2], params[3]))


def custom_early_stopping(
    monitor="val_accuracy", threshold=0.99, patience=5, verbose=1
):
    global epochs

    class CustomEarlyStopping(EarlyStopping):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.wait = 0  # Count of epochs without improvement
            self.epoch = 0
            self.patience = epochs  # Initialize with patience
            self.max_accuracy = 0.0

        def on_epoch_end(self, epoch, logs=None):
            self.epoch += 1
            current_metric = self.get_monitor_value(logs)
            if current_metric is None:
                return

            # Check if the current metric is above the threshold
            if current_metric >= threshold:
                self.stopped_epoch = epoch
                self.model.stop_training = True
                if verbose > 0:  # Changed from self.verbose to verbose
                    print(f"Epoch {epoch + 1}: Early stopping activated.")
            else:
                if current_metric > self.max_accuracy:
                    self.max_accuracy = current_metric
                    # print("\n" * 10 + "Record Max Accuracy!!!!!!" + "\n" * 30)
                    self.wait = 0  # Reset patience if new maximum accuracy achieved

                # Calculate dynamic patience
                if self.wait:
                    self.patience = min(
                        self.patience - 1, dynamic_patience(current_metric)
                    )
                else:
                    self.patience = dynamic_patience(current_metric)
                # print("WAIT:", self.wait, "\nPatience:", self.patience)
                # Check if the waiting period exceeds dynamic patience
                if 0 >= self.patience:
                    self.stopped_epoch = epoch
                    self.model.stop_training = True
                    if verbose > 0:  # Changed from self.verbose to verbose
                        print(
                            f"Epoch {epoch + 1}: Early stopping activated due to lack of improvement."
                        )
                else:
                    # If patience not exhausted, increment wait
                    self.wait += 1
                print(
                    "\nUntil the Early Stop is activated:",
                    self.patience,
                )

    return CustomEarlyStopping(
        monitor=monitor, mode="max", patience=patience, verbose=verbose
    )


# Usage
early_stopping_callback = custom_early_stopping(
    threshold=threshold, patience=patience, verbose=1
)


# Include it in your list of callbacks
callbacks = [checkpoint_callback, early_stopping_callback]

# LSTMモデルの作成

custom_optimizer = Adam(learning_rate=1e-5)
model = Sequential()
model.add(LSTM(hidden_size, input_shape=(seq_length, input_dim)))
model.add(Dense(total_labels, activation="softmax"))
model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer=custom_optimizer,
    metrics=["accuracy"],
)
history = model.fit(
    X_train,
    y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_data=(X_test, y_test),
    callbacks=callbacks,
)
model.summary()

y_hat_keras = model.predict(X_test)


# 最良のチェックポイントをロードしてテストデータに対する予測を行う
model.load_weights(checkpoint_filepath)
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
    total_labels=total_labels,
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
print(X_test.shape)
n = input.shape[0]

ht_1 = np.zeros(n * hidden_size).reshape((n, hidden_size))
Ct_1 = np.zeros(n * hidden_size).reshape((n, hidden_size))

ht_list = []

for t in np.arange(input.shape[1]):
    try:
        xt = np.array(input[:, t, :])
    except IndexError or TypeError:
        xt = np.array(input[t, :])

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
print(y_pred_reconstructed)
accuracy = np.mean(y_pred_reconstructed == y_test)
print(f"Approximation Accuracy: {accuracy}")


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
ConfusionMatrixDisplay(confusion_mtx, display_labels=list(range(total_labels))).plot(
    cmap="Blues", values_format="d"
)
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Confusion Matrix")
plt.show()

confusion_mtx_reconstructed = confusion_matrix(y_test, y_pred_reconstructed)

# 再現モデルの混同行列の可視化
ConfusionMatrixDisplay(
    confusion_mtx_reconstructed, display_labels=list(range(total_labels))
).plot(cmap="Blues", values_format="d")
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Reconstructed Model Confusion Matrix")
plt.show()


subprocess.run(["python", "npz2npy.py"])
subprocess.run(["python", "LSTM_np.py"])
