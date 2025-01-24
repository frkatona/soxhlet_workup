import pandas as pd
import numpy as np

## Load data ##
data = pd.read_csv('rawdata/250123_RLOvsLRO_reformat.csv')

# Constants
phi_hexane = 0.39
V_hexane_molar = 130.7  # mL/mol
rho_hexane = 0.659  # g/cm³
R = 8.3145  # J/(mol·K)
T = 298.15  # K

## Data Processing ##
# Calculate individual crosslink density for each sample
m_hexane = data['wash'] - data['pre-wash']
V_hexane = m_hexane / rho_hexane
V_poly = data['pre-wash'] / (data['pre-wash'] + phi_hexane * V_hexane)

n = - (np.log(1 - V_poly) + V_poly + phi_hexane * V_poly**2) / (
        V_hexane_molar * (V_poly**(1 / 3) - V_poly / 2)) * 1000  # mmol/cm³

data['crosslink_density'] = n

## Save results to CSV ##
output_file = 'LRO-RLO_n-output.csv'
data[['sample', 'crosslink_density']].to_csv(output_file, index=False)

print(f"Crosslink density results for individual samples saved to {output_file}")
