# Title: CSE5539 Midterm Lab Fundamental frequency detection with correlogram
# Author: Yiran Lawrence Luo
# Date: Mar 1, 2016
# External libraries used: NumPy, Matplotlib

import numpy as np
import math
import matplotlib.pyplot as plt

def run():
	# The assumed channel frequencies in log scale
	freq = np.logspace(math.log(80), math.log(4000), base = math.exp(1), num=64)

	# Loads the .dat cell model file
	vowel_name = 'ar0'

	# Read the r(i, j) values
	cell_data = []
	with open(vowel_name + '.dat') as f:
	    for i in range(64):
	        temp_list = []
	        for j in range(325):
	            x = f.readline()
	            temp_list.append(float(x))
	        cell_data.append(temp_list)

	# Technically we are slicing at the very last time step,
	# which means j = 325 - 1
	j = 324
	channel_data_list = []
	for i in range(64):
	    channel_data = []
	    for l in range(125):
	        point = 0.0
	        for k in range(200):
	            # Calculate the auto-correlation value at this channel and this lag time
	            point += cell_data[i][j-k] * cell_data[i][j-k-l] * 0.02
	        # Offsets each line at above the assumed center frequency
	        channel_data.append(point/10000 + freq[i])
	        
	    # Plot the wave for each channel into the correlogram
	    plt.plot(range(125),channel_data,'r-')
	    channel_data_list.append(channel_data)



	plt.yscale('log')
	plt.axis([0, 125, 80, 4100])
	plt.yticks([80,216,584,1575,4000],[80,216,584,1575,4000])
	plt.xticks([0,25,50,75,100,125],[0,2.5,5.0,7.5,10.0,12.5])
	plt.title('Correlogram of ' + vowel_name)
	plt.ylabel('Channel center frequency (Hz)')
	plt.xlabel('Lag (msec)')
	plt.savefig(vowel_name + '.png')
	plt.close()

	# Now plot the pooled correlation values
	lag_list = []
	for l in range(125):
	    lag_sum = 0.5
	    for i in range(64):
	        lag_sum += channel_data_list[i][l]
	    lag_list.append(lag_sum)

	# Output at what lag time the correlation value hits the peak
	# Zero lag is omitted
	print "The max correlation is at lag time step:", 
	print lag_list.index(max(lag_list[1:]))

	plt.plot(range(125),lag_list,'r-')
	axes = plt.gca()
	axes.set_xlim([0, 125])
	plt.xticks([0,25,50,75,100,125],[0,2.5,5.0,7.5,10.0,12.5])
	plt.gca().yaxis.set_major_locator(plt.NullLocator())
	plt.title('Pooled Correlogram of ' + vowel_name)
	plt.xlabel('Lag (msec)')
	plt.savefig(vowel_name + '_pooled.png')

run()