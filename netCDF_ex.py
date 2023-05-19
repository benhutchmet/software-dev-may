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


# define a function called "is_valid"
# that takes (filename, lat, lon) as arguments
# checks that filename is a valid file path
# checks that lat and lon are valid coordinates between -90 and 90 and -180 and 180 respectively
# returns True if all are valid, False otherwise
# returns an error message if any of the checks fail
def is_valid(filename, lat, lon):
    """ 
    Checks that a file path and coordinates are valid.
    
    Parameters
    ----------
    filename : str
        Fully qualified pathname of a valid NetCDF file.
    lat : float
        Latitude coordinate to check.
    lon : float
        Longitude coordinate to check.

    Returns
    -------
    bool
        True if all checks pass, False otherwise.
    str
        Error message if any checks fail.
    """ 
    # check that filename is a valid file path
    if not op.exists(filename):
        return False, f"{filename} is not a valid file path"

    # check that lat and lon are valid coordinates between -90 and 90 and -180 and 180 respectively
    if lat < -90 or lat > 90:
        return False, f"{lat} is not a valid latitude"
    if lon < -180 or lon > 180:
        return False, f"{lon} is not a valid longitude"

    # return True if all are valid, False otherwise
    return True, None


# define a function called "extract_data"
# that takes (filename, lat, lon) as arguments
# and extracts the SST data at the given coordinates
# returns the extracted data
def extract_data(filename, lat, lon):
    """ 
    Extracts SST data at the given coordinates.
    
    Parameters
    ----------
    filename : str
        Fully qualified pathname of a valid NetCDF file.
    lat : float
        Latitude coordinate to extract data at.
    lon : float
        Longitude coordinate to extract data at.

    Returns
    -------
    data : float
        SST data at the given coordinates.
    """ 
    # load the file using xarray
    loaded = load_file(filename, "xarray")

    # show the information about the loaded file
    show_info(loaded)

    # extract the SST data at the given coordinates
    data = loaded.sel(lat=lat, lon=lon, method="nearest")["analysed_sst"].data

    # if the data is not empty, then print it
    if data: 
        print(f"SST at {lat}, {lon} is {data}")
    else:
        print(f"No data at {lat}, {lon}. Likely land.")
        # exit the program if there is no data
        # tell the user that there is no data
        print("Exiting program")
        exit()

    # return the extracted data
    return data

def main_program(file_path, lat, lon):
    """Checks that a file path and coordinates are valid and extracts SST data at the given coordinates.

    Parameters
    ----------
    file_path : str
        Fully qualified pathname of a valid NetCDF file.
    lat : float
        Latitude coordinate to extract data at.
    lon : float
        Longitude coordinate to extract data at.

    Returns
    -------
    None
    """
    # check that the file path and coordinates are valid
    valid, error = is_valid(file_path, lat, lon)

    # if they are valid, then extract the data
    if valid:
        extract_data(file_path, lat, lon)
    else:
        # if they are not valid, then print an error message
        print(error)
        # exit the program if there is an error
        print("Exiting program")
        exit()

# call main program
if __name__ == '__main__': 
    
    # define the file path
    polcoms_file = "/workspaces/software-dev-may/data/polcoms.nc"
    GHR_file = "/workspaces/software-dev-may/data/20100601120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_LT-v02.0-fv01.0.nc"

    # define the coordinates
    lat = 50.0
    lon = -10.0

    # define invalid coordinates
    invalid_lat = 100.0
    invalid_lon = 200.0

    #main_program(GHR_file, lat, lon)

    main_program(GHR_file, invalid_lat, invalid_lon)
