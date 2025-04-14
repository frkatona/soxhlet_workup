import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

## Load data ##
data = pd.read_csv('rawdata/250123_RLOvsLRO_reformat.csv')

## Extract sample base names ##
data['sample_base'] = data['sample'].str.extract(r'(LRO_[a-z-]+|RLO_[a-z-]+)')

# Group by the sample base and calculate means and standard deviations
numeric_columns = ['pre-wash', 'wash', 'post-dry']
grouped = data.groupby('sample_base')[numeric_columns].agg(['mean', 'std'])
grouped.columns = ['_'.join(col) for col in grouped.columns]  # Flatten MultiIndex
grouped.reset_index(inplace=True)

# Constants
phi_hexane = 0.39
V_hexane_molar = 130.7  # cm³/mol
rho_hexane = 0.659  # g/cm³
R = 8.3145  # J/(mol·K)
T = 298.15  # K

## Data Processing ##
# Calculate mean values
m_hexane_mean = grouped['wash_mean'] - grouped['pre-wash_mean']
V_hexane_mean = m_hexane_mean / rho_hexane
V_poly_mean = grouped['pre-wash_mean'] / (grouped['pre-wash_mean'] + phi_hexane * V_hexane_mean)

n_mean = - (np.log(1 - V_poly_mean) + V_poly_mean + phi_hexane * V_poly_mean**2) / (
        V_hexane_molar * (V_poly_mean**(1 / 3) - V_poly_mean / 2)) * 1000
E_mean = 3 * n_mean * R * T * 1e-3  # Convert to kPa
gel_fraction_mean = grouped['post-dry_mean'] / grouped['pre-wash_mean'] * 100

# Propagate standard deviations
m_hexane_std = np.sqrt(grouped['wash_std']**2 + grouped['pre-wash_std']**2)
V_hexane_std = m_hexane_std / rho_hexane
V_poly_std = np.sqrt(
    (grouped['pre-wash_std'] / grouped['pre-wash_mean'])**2 +
    (phi_hexane * V_hexane_std / (grouped['pre-wash_mean'] + phi_hexane * V_hexane_mean))**2
) * V_poly_mean

# Approximate std propagation for n and E
n_std = np.abs(n_mean) * V_poly_std / V_poly_mean
E_std = 3 * R * T * 1e-3 * n_std
gel_fraction_std = np.sqrt(
    (grouped['post-dry_std'] / grouped['post-dry_mean'])**2 +
    (grouped['pre-wash_std'] / grouped['pre-wash_mean'])**2
) * gel_fraction_mean

grouped['n_mean'] = n_mean
grouped['n_std'] = n_std
grouped['E_mean'] = E_mean
grouped['E_std'] = E_std
grouped['gel_fraction_mean'] = gel_fraction_mean
grouped['gel_fraction_std'] = gel_fraction_std

## Plotting ##
# Formatting
fontsize = 16
colors = ['#11281b', '#296c58', '#39b38c', '#64c5ab', '#8b2317', '#c63030', '#c44846', '#e8746e']

# Crosslink density with error bars
plt.figure(figsize=(10, 5))
plt.bar(grouped['sample_base'], grouped['n_mean'], yerr=grouped['n_std'], capsize=5, color=colors, alpha=0.7)
plt.xticks(rotation=45, fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('Crosslink Density (mmol/cm³)', fontsize=fontsize)
plt.tight_layout()
plt.show()

# Elastic modulus with error bars
plt.figure(figsize=(10, 5))
plt.bar(grouped['sample_base'], grouped['E_mean'], yerr=grouped['E_std'], capsize=5, color=colors, alpha=0.7)
plt.xticks(rotation=45, fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('Elastic Modulus (kPa)', fontsize=fontsize)
plt.tight_layout()
plt.show()

# Gel fraction with error bars
plt.figure(figsize=(10, 5))
plt.bar(grouped['sample_base'], grouped['gel_fraction_mean'], yerr=grouped['gel_fraction_std'], capsize=5, color=colors, alpha=0.7)
plt.xticks(rotation=45, fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('Gel Fraction (%)', fontsize=fontsize)
plt.tight_layout()
plt.show()
