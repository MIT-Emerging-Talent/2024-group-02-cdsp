import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Example data
data = sns.load_dataset("flights")
data = data.pivot_table(index="month", columns="year", values="passengers", aggfunc="sum")

# Another DataFrame with totals
totals = data.sum(axis=0)  # Sum of passengers for each year

# Create a heatmap for main data
sns.heatmap(data, annot=True, cmap='coolwarm', cbar=False, fmt='d')

# Create a heatmap for totals
sns.heatmap(totals.to_frame().T, annot=True, cmap='coolwarm', cbar=False, fmt='d', linewidths=.5, linecolor='black', alpha=0.1)

# Show plot
plt.imshow([[0]], cmap='coolwarm', alpha=0)  # workaround to display the plot correctly
plt.show()
