import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 22})

# Data from the table
sizes = [1048576, 524288, 262144, 131072, 65536, 32768, 16384, 8192, 4096, 2048]
cycles_per_value = [7.20, 6.76, 5.90, 3.43, 2.20, 2.19, 2.12, 2.10, 2.00, 1.85]
# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(sizes, cycles_per_value, 'bo-', markersize=8, linewidth=2)

# Set logarithmic scale for x-axis
plt.xscale('log')

for i, size in enumerate(sizes):
    if(i % 2 == 1):
        continue
    plt.text(size, cycles_per_value[i] + 0.2, f'{size:,}', ha='center', va='bottom')

# Customize the plot
plt.xlabel('Size')
plt.ylabel('Cycles per value')
#plt.title('Size vs cycles per value')
plt.grid(True, which="both", ls="--")

# Invert x-axis to have smaller sizes on the right
plt.gca().invert_xaxis()

# Save the plot as PNG
plt.tight_layout()
plt.savefig('size_vs_cycles_english.png', dpi=300, bbox_inches='tight')
plt.close()
