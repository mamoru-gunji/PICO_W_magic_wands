import time

try:
    import numpy as np
except ImportError:
    from ulab import numpy as np

    pass

import global_value as g

try:
    from numpy import random
except ImportError:
    import random

    pass

try:
    from memory_usage import print_memory_usage as mem

    g.mem_use = True
except ImportError:
    g.mem_use = False
    pass


if g.mem_use:
    g.mem = mem


class LSTM:
    def __init__(self, prt=False):
        g.prt = prt
        if prt:
            try:
                now = time.ticks_ms()
            except Exception:
                pass
        self.Wi = np.load("Wi.npy")
        self.Ui = np.load("Ui.npy")
        self.bi = np.load("bi.npy")
        self.Wc = np.load("Wc.npy")
        self.Uc = np.load("Uc.npy")
        self.bc = np.load("bc.npy")
        self.Wf = np.load("Wf.npy")
        self.Uf = np.load("Uf.npy")
        self.bf = np.load("bf.npy")
        self.Wo = np.load("Wo.npy")
        self.Uo = np.load("Uo.npy")
        self.bo = np.load("bo.npy")
        self.W_out = np.load("W_out.npy")
        self.b_out = np.load("b_out.npy")
        self.ht_1 = None
        self.Ct_1 = None

        self.hidden_size = int(open("hidden_size.txt", "r").read())
        self.input_dim = int(open("input_dim.txt", "r").read())
        self.seq_length = int(open("seq_length.txt", "r").read())
        self.total_labels = int(open("total_labels.txt", "r").read())
        self.y_hat = np.array([])
        self.input_data = np.array([])
        if g.mem_use:
            g.mem(g.prt)
        if prt:
            try:
                print((time.ticks_ms() - now) / 1000)
            except Exception:
                pass

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def forward(self, x):
        n, hidden_size = x.shape[0], self.Wi.shape[1]
        ht_list = []

        if self.ht_1 is None:
            self.ht_1 = np.zeros(n * hidden_size).reshape((n, hidden_size))
            self.Ct_1 = np.zeros(n * hidden_size).reshape((n, hidden_size))
        for t in np.arange(x.shape[1]):
            try:
                xt = np.array(x[:, t, :])
                onesample = False

            except IndexError or TypeError:
                xt = np.array(x[t, :])
                onesample = True

            it = self.sigmoid(
                np.dot(xt, self.Wi) + np.dot(self.ht_1, self.Ui) + self.bi
            )
            Ct_tilda = np.tanh(
                np.dot(xt, self.Wc) + np.dot(self.ht_1, self.Uc) + self.bc
            )
            ft = self.sigmoid(
                np.dot(xt, self.Wf) + np.dot(self.ht_1, self.Uf) + self.bf
            )
            Ct = it * Ct_tilda + ft * self.Ct_1
            ot = self.sigmoid(
                np.dot(xt, self.Wo) + np.dot(self.ht_1, self.Uo) + self.bo
            )
            ht = ot * np.tanh(Ct)
            ht_list.append(ht)

            self.ht_1 = ht
            self.Ct_1 = Ct

        y = np.dot(ht, self.W_out) + self.b_out
        if onesample:
            y = np.array([y[0, :]])
        # print(y.shape)
        return y

    def generate_random_matrix(self, rows, cols):
        matrix = [[random.random() for _ in range(cols)] for _ in range(rows)]
        return matrix

    def dammy_data(self):
        self.input_data = np.array(
            self.generate_random_matrix(self.seq_length, self.input_dim)
        )

    def machine_pred(self, input_data):
        if g.prt:
            try:
                now = time.ticks_ms()
            except Exception:
                pass
        self.y_hat = self.forward(input_data)

        if g.prt:
            label = np.array([])
            try:
                next_label = np.array([np.argmax(self.y_hat, axis=1)])
            except Exception:
                next_label = np.array(np.argmax(self.y_hat, axis=1))
                
            label = np.concatenate(
                (label, next_label), axis=0
            )
            try:
                print((time.ticks_ms() - now) / 1000)
                now = time.ticks_ms()
            except Exception:
                pass

            # print(self.y_hat)
            y = np.array(range(self.total_labels))
            print("TEST DATA CORRECT LABEL: ", y, "\n ONLY NUMPY CLUSSTERING: ", label)

        return self.y_hat

    ######################################################################
    def main(self):
        if self.input_data.size < 1:
            self.dammy_data()
        y_hat = self.machine_pred(self.input_data)
        return y_hat


if __name__ == "__main__":
    PRED = LSTM(prt=True)
    print(PRED.main())