import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 14})

# Data from the table
years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
transistors = [1, 2, 2, 3.2, 4.3, 6.9, 8.5, 11.8, 15, 16, 19]  # in billions
processors = ['Apple A7', 'Apple A8', 'Apple A9', 'Apple A10', 'Apple A11', 
              'Apple A12', 'Apple A13', 'Apple A14', 'Apple A15', 'Apple A16', 'Apple A17']

# Normalize years for numerical stability in fitting
year_normalized = np.array(years) - 2013
transistors = np.array(transistors)

# Fit exponential curve: log(transistors) = b * year + log(a)
# This gives transistors = a * exp(b * year)
coeffs = np.polyfit(year_normalized, np.log(transistors), 1)
b, log_a = coeffs
a = np.exp(log_a)

# Calculate percentage gain per year
percent_gain = (np.exp(b) - 1) * 100
print(f"Annual percentage gain in transistor count: {percent_gain:.0f}%")

# Generate points for the exponential trend line
trend_years = np.linspace(0, 10, 100)  # Normalized years from 0 to 10 (2013 to 2023)
trend_transistors = a * np.exp(b * trend_years)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(years, transistors, 'bo-', markersize=8, linewidth=2, label='Data points')

# Plot exponential trend line
plt.plot(trend_years + 2013, trend_transistors, 'r--', 
         label=f'Exponential trend ({percent_gain:.0f}%/year)')

# Add labels for each point
for i, processor in enumerate(processors):
    plt.text(years[i], transistors[i] + 0.5, processor, ha='center', va='bottom')

# Customize the plot
plt.xlabel('Year')
plt.ylabel('Number of transistors (billions)')
plt.title('Year vs number of transistors')
plt.grid(True, which="both", ls="--")
plt.legend()

# Set x-axis ticks to show every year
plt.xticks(years)

# Save the plot as PNG
plt.tight_layout()
plt.savefig('transistors_vs_years_exponential.png', dpi=300, bbox_inches='tight')
plt.close()