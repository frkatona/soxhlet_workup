import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

# Load the data
df = pd.read_csv('CSVs/AuPDMS2.csv',  header = 0)    
x_label = 'oven-laser-oven times (min)'

# Define the constants
phi_hexane = 0.39  
V_hexane_molar = 130.7 # mL/mol 
p_hexane = 0.661 # g/mL
R = 8.3145 # J/mol K
T = 298.15  # K

# Calculate mass of hexane absorbed by the polymer
M_hexane = df['wash'] - df['pre-wash']

# Calculate volume of hexane absorbed by the polymer
V_hexane = M_hexane / p_hexane

# Calculate polymer volume fraction
V_poly = df['pre-wash'] / (df['pre-wash'] + phi_hexane * V_hexane)

# Calculate n for each sample
n = - (np.log(1 - V_poly) + V_poly + phi_hexane * V_poly**2) / (V_hexane_molar * (V_poly**(1/3) - V_poly / 2))

# Calculate E in MPa for each sample (cm³ -> m³ -> MPa)
E = 3 * n * R * T

# Add the calculated n, E, and V_poly to the dataframe
df['n'] = n
df['E'] = E
df['V_poly'] = V_poly

# Extract the group name from the sample name through .split if needed
df['group'] = df['sample']

# Calculate the average and standard deviation for each group
numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
grouped = df.groupby('group')[numerical_columns].agg(['mean', 'std'])

# Plot the bar plot for crosslink density and elastic modulus
fig, ax1 = plt.subplots()
colors = plt.cm.viridis(np.linspace(0, 1, len(grouped.index)))  
sns.barplot(x=grouped.index, y=grouped['n']['mean'], yerr=grouped['n']['std'], ax=ax1, capsize=0.1, palette=colors)
ax1.set_ylabel('Average Crosslink Density (mol/cm³)')

# Create a second y-axis that shares the same x-axis
ax2 = ax1.twinx()
sns.barplot(x=grouped.index, y=grouped['E']['mean'], yerr=grouped['E']['std'], ax=ax2, capsize=0.1, palette=colors, alpha=0.5)
ax2.set_ylabel('Elastic Modulus (MPa)')

ax1.set_xlabel(x_label, fontsize=16)
plt.show()


# # Plot the bar plot for elastic modulus
# fig2, ax2 = plt.subplots()
# sns.barplot(x=grouped.index, y=grouped['E']['mean'], yerr=grouped['E']['std'], ax=ax2, capsize=0.1, palette=colors)
# ax2.set_ylabel('Elastic Modulus (MPa)')
# ax2.set_xlabel(x_label, fontsize=16)
# # ax2.set_title('Average Elastic Modulus by Group')
# plt.show()

fig, ax = plt.subplots()
sns.barplot(x=grouped['V_poly']['mean'].index, y=grouped['V_poly']['mean'], yerr=grouped['V_poly']['std'], ax=ax, capsize=0.1, palette=colors)
ax.set_ylabel('Average Polymer Volume Fraction')
ax.set_xlabel(x_label, fontsize=16)
# ax.set_title('Average Polymer Volume Fraction by Group')
plt.show()

# Scatterplot and trendline
z = np.polyfit(range(len(grouped.index)), grouped['n']['mean'], 1)
p = np.poly1d(z)
r_squared = np.corrcoef(range(len(grouped.index)), grouped['n']['mean'])[0, 1]**2

fig, ax = plt.subplots()
sns.scatterplot(x=range(len(grouped.index)), y=grouped['n']['mean'], ax=ax, color='b')
x_trendline = np.linspace(0, len(grouped.index)-1, 100)
y_trendline = p(x_trendline)

ax.plot(x_trendline, y_trendline, color='r')
ax.set_xlabel(x_label, fontsize=16)
ax.set_xticks(range(len(grouped.index)))
ax.set_xticklabels(grouped.index, rotation=45)
ax.set_ylabel('Crosslink Density (mol/cm³)')
# ax.set_title('Crosslink Density by Sample')
eq_text = "y = {:.3f}x + {:.3f}, $r^2$ = {:.3f}".format(z[0], z[1], r_squared)
plt.text(0.05, 0.95, eq_text, transform=ax.transAxes, fontsize=12, verticalalignment='top')
plt.show()

print(df)