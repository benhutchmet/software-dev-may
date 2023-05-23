import /workspaces/software-dev-may/netCDF_ex.py as netCDF_ex
import nose.tools as nt


# # define the setup_module function
# def setup_module():
#     """Set up the module for testing."""
#     # define the file path
#     #polcoms_file = "/workspaces/software-dev-may/data/polcoms.nc"



def test_is_valid_normal_lat():
    """Test whether is_valid_normal_lat returns True for valid input."""
    # define the input
    lat = 20.0
    # call the function
    result = netCDF_ex.is_valid(lat=lat)
    # check the result
    nt.assert_true(result)

# define a test for an invalid latitude
def test_is_valid_invalid_lat():
    """Test whether is_valid_normal_lat returns False for invalid input."""
    # define the input
    lat = 100.0
    # call the function
    result = netCDF_ex.is_valid(lat=lat)
    # check the result
    nt.assert_false(result)

# # define the teardown_module function
# def teardown_module():
#     """Tear down the module after testing."""
#     # nothing to do here
#     pass
