#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

#%%
# Load the data
file_path = 'CSVs/240529_PDMS_paper-revisions_durometer.csv'
df = pd.read_csv(file_path)

# Correcting the sample type extraction to the specific sample types
df['sample_type'] = df['sample'].str.extract(r'(ambient-pristine|ambient-1e-6|laser-1e-6)')[0]

# Remove rows with NaN in 'sample_type' if any
df = df.dropna(subset=['sample_type'])

# Convert 'sample_type' to a categorical type with ordered categories
df['sample_type'] = pd.Categorical(df['sample_type'], categories=df['sample_type'].unique(), ordered=True)

# Grouping the data by the corrected sample type and calculating mean and std
grouped_prefix_corrected = df.groupby('sample_type').agg({'hardness (Ha)': ['mean', 'std']}).reset_index()
grouped_prefix_corrected.columns = ['sample_type', 'Ha_mean', 'Ha_std']

#%%
# Plotting
fontsize = 20
plt.figure(figsize=(12, 8))
plt.bar(grouped_prefix_corrected['sample_type'], grouped_prefix_corrected['Ha_mean'], yerr=grouped_prefix_corrected['Ha_std'], capsize=5)
plt.ylabel('Hardness (Ha)', fontsize=fontsize)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))  # Set y-axis to scientific notation
plt.tight_layout()

# Post-hoc test (Tukey's HSD)
tukey = pairwise_tukeyhsd(endog=df['hardness (Ha)'], groups=df['sample_type'], alpha=0.05)
print("Tukey's HSD results:")
print(tukey)

# Plotting Tukey's HSD
tukey.plot_simultaneous()
plt.show()
# %%
