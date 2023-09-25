import numpy as np
from manualLSTM import manualLSTM
from bilinear_interpolation import resize_matrix

loaded_data = np.load('LSTM_parameter.npz')

hidden_size = loaded_data['hidden_size']
Wi = loaded_data['Wi']
Ui = loaded_data['Ui']
bi = loaded_data['bi']
Wc = loaded_data['Wc']
Uc = loaded_data['Uc']
bc = loaded_data['bc']
Wf = loaded_data['Wf']
Uf = loaded_data['Uf']
bf = loaded_data['bf']
Wo = loaded_data['Wo']
Uo = loaded_data['Uo']
bo = loaded_data['bo']
W_out = loaded_data['W_out']
b_out = loaded_data['b_out']

input_dim = loaded_data['input_dim']
seq_length = loaded_data['seq_length']
num_features = loaded_data['num_features']

lstm_instance = manualLSTM(Wi, Ui, bi, Wc, Uc, bc, Wf, Uf, bf, Wo, Uo, bo, W_out, b_out)


def interpolate_data(data, seq_length):
    interpolated_data = []
    interpolated_data = resize_matrix(data, seq_length, input_dim)
    return interpolated_data


X_test = interpolate_data(np.random.rand(np.random.randint(10,120), input_dim),seq_length)
X_test = np.stack([X_test, interpolate_data([np.random.beta(2,2,input_dim) for i in range(np.random.randint(10,120))],seq_length)], axis=0)
X_test = np.concatenate([X_test, interpolate_data(np.random.randn(np.random.randint(10,120), input_dim), seq_length).reshape(1, seq_length, input_dim)], axis=0)
X_test = np.concatenate([X_test, interpolate_data([np.random.gamma(3,1,input_dim) for i in range(np.random.randint(10,120))], seq_length).reshape(1, seq_length, input_dim)], axis=0)
y = np.array(range(num_features))

y_hat = lstm_instance.forward(X_test)
label = np.argmax(y_hat, axis=1)
print(y_hat)
print('TEST DATA CORRECT LABEL: ',y,'\n ONLY NUMPY CLUSSTERING: ',label)
