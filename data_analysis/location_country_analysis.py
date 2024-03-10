
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'src/cleaned_tech_layoffs_data.csv' # Modify this path to your local file location
data = pd.read_csv(file_path)

# Top 10 layoff locations analysis
top_10_locations = data.groupby('Location HQ')['# Laid Off Numeric'].sum().sort_values(ascending=False).head(10)
print("Top 10 Layoff Locations:")
print(top_10_locations)

# Top countries by layoffs analysis
top_countries_layoffs = data.groupby('Country')['# Laid Off Numeric'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Countries by Layoffs:")
print(top_countries_layoffs)

# Plotting the top countries by layoffs
plt.figure(figsize=(10, 8))
top_countries_layoffs.plot(kind='barh', color='skyblue')
plt.xlabel('Total Layoffs')
plt.ylabel('Country')
plt.title('Top 10 Countries by Total Layoffs')
plt.gca().invert_yaxis()  # To display the country with the highest layoffs at the top
plt.show()
