#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Constants
phi_hexane = 0.39  # Flory interaction parameter (unique to system), dimensionless
V_hexane_molar = 130.7  # molar volume, mL/mol 
p_hexane = 0.661  # density of hexane, g/mL
R = 8.3145  # gas constant, J/mol K
T = 298.15  # absolute temp, K

#%%
# Load the data
file_path = 'CSVs/240529_PDMS_hexanes_revisions.csv'
df = pd.read_csv(file_path)

# Calculations
df['diff'] = df['pre-wash'] - df['post-dry']
df['gelFraction'] = 1 - (df['diff'] / df['pre-wash'])
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

# Grouping the data by the corrected sample type and calculating mean and std of the difference
grouped_diff = df.groupby('sample_type')['gelFraction'].agg(['mean', 'std']).reset_index()
grouped_diff.columns = ['sample_type', 'diff_mean', 'diff_std']

# Plotting
plt.figure(figsize=(12, 8))
fontsize = 20
bar_width = 0.35  # Width of each bar
x_pos_prefix_corrected = np.arange(len(grouped_prefix_corrected['sample_type']))
x_pos_diff = x_pos_prefix_corrected + bar_width

plt.bar(x_pos_prefix_corrected, grouped_prefix_corrected['n_mean'], yerr=grouped_prefix_corrected['n_std'], capsize=5, width=bar_width, label='Crosslink Density')
plt.bar(x_pos_diff, grouped_diff['diff_mean'], yerr=grouped_diff['diff_std'], capsize=5, width=bar_width, label='Difference (Pre-wash - Post-dry)')
plt.ylabel('Crosslink Density (mmol/cm^3)', fontsize=fontsize)
plt.xticks(x_pos_prefix_corrected + bar_width/2, grouped_prefix_corrected['sample_type'], fontsize=fontsize)  # Set x-axis positions and labels
plt.yticks(fontsize=fontsize)
plt.legend(fontsize=fontsize)
plt.tight_layout()
plt.show()

# Difference test (Tukey's HSD)
tukey_n = pairwise_tukeyhsd(endog=df['n'], groups=df['sample_type'], alpha=0.05)
tukey_diff = pairwise_tukeyhsd(endog=df['diff'], groups=df['sample_type'], alpha=0.05)
print("Tukey's HSD results:")
print("Crosslink Density:")
print(tukey_n)
print("Gel Fraction:")
print(tukey_diff)

# Plotting Tukey's HSD
# tukey.plot_simultaneous()
plt.show()