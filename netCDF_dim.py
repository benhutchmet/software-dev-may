# import the relevant libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs

# use xarray to open the netCDF file
# define the file path
file_path = "/workspaces/software-dev-may/data/20100601120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_LT-v02.0-fv01.0.nc"

# open the file using xarray
# divide into chunks to reduce memory usage
ds = xr.open_dataset(file_path, chunks={'time': 1})

# have a look at the dataset
ds.info()