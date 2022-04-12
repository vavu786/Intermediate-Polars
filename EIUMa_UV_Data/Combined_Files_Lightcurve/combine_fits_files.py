from astropy.table import Table, vstack
import os

all_fits_files = []
all_fits_tables = []
all_fits_length = 0;
for root, dirs, files in os.walk("../Combined_Files_Lightcurve/", topdown=False):
        for name in files:
            if name.endswith('.fits'):
                all_fits_files.append(os.path.join(root, name))

print(all_fits_files)

# t1 = Table.read('./EIUMa_UVIT_A/RAS_VIS/uvt_01/F_01/AS1A10_073T05_9000004068uvtFIIPC00F1_l2ce.fits', format='fits')
# t2 = Table.read('file2.fits', format='fits')

for i, fits_file in enumerate(all_fits_files):
    t1 = Table.read(all_fits_files[i], format='fits')
    all_fits_length = all_fits_length + len(t1)
    all_fits_tables.append(t1)

combined_fits_file = vstack(all_fits_tables)
combined_fits_file.write("uvt01_through_14.fits")

print("{} = {}".format(all_fits_length, len(combined_fits_file)))


