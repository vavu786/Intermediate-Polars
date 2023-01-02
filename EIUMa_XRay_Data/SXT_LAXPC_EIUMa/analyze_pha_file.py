from astropy.io import fits
import pandas as pd
import numpy as np

with fits.open("EIUma_spectrum.pha") as data:
	df = pd.DataFrame(data[1].data)

counts = df["COUNTS"].to_numpy()
print([i for i in counts])
print(np.size(counts) - np.count_nonzero(counts))
