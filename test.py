import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs

# write a function which prints the sum of two numbers
def sum(a,b):
    # write a docstring
    """ This function returns the sum of two numbers """
    # print the types of a and b
    print(type(a))
    print(type(b))
    return a+b

print(sum(1,2))
