import odbc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import curvefit as cf
from sklearn.metrics import mean_squared_error, r2_score
from scipy.optimize import curve_fit

# Define exponential decay function
def exponential_decay(x, a, b):
    return a * np.exp(b * x)


def exponentRun (dict):
# Mapping the levels to a numerical scale for fitting

    x_values = np.array(list(dict.keys()))
    y_values = np.array(list(dict.values()))

    # Fit the exponential decay model to the data
    params, covariance = curve_fit(exponential_decay, x_values, y_values, p0=[max(y_values), -1])

    # Extract fitted parameters
    a_fit, b_fit = params

    # Use the fitted model to predict frequencies for each differential
    predicted = exponential_decay(x_values, a_fit, b_fit)

    actual_values = np.array(list(dict.values()))
    predicted_values = np.array(predicted)
        
        # Calculate R-squared
    r_squared = r2_score(actual_values, predicted_values)
    print(f'R-squared: {r_squared}')

        # Calculate MSE and RMSE
    mse = mean_squared_error(actual_values, predicted_values)
    rmse = np.sqrt(mse)
    print(f'MSE: {mse}, RMSE: {rmse}')

    print("Fit Results:")
    print(f"Parameter a (initial value): {a_fit:.4f}")
    print(f"Parameter b (growth rate): {b_fit:.4f}")
    print("\nPredicted Frequencies:")
    for level, freq in enumerate(predicted_values, start=1):
        print(f"Level {7 - 2 * (level - 1)}: {freq:.2f}")

    print(f'Actual values: {actual_values}')
    
    print("\nCovariance Matrix:")
    print(f"[[{covariance[0, 0]:.6f}, {covariance[0, 1]:.6f}]")
    print(f" [{covariance[1, 0]:.6f}, {covariance[1, 1]:.6f}]]")

    return a_fit, b_fit, predicted, covariance
