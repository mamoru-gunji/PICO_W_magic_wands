from scipy.optimize import curve_fit
import numpy as np
import math

# Given points
points = np.array([(0, 2**15), (0.5, 100), (0.75, 10), (1, 0)])


# Exponential function model
def gaussian_func(x, A, B, C, D):
    return A * np.exp(B * x**2) + C * np.exp(D * x)


# Fitting
params, covariance = curve_fit(
    gaussian_func,
    points[:, 0],
    points[:, 1],
    # p0=initial_guesses,
    maxfev=2000000000,
)


# Fitted parameters
A_fit, B_fit, C_fit, D_fit = params

print("A:", A_fit)
print("B:", B_fit)
print("C:", C_fit)
print("D:", D_fit)

for x in range(1001):
    x_test = 0.001 * x
    print(x, int(gaussian_func(x_test, params[0], params[1], params[2], params[3])))
