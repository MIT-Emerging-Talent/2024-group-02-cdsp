import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('cleaned_tech_layoffs_data.csv')

# Grouping the data by Industry and Year, then summing the number of laid off employees
heatmap_data = df.groupby(['Industry', 'Year'])['# Laid Off Numeric'].sum().unstack(fill_value=0)

# Adding a 'Total' column for the sum of layoffs across all years for each industry
heatmap_data['Total'] = heatmap_data.sum(axis=1)

# Sorting industries by the total number of laid off employees in descending order
heatmap_data_sorted_with_total = heatmap_data.sort_values('Total', ascending=False)

# Creating the heatmap 
plt.figure(figsize=(12, 10))
sns.heatmap(heatmap_data_sorted_with_total, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=1.0)
plt.title('Number of Employees Laid Off by Industry and Year (Including Totals)')
plt.xlabel('Year')
plt.ylabel('Industry')
plt.tight_layout() 
plt.show()
