import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 14  # Adjust the value as needed

# Parameters for the normal distribution (mu and sigma for the normal)
mu = 0.0      # Mean of the normal distribution
sigma = 1.0   # Standard deviation of the normal distribution
N = 10        # Number of i.i.d. normal variables to sum
num_samples = 100000  # Number of samples to generate for estimation
num_bins = 10000  # Number of bins for the histogram

# Generate samples from the original normal distribution
original_samples = np.random.normal(loc=mu, scale=sigma, size=num_samples)

# Generate samples for the sum divided by N: create a 2D array of normal samples, sum along axis=1, and divide by N
sum_samples_array = np.random.normal(loc=mu, scale=sigma, size=(num_samples, N))
sum_samples = np.sum(sum_samples_array, axis=1) / N

# Determine the common x-axis range based on the combined data
x_min = -10 # min(original_samples.min(), sum_samples.min())
x_max = 10 # max(original_samples.max(), sum_samples.max())

# Plot the distributions using histograms (with density for probability distribution approximation)
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Original normal distribution
axs[0].hist(original_samples, bins=num_bins, density=True, alpha=0.6, color='green', range=(x_min, x_max))
axs[0].set_title('Original normal distribution')
axs[0].set_xlabel('Value')
axs[0].set_ylabel('Density')

# Distribution of the sum divided by N
axs[1].hist(sum_samples, bins=num_bins, density=True, alpha=0.6, color='blue', range=(x_min, x_max))
axs[1].set_title(f'Sum of {N} i.i.d. normals / {N}')
axs[1].set_xlabel('Value')
axs[1].set_ylabel('Density')

# Remove the top and right spines for both plots
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()

# Save the plot as a PNG file
plt.savefig('normal_distribution_plot.png', dpi=300)

#plt.show()