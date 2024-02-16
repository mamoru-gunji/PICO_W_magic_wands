import random
from ulab import numpy as np

# 6x6のランダム行列を作成# 835
size = 75
random_matrix = np.array([[random.random() for _ in range(size)] for _ in range(size)])
random_matrix_2 = np.array([[random.random() for _ in range(size)] for _ in range(size)])
random_matrix_3 = np.array([[random.random() for _ in range(size)] for _ in range(size)])

random_array = np.array([[random.random() for _ in range(6)] for _ in range(size)])
random_matrix = np.dot(random_matrix*random_matrix_2*random_matrix_3, random_array)

# ランダム行列を出力
itemsize_in_bytes = random_matrix.itemsize
total_size_in_bytes = random_matrix.size * itemsize_in_bytes
print(f"The variable uses {total_size_in_bytes} bytes.")