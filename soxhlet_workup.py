import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

# Load the data
df = pd.read_csv(r'CSVs\240506_CB-PDMS-paper-revisions.csv',  header = 0)    
# x_label = 'oven-laser-oven times (min)'

# Define the constants
phi_hexane = 0.39  
V_hexane_molar = 130.7 # mL/mol 
p_hexane = 0.661 # g/mL
R = 8.3145 # J/mol K
T = 298.15  # K

M_hexane = df['wash'] - df['pre-wash']
V_hexane = M_hexane / p_hexane
V_poly = df['pre-wash'] / (df['pre-wash'] + phi_hexane * V_hexane)

n = - (np.log(1 - V_poly) + V_poly + phi_hexane * V_poly**2) / (V_hexane_molar * (V_poly**(1/3) - V_poly / 2))
E = 3 * n * R * T # ~ 7000 * n

df['n'] = n
df['E'] = E
df['V_poly'] = V_poly
df['group'] = df['sample']

# # Statistical analysis (for repeated measures)
# numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
# df = df.groupby('group')[numerical_columns].agg(['mean', 'std']).reset_index()

# Plotting
fontsize = 20
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='sample', y='n', data=df, ax=ax, ci='sd')
plt.xlabel('', fontsize=fontsize)
plt.ylabel('n (mol/mL)', fontsize=fontsize)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.tight_layout()
plt.show()