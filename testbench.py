import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
data = pd.read_csv('CSVs/241127_RLOvsLRO_SwellMassData_topside.csv')

# formatting
colors = ['#253d3d', '#296c6c', '#1f9595', '#52c4c4', '#1f5570', '#287499', '#1d86bb', '#1498da',] 
fontsize = 20

## Plotting
# swell
plt.figure(figsize=(10, 5))
plt.bar(data[r'sample'], data[r'swell%'], color=colors)
# plt.xlabel('sample', fontsize=fontsize)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('swell %', fontsize=fontsize)

# gel
plt.figure(figsize=(10, 5))
plt.bar(data[r'sample'], data[r'gel%'], color=colors)
# plt.xlabel('sample', fontsize=fontsize)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('gel %', fontsize=fontsize)

plt.tight_layout()
plt.show()