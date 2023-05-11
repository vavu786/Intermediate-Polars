from astropy.io import fits
import pandas as pd
import numpy as np

sxt_pha_filename = "EIUma_spectrum.pha"
laxpc_pha_filename = "lxp2level2.spec"

with fits.open(laxpc_pha_filename) as data:
	df = pd.DataFrame(data[1].data)

counts = df["COUNTS"].to_numpy()
print([i for i in counts])

num_values = np.size(counts)
num_zeros = num_values - np.count_nonzero(counts)

print(str(num_zeros) + " out of " + str(num_values) + " are 0.")
for i, num in enumerate(counts):
	if num != 0:
		print("First non-zero item is at index " + str(i) + ".")
		break

for i, num in enumerate(counts[::-1]):
	if num != 0:
		print("Last non-zero item is at index " + str(num_values-i-1) + ".")
		break


print(counts[18])
print(counts[1019])
