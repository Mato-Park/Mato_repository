# 1. make random numbers
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


n = 1000
y = np.random.normal(loc = 0, scale = 1, size = n).reshape(n, 1)
x = np.random.normal(loc = 0, scale = 1, size = n).reshape(n, 1)
x2 = np.random.normal(loc = 0, scale = 1, size = n).reshape(n, 1)
x2 = x2 * x2
x3 = np.random.normal(loc = 1, scale = 2, size = n).reshape(n, 1)
cons = np.ones((1000, 1))
error = np.random.normal(loc = 0, scale = 1, size = n).reshape(n, 1)

y_bar = 3 * cons + x + 2 * x2 + x3 + error
X = np.concatenate((cons, x, x2, x3), axis = 1)
k = np.shape(X)[1]

XX = X.T.dot(X)
xy = X.T.dot(y_bar)
beta_hat = np.linalg.inv(XX).dot(xy)

# def lin_regression(x, y):
#     XX = np.dot(x.T, x)
#     xy = np.dot(x.T, y)
#     beta_hat = np.dot(np.linalg.inv(XX), xy)
#     return beta_hat

y_hat = np.dot(X, beta_hat)
error_hat = y_bar - y_hat
var_error = np.dot(error_hat.T, error_hat) / (n - k)
cov = np.linalg.inv(XX) * var_error
var_beta = np.diag(cov)
sd_beta = (var_beta ** (1 / 2)).reshape(4, 1)
t_stat = beta_hat / sd_beta

p_beta_hat = pd.DataFrame(beta_hat)
p_sd_beta = pd.DataFrame(sd_beta)
p_t_stat = pd.DataFrame(t_stat)

result_table = pd.DataFrame(beta_hat, index = ['beta0', 'beta1', 'beta2', 'beta3'], columns = ['Beta_hat'])
result_table['sd'] = pd.DataFrame(sd_beta, index = result_table.index)
result_table['t_stat'] = pd.DataFrame(t_stat, index = result_table.index)


# make scatter ploy maybe tomorrow
