import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Data
time = np.array([45, 65, 90, 110, 220])
conductivity = np.array([0.099686, 0.1002, 0.1006, 0.104, 0.10677])
error = np.array([0.0033505, 0.0031587, 0.0134487, 0.008101, 0.016897])

# Fitting function
def log_fit_func(x, a, b, c):
    return a + b * np.log(x + c)

# Curve fitting
popt_log, pcov_log = curve_fit(log_fit_func, time, conductivity, p0=(1, 1, 1), bounds=([-np.inf, -np.inf, -1], np.inf))

# Plotting the data
plt.figure(figsize=(10,6))
plt.errorbar(time, conductivity, yerr=error, fmt='o', label='data')
plt.plot(time, log_fit_func(time, *popt_log), 'g-', label=f'log fit: a={popt_log[0]:.5f}, b={popt_log[1]:.5f}, c={popt_log[2]:.5f}')
plt.xlabel('Time (minutes)')
plt.ylabel('Thermal Conductivity (W/mK)')
# plt.title('Thermal Conductivit    y vs Time (Logarithmic Fit)')
plt.legend()
plt.grid(True)
plt.show()
