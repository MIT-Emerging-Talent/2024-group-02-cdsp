import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'src/cleaned_tech_layoffs_data.csv'  # Modify this path to your local file location
data = pd.read_csv(file_path)

# Analysis for top 10 layoff locations
top_10_locations = data.groupby('Location HQ')['# Laid Off Numeric'].sum().sort_values(ascending=False).head(10)

# Plotting the top 10 layoff locations
plt.figure(figsize=(10, 8))
top_10_locations.plot(kind='barh', color='lightcoral')
plt.xlabel('Total Layoffs')
plt.ylabel('Location HQ')
plt.title('Top 10 Layoff Locations')
plt.gca().invert_yaxis()  # To display the location with the highest layoffs at the top
plt.show()
