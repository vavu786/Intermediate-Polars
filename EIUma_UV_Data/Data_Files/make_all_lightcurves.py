# Script that creates lightcurves for all files in all subdirectories
# Script must be in same directory as the "EIUMa_UVT_" directories

import curvit
import os
import sys
from shutil import copy


count = 0

# Create a lightcurves directory only if not already created
if not os.path.isdir("lightcurves"):
    directory_of_lcs = "lightcurves"
    full_lc_directory_path = os.path.join(os.getcwd(), directory_of_lcs)
    os.mkdir(full_lc_directory_path)

# Only execute the script if there is a numeric command line argument
if sys.argv[1].isnumeric():

    # Takes in bin size as a command line argument
    binsize = int(sys.argv[1])

    # Iterates through all subdirectories and files in the current directory
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name.endswith('.fits'):
                print("Creating lightcurve for " + os.path.join(root, name) + " ...")
                curvit.curve(events_list = os.path.join(root, name), xp = 2750.00, yp = 2100.00, radius = 15, bwidth = binsize, background = 'auto')
                count = count + 1
    
    # The rest of the script just takes all the .png files that are the lightcurves and puts them all in one directory, so we can see all of them
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name.startswith("curve") and name.endswith('.png') and ("uvt" not in name[-10:-4]): 
                indexOfuvt = root.find("uvt_")
                newname = os.path.join(root, name[0:-4] + "_" + root[indexOfuvt:indexOfuvt + 6] + ".png")
                files.append(newname)
                os.rename(os.path.join(root, name), newname) 
                copy(newname, "lightcurves/")

    print("Created lightcurve for {} files".format(count))
else:
    print("Need an integer command line argument: Radius")

