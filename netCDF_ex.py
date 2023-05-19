import netCDF4 as nc 

import os.path as op 

import xarray as xr

print("hello")

def load_netcdf(file): 

    """ 

    Read file using netcdf library 

    :param file: fully quaified pathname of valid nc file 

    :return: loaded data 

    """ 

    dataset = nc.Dataset(file) 

    return dataset 

  

def load_xarray(file): 

    """ 

    Read file using xarray library 

    :param file: fully quaified pathname of valid nc file 

    :return: loaded data 

    """ 

    the_xarray = xr.open_dataset(file) 

    return the_xarray 

  

def load_file(file, how): 

    """ 

    Given the file and how to load it, do it 

    :param file: fully quaified pathname of valid nc file 

    :param how: can be "netcdf", "xarray" 

    :return: loaded data 

    """ 

    if how == "netcdf": 

        loaded = load_netcdf(file) 

    elif how == "xarray": 

        loaded = load_xarray(file) 

    return loaded 

  

def show_info(loaded): 

    """ 

    Print out various dataset information depending on its type 

    :param loaded: 

    :return: n/a 

    """ 

    if type(loaded) is nc.Dataset: 

        print("====================NETCDF=====================") 

        print(loaded.variables) 

        print(loaded.dimensions) 

    elif type(loaded) is xr.Dataset: 

        print("====================XARRAY=====================") 

        print(loaded.variables) 

        print(loaded.attrs) 

        print(loaded.coords) 

def main_program(): 

    file = op.normpath("/home/jane/Documents/06_ReSC_data/polcoms.nc") 

    loaded = load_file(file, "netcdf") 

    show_info(loaded) 

    loaded = load_file(file, "xarray") 

    show_info(loaded) 

  

    file = op.normpath("/home/jane/Documents/06_ReSC_data/20100601120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_LT-v02" 

                       ".0-fv01.0.nc") 

    loaded = load_file(file, "netcdf") 

    show_info(loaded) 

  

if __name__ == '__main__': 

    main_program()