try:
    import numpy as np
except ImportError:
    from ulab import numpy as np
    pass

class manualLSTM:
    def __init__(self, Wi, Ui, bi, Wc, Uc, bc, Wf, Uf, bf, Wo, Uo, bo, W_out, b_out):
        self.Wi = Wi
        self.Ui = Ui
        self.bi = bi
        self.Wc = Wc
        self.Uc = Uc
        self.bc = bc
        self.Wf = Wf
        self.Uf = Uf
        self.bf = bf
        self.Wo = Wo
        self.Uo = Uo
        self.bo = bo
        self.W_out = W_out
        self.b_out = b_out
        self.ht_1 = None
        self.Ct_1 = None

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
            y = np.array([y[0,:]])
        # print(y.shape)
        return y