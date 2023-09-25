# bilinear_interpolation.py
import numpy as np


def bilinear_interpolation(x, y, points):
    x1, y1 = int(np.floor(x)), int(np.floor(y))
    x2, y2 = x1 + 1, y1 + 1
    if x2 >= len(points) or y2 >= len(points[0]):
        return points[x1][y1]
    Q11 = points[x1][y1]
    Q12 = points[x1][y2]
    Q21 = points[x2][y1]
    Q22 = points[x2][y2]

    result = (
        Q11 * (x2 - x) * (y2 - y)
        + Q21 * (x - x1) * (y2 - y)
        + Q12 * (x2 - x) * (y - y1)
        + Q22 * (x - x1) * (y - y1)
    )

    return result


def resize_matrix(original_matrix, new_rows, new_cols):
    resized_matrix = []
    for i in range(new_rows):
        row = []
        for j in range(new_cols):
            x = (i / (new_rows - 1)) * (len(original_matrix) - 1)
            y = (j / (new_cols - 1)) * (len(original_matrix[0]) - 1)
            interpolated_value = bilinear_interpolation(x, y, original_matrix)
            row.append(interpolated_value)
        resized_matrix.append(row)
    resized_matrix = np.array(resized_matrix)
    return resized_matrix


# original_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# new_rows = 4
# new_cols = 6

# expanded_matrix = resize_matrix(original_matrix, new_rows, new_cols)
# print(expanded_matrix)
