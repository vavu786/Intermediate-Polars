import os
from astropy.table import Table

def main():
    all_fits_files = []
    all_photon_rates = []
    all_file_numbers = []
    full_path = "/home/hamza/Schlegel_Files/Intermediate-Polars/EIUMa_UV_Data/"

    for root, dirs, files in os.walk(full_path + "Data_Files/", topdown=False):
        for name in files:
            if name.endswith('.fits'):
                all_fits_files.append(os.path.join(root, name))
    
    for f in all_fits_files:
        dat = Table.read(f, format="fits")
        df = dat.to_pandas()

        photons_per_time = sum(df["EFFECTIVE_NUM_PHOTONS"].to_numpy()) / (df["Time"].to_numpy()[-1] - df["Time"].to_numpy()[0])
        all_photon_rates.append(photons_per_time)
        
        index_of_num = f.find("uvt") + 4
        all_file_numbers.append(int(f[index_of_num]+f[index_of_num+1]))

    for photon_rate, num in zip(all_photon_rates, all_file_numbers):
        print(f"{photon_rate} {num}")

if __name__ == "__main__":
    main()
