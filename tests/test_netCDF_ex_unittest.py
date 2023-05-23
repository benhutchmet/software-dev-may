import unittest
from src.netCDF_ex import is_valid
from src.netCDF_ex import extract_data

class ValidityTests(unittest.TestCase):
    """Tests for the is_valid function."""

    def test_valid_input(self):
        """Test whether valid input returns True and no error message."""
        # define the input
        filename = "/workspaces/software-dev-may/data/polcoms.nc"
        lat = 45.0
        lon = -120.0
        # call the function
        result, error_msg = is_valid(filename=filename, lat=lat, lon=lon)
        # check the result
        self.assertTrue(result)
        self.assertIsNone(error_msg)

    def test_invalid_file_path(self):
        """Test whether an invalid file path returns False and an error message."""
        # define the input
        filename = "/path/to/invalid/file.nc"
        lat = 45.0
        lon = -120.0
        # call the function
        result, error_msg = is_valid(filename=filename, lat=lat, lon=lon)
        # check the result
        self.assertFalse(result)
        self.assertEqual(error_msg, f"{filename} is not a valid file path")

    def test_invalid_latitude(self):
        """Test whether an invalid latitude returns False and an error message."""
        # define the input
        filename = "/path/to/valid/file.nc"
        lat = 100.0
        lon = -120.0
        # call the function
        result, error_msg = is_valid(filename=filename, lat=lat, lon=lon)
        # check the result
        self.assertFalse(result)
        self.assertEqual(error_msg, f"{lat} is not a valid latitude")

    def test_invalid_longitude(self):
        """Test whether an invalid longitude returns False and an error message."""
        # define the input
        filename = "/path/to/valid/file.nc"
        lat = 45.0
        lon = 200.0
        # call the function
        result, error_msg = is_valid(filename=filename, lat=lat, lon=lon)
        # check the result
        self.assertFalse(result)
        self.assertEqual(error_msg, f"{lon} is not a valid longitude")

# define a new class for testing the extract_data function
class ExtractDataTests(unittest.TestCase):
    """Tests for the extract_data function."""

    # define a test for valid input
    def test_valid_input(self):
        """Test whether valid input returns the correct data."""
        # define the input
        filename = "/workspaces/software-dev-may/data/20100601120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_LT-v02.0-fv01.0.nc"
        lat = 45.0
        lon = -120.0
        # call the function
        data = extract_data(filename=filename, lat=lat, lon=lon)
        # check the result
        self.assertEqual(data, 10.0)

    # define a test for invalid input
    def test_invalid_filepath(self):
        """Test whether an invalid file path returns None."""
        # define the input
        filename = "/path/to/invalid/file.nc"
        lat = 45.0
        lon = -120.0
        # call the function
        data = extract_data(filename=filename, lat=lat, lon=lon)
        # check the result
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
