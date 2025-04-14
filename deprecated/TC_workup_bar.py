import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv('CSVs/AuPDMS1_TC.csv')

# Calculate mean and standard deviation
df['mean_TC'] = df[['TC_1', 'TC_2', 'TC_3']].mean(axis=1)
df['std_TC'] = df[['TC_1', 'TC_2', 'TC_3']].std(axis=1)

# Sort dataframe alphabetically by sample
df_sorted = df.sort_values(by='sample')

# Create viridis color map
cmap = plt.get_cmap('viridis')
colors = cmap(np.linspace(0, 1, len(df_sorted)))

# Create bar plot with error bars
plt.figure(figsize=(12, 8))
bar = plt.bar(df_sorted['sample'], df_sorted['mean_TC'], yerr=df_sorted['std_TC'], 
              align='center', alpha=0.5, ecolor='black', capsize=10, color=colors)

plt.xlabel('oven-laser-oven times (min)', fontsize=16)
plt.ylabel('Thermal Conductivity (W/mK)', fontsize=16)
# plt.xticks(rotation='vertical')

plt.tight_layout()
plt.show()
