import os.path as op 
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

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
    #show_info(loaded)

    # extract the SST data at the given coordinates
    data = loaded.sel(lat=lat, lon=lon, method="nearest")["analysed_sst"].data

    # extract the SST error at the given coordinates
    error = loaded.sel(lat=lat, lon=lon, method="nearest")["analysis_error"].data

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

def main_program(file_path, lat, lon, how="point"):
    """Checks that a file path and coordinates are valid and extracts SST data at the given coordinates.

    Parameters
    ----------
    file_path : str
        Fully qualified pathname of a valid NetCDF file.
    lat : float
        Latitude coordinate to extract data at.
    lon : float
        Longitude coordinate to extract data at.
    how : str
        Method to load the file, can be "point" or "line". Defaults to "point".

    Returns
    -------
    None
    """
    # check that the file path and coordinates are valid
    valid, error = is_valid(file_path, lat, lon)

    # if they are valid, then extract the data
    if valid:
        if how == "point":
            extract_data(file_path, lat, lon)
        elif how == "line":
            # initialise an empty list to store the data
            data = []
            # initialise an empty list to store the error
            error = []
            # initialise an empty list to store the latitude
            lat = []
            # extract the data
            data, error, lat = extract_data_along_line(file_path, lon)
            # plot the data
            plot_data(data, error, lat)
        else:
            print(f"{how} is not a valid method")
            print("Exiting program")
            exit()
    else:
        # if they are not valid, then print an error message
        print(error)
        # exit the program if there is an error
        print("Exiting program")
        exit()

# define a function which calls the extract data function
# along a line of longitude (i.e. in the centre of the Atlantic Ocean)
# and extracts the SST data and error at each point into an array
def extract_data_along_line(filename, lon):
    """Extracts SST data and error along a line of longitude.

    Parameters
    ----------
    filename : str
        Fully qualified pathname of a valid NetCDF file.
    lon : float
        Longitude coordinate to extract data at.

    Returns
    -------
    data : numpy.ndarray
        SST data at the given coordinates.
    error : numpy.ndarray
        SST error at the given coordinates.
    lat : numpy.ndarray
        Latitude coordinates.
    """
    # load the file using xarray
    loaded = load_file(filename, "xarray")

    # extract the SST data, error, and lat at the given coordinates
    data = loaded.sel(lon=lon, method="nearest")["analysed_sst"].data
    error = loaded.sel(lon=lon, method="nearest")["analysis_error"].data
    lat = loaded.sel(lon=lon, method="nearest")["lat"].data

    # create a mask for non-NaN entries in data and error
    mask = ~np.isnan(data) & ~np.isnan(error)

    # extract only the True + false values from the mask
    mask_lat = mask[0,:]

    # apply the mask to data, error, and lat
    data = data[mask]
    error = error[mask]
    # specify [0,:] to get the first row of the array
    lat = lat[mask_lat]

    return data, error, lat


# define a plotting function which takes the extracted data and error
# and plots them on a graph
# with latitude on the x-axis and SST on the y-axis
# with error bars
def plot_data(data, error, lat):
    """Plots SST data and error on a graph.

    Parameters
    ----------
    data : numpy.ndarray
        SST data at the given coordinates.
    error : numpy.ndarray
        SST error at the given coordinates.
    lat : numpy.ndarray
        Latitude coordinates.

    Returns
    -------
    None
    """
    # print the data and shapes for debugging
    print(data[381:])
    print(error[381:])
    print(lat[381:])
    # check whether any nan values have been introduced
    print(np.isnan(data).any())
    print(np.isnan(error).any())
    # check the shapes of the data
    print(data.shape)
    print(error.shape)
    print(lat.shape)

    # plot the data
    # with latitude on the x-axis and SST on the y-axis
    # with error bars
    # skip over any NaN values
    plt.errorbar(lat, data, yerr=error, fmt="none", ecolor="r", label="Error", alpha=0.3)
    plt.plot(lat, data, "b-", label="SST")
    # add axis labels
    plt.xlabel("Latitude")
    plt.ylabel("SST (K)")
    # add a title
    plt.title("SST along a line of longitude")
    # show the plot
    plt.show()


# call main program
if __name__ == '__main__': 
    
    # define the file path
    polcoms_file = "/workspaces/software-dev-may/data/polcoms.nc"
    GHR_file = "/workspaces/software-dev-may/data/20100601120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_LT-v02.0-fv01.0.nc"

    # define the coordinates
    lat = 50.000245
    lon = -10.0356456

    # define invalid file path
    invalid_file = "invalid_file.bash"

    # define invalid coordinates
    invalid_lat = 100.0
    invalid_lon = 200.0

    #main_program(invalid_file, lat, lon)

    main_program(GHR_file, lat, lon, how="line")
