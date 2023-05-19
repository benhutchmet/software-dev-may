import os.path as op 
import netCDF4 as nc 
import xarray as xr

def load_netcdf(file): 
    """ 
    Loads a NetCDF file.
    
    Parameters
    ----------
    file : str
        Fully qualified pathname of a valid NetCDF file.

    Returns
    -------
    dataset : netCDF4.Dataset
        Loaded data from the file.
    """ 
    dataset = nc.Dataset(file) 
    return dataset 

def load_xarray(file): 
    """ 
    Loads a NetCDF file using xarray.
    
    Parameters
    ----------
    file : str
        Fully qualified pathname of a valid NetCDF file.

    Returns
    -------
    the_xarray : xarray.Dataset
        Loaded data from the file.
    """ 
    the_xarray = xr.open_dataset(file) 
    return the_xarray 

def load_file(file, how): 
    """ 
    Loads a file based on a specified method.
    
    Parameters
    ----------
    file : str
        Fully qualified pathname of a valid NetCDF file.
    how : str
        Method to load the file, can be "netcdf" or "xarray".

    Returns
    -------
    loaded : netCDF4.Dataset or xarray.Dataset
        Loaded data from the file.
    """ 
    if how == "netcdf": 
        loaded = load_netcdf(file) 
    elif how == "xarray": 
        loaded = load_xarray(file) 

    return loaded 

def show_info(loaded): 
    """ 
    Prints various dataset information depending on its type.

    Parameters
    ----------
    loaded : netCDF4.Dataset or xarray.Dataset
        Loaded dataset to show information about.

    Returns
    -------
    None
    """ 
    if isinstance(loaded, nc.Dataset): 
        print("====================NETCDF=====================") 
        print(loaded.variables) 
        print(loaded.dimensions) 
    elif isinstance(loaded, xr.Dataset): 
        print("====================XARRAY=====================") 
        print(loaded.variables) 
        print(loaded.attrs) 
        print(loaded.coords) 

def main_program(): 
    """ 
    Main program function to load and display information about datasets.
    
    Returns
    -------
    None
    """ 
    # set up file paths
    file_path_1 = "/workspaces/software-dev-may/data/polcoms.nc"
    file_path_2 = "/workspaces/software-dev-may/data/20100601120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_LT-v02.0-fv01.0.nc"

    # load each of the files using both methods
    for file in [file_path_1, file_path_2]:
        file = op.normpath(file) 

        # first uses netCDF4, second uses xarray
        for method in ["netcdf", "xarray"]:
            loaded = load_file(file, method)
            show_info(loaded) 

# call main program
if __name__ == '__main__': 
    main_program()
