import matplotlib.pyplot as plt

# Set default font size
plt.rcParams.update({'font.size': 14})

# Data for Apple M4
m4_lanes = list(range(1, 41))
m4_bandwidth = [647, 1309, 1960, 2608, 3244, 3883, 4508, 5126, 5741, 6324, 6924, 7504, 8112, 8666, 9185, 9859, 10437, 11000, 11572, 12116, 12661, 13222, 13775, 14332, 14865, 15395, 15905, 16419, 15236, 15207, 14847, 15888, 16467, 16259, 16856, 17507, 17456, 17780, 18530, 18469]
m4_bandwidth = [2*x/1000 for x in m4_bandwidth]  # Double the M4 bandwidth values (128-bit cache line)

# Theoretical line y = 647x (scaled by 2/1000)
theoretical_lanes = list(range(1, 29))  # Match x limit of 28
theoretical_bandwidth = [1.294*x for x in theoretical_lanes]  # y = 647x * 2/1000 = 1.294x

# Plot 2: Number of lanes vs Bandwidth
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(m4_lanes, m4_bandwidth, label='M4', marker='s')
ax.plot(theoretical_lanes, theoretical_bandwidth, label='Theoretical y=647x', linestyle='--', color='black')
ax.set_xlabel('Number of lanes')
ax.set_ylabel('Bandwidth (GB/s)')
ax.set_title('Bandwidth vs number of lanes')
ax.set_xlim(left=0, right=28)
ax.legend(frameon=False)
ax.grid(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('bandwidth_vs_lanes_english.png')
plt.close()