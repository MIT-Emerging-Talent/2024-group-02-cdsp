# import for handling date periods
from pandas import Period

# Converting the 'Date' column to a period for month and year grouping
data['YearMonth'] = data['Date'].dt.to_period('M')

# Aggregate the total number of layoffs by year and month
monthly_layoffs = data.groupby('YearMonth')['# Laid Off Numeric'].sum().reset_index()
monthly_layoffs['YearMonth'] = monthly_layoffs['YearMonth'].dt.to_timestamp()  # Convert back to datetime for plotting

# Count the number of layoff events by year and month
monthly_events = data.groupby('YearMonth').size().reset_index(name='Events')
monthly_events['YearMonth'] = monthly_events['YearMonth'].dt.to_timestamp()  # Convert back to datetime for plotting
