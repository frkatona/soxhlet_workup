import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_for_plot = pd.DataFrame({
    "sample": [
        "LRO_center-1", "LRO_center-2", "LRO_center-3",
        "LRO_inner-lip-1", "LRO_inner-lip-2", "LRO_inner-lip-3",
        "LRO_lip-1", "LRO_lip-2", "LRO_lip-3",
        "LRO_bulk-1", "LRO_bulk-2", "LRO_bulk-3",
        "RLO_center-1", "RLO_center-2", "RLO_center-3",
        "RLO_inner-lip-1", "RLO_inner-lip-2", "RLO_inner-lip-3",
        "RLO_lip-1", "RLO_lip-2", "RLO_lip-3",
        "RLO_bulk-1", "RLO_bulk-2", "RLO_bulk-3"
    ],
    "crosslink_density": [
        3.08882507756363, 4.517625912836021, 3.7574150633160426,
        4.060727711122752, 4.015554402756879, 4.047812149059153,
        4.358049327794311, 4.313186520814997, 4.297026502116161,
        4.515905084837487, 4.54856361086825, 4.388866594500977,
        4.581015566212249, 4.399963087749691, 4.424247310742694,
        4.371468747090563, 4.289512646374745, 4.415945555020074,
        4.4143574857399495, 4.39404337905261, 4.3062473568578366,
        4.36863753285699, 4.4152640165595605, 4.397466681901262
    ]
})

# Define the desired order
order = [
    "LRO_center", "LRO_inner", "LRO_lip", "LRO_bulk",
    "RLO_center", "RLO_inner", "RLO_lip", "RLO_bulk"
]

# Group by sample category (e.g., "LRO_center")
data_for_plot['category'] = data_for_plot['sample'].str.extract(r'(LRO_[a-z]+|RLO_[a-z]+)')

grouped = data_for_plot.groupby('category')['crosslink_density'].agg(['mean', 'std']).reset_index()

# Sort by the desired order
grouped['category'] = pd.Categorical(grouped['category'], categories=order, ordered=True)
grouped = grouped.sort_values('category')

# Pre-set list of 8 colors
colors = ['#11281b', '#296c58', '#39b38c', '#64c5ab', '#8b2317', '#c63030', '#c44846', '#e8746e']

fontsize = 16

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(grouped['category'], grouped['mean'], c=colors, s=100, alpha=0.7)
plt.errorbar(grouped['category'], grouped['mean'], yerr=grouped['std'], fmt='o', color='black', capsize=5, alpha=0.7)
plt.xticks(rotation=45, fontsize=fontsize)
plt.yticks(fontsize=14)
plt.ylabel('Crosslink Density (mmol/cm³)', fontsize=fontsize)
plt.tight_layout()
plt.show()
