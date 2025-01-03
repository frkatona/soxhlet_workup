import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


## load data ##
data = pd.read_csv('CSVs/241127_RLOvsLRO_SwellMassData_topside.csv')


## constants ##
phi_hexane = 0.39  # interaction parameter for hexane/PDMS
V_hexane_molar = 130.7  # molar volume for hexane (mL/mol)
rho_hexane = 0.659  # density of hexane, in g/cm^3 (have I seen this *1e-3?)
R = 8.3145  # universal gas constant (J/(mol·K))
T = 298.15  # absolute temperature (K)


## data processing ##
m_hexane = data['wash'] - data['pre-wash']  # mass of hexane absorbed (g)
V_hexane = m_hexane / rho_hexane  # volume absorbed by polymer (cm^3)
V_poly = data['pre-wash'] / (data['pre-wash'] + phi_hexane * V_hexane) # volume fraction of polymer


## determine crosslink density and modulus from polymer volume fraction ##
n = - (np.log(1-V_poly) + V_poly + phi_hexane * V_poly**2) / (V_hexane_molar * (V_poly**(1/3) - V_poly / 2)) * 1000  # 1000 for mol --> mmol
# n = - (np.log(1 - V_poly) + V_poly + phi_hexane * V_poly**2) / (V_hexane_molar * (V_poly**(1/3) - V_poly / 2)) 

E = 3 * n * R * T
E = E * 1e-3  # Convert E from Pa to kPa

data['n'] = n
data['E'] = E

data['gel fraction'] = data['post-dry'] / data['pre-wash'] * 100


## Plotting ##
# formatting
colors = ['#253d3d', '#296c58', '#1ea57a', '#59baa0', '#8b2317', '#c63030', '#c44846', '#e8746e',] 
fontsize = 30

# cross-link density
plt.figure(figsize=(10, 5))
plt.bar(data[r'sample'], data[r'n'], color=colors)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('crosslink density (mmol/cm³)', fontsize=fontsize)

# modulus
plt.figure(figsize=(10, 5))
plt.bar(data[r'sample'], data[r'E'], color=colors)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('elastic modulus (kPa)', fontsize=fontsize)

# gel fraction
plt.figure(figsize=(10, 5))
plt.bar(data[r'sample'], data[r'gel fraction'], color=colors)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('gel fraction (%)', fontsize=fontsize)

# show plots
plt.tight_layout()
plt.show()