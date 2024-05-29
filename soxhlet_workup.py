#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Constants
phi_hexane = 0.39  # dimensionless
V_hexane_molar = 130.7  # mL/mol 
p_hexane = 0.661  # g/mL
R = 8.3145  # J/mol K
T = 298.15  # K

#%%
# Load the data
file_path = 'CSVs/240529_PDMS_paper-revisions.csv'
df = pd.read_csv(file_path)

# Calculations
M_hexane = df['wash'] - df['pre-wash']
V_hexane = M_hexane / p_hexane
V_poly = df['pre-wash'] / (df['pre-wash'] + phi_hexane * V_hexane)

n = - (np.log(1 - V_poly) + V_poly + phi_hexane * V_poly**2) / (V_hexane_molar * (V_poly**(1/3) - V_poly / 2)) * 1000  # 1000 for mol --> mmol
E = 3 * n * R * T  # modulus = ~7000 * n

df['n'] = n
df['E'] = E
df['V_poly'] = V_poly

# Correcting the sample type extraction to the specific sample types
df['sample_type'] = df['sample'].str.extract(r'(ambient-pristine|ambient-1e-6|laser-1e-6)')[0]

# Remove rows with NaN in 'sample_type' if any
df = df.dropna(subset=['sample_type'])

# Convert 'sample_type' to a categorical type with ordered categories
df['sample_type'] = pd.Categorical(df['sample_type'], categories=df['sample_type'].unique(), ordered=True)

# Grouping the data by the corrected sample type and calculating mean and std
grouped_prefix_corrected = df.groupby('sample_type').agg({'n': ['mean', 'std']}).reset_index()
grouped_prefix_corrected.columns = ['sample_type', 'n_mean', 'n_std']

#%%
# Plotting
fontsize = 20
plt.figure(figsize=(12, 8))
plt.bar(grouped_prefix_corrected['sample_type'], grouped_prefix_corrected['n_mean'], yerr=grouped_prefix_corrected['n_std'], capsize=5)
plt.ylabel('Crosslink Density (mmol/cm^3)', fontsize=fontsize)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))  # Set y-axis to scientific notation
plt.tight_layout()

# Post-hoc test (Tukey's HSD)
tukey = pairwise_tukeyhsd(endog=df['E'], groups=df['sample_type'], alpha=0.05)
print("Tukey's HSD results:")
print(tukey)

# Plotting Tukey's HSD
tukey.plot_simultaneous()
plt.show()
# %%
