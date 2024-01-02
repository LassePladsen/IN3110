""" Test script executing all the necessary unit tests for the functions in analytic_tools/utilities.py module
    which is a part of the analytic_tools package
"""

# Include the necessary packages here
from pathlib import Path

import pytest
# This should work if analytic_tools has been installed properly in your environment
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
)


@pytest.mark.task12
def test_get_diagnostics(example_config):
    """Test functionality of get_diagnostics in utilities module

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
                                     from Figure 1 in assignment2.md

    Returns:
    None
    """
    expected = {
        "subdirectories": 4,
        ".npy files": 2,
        ".txt files": 0,
        ".csv files": 8,
        ".md files": 0,
        "other files": 0,
        "files": 10
    }
    assert (get_diagnostics(example_config / "pollution_data") == expected)


@pytest.mark.task12
@pytest.mark.parametrize(
        "exception, dir",
        [
            (NotADirectoryError, "Not_a_real_directory"),
            # This is really trigger the .exists() error instead of .is_dir()
            (NotADirectoryError, "Not_anything"),  # This is therefore redundant
            (TypeError, 1),
            (TypeError, 1.0),
            (TypeError, [5]),
            (TypeError, {2: 5}),
            (TypeError, True),
            (TypeError, False)
        ]
)
def test_get_diagnostics_exceptions(exception, dir):
    """Test the error handling of get_diagnostics function

    Parameters:
        exception (concrete exception): The exception to raise
        dir (str or pathlib.Path): The parameter to pass as 'dir' to the function

    Returns:
        None
    """
    with pytest.raises(exception):
        get_diagnostics(dir)


@pytest.mark.task22
def test_is_gas_csv():
    """Test functionality of is_gas_csv from utilities module

    Parameters:
        None

    Returns:
        None
    """

    assert not is_gas_csv("not_existing_csv.csv")
    assert not is_gas_csv("not_existing_other.csv")
    assert not is_gas_csv("<co>2.csv")
    assert not is_gas_csv("!@$N2o.csv")
    assert not is_gas_csv(Path(__file__).parent.absolute() / "pollution_data/by_src/src_industry/CH4_EsA.csv")
    assert not is_gas_csv(Path(__file__).parent.absolute() / "pollution_data/by_src/src_industry/co2_ydx.csv")
    assert is_gas_csv(Path(__file__).parent.absolute() / "pollution_data/by_src/src_airtraffic/CH4.csv")
    assert is_gas_csv(Path(__file__).parent.absolute() / "pollution_data/by_src/src_agriculture/co2.csv")
    assert is_gas_csv("n2o.csv")
    assert is_gas_csv("sF6.csv")


@pytest.mark.task22
@pytest.mark.parametrize(
        "exception, path",
        [
            (ValueError, Path(__file__).parent.absolute()),
            (ValueError,
             (Path(__file__).parent.absolute() / "..").resolve() / "pollution_data/by_src/src_industry/co2.txt"),
            (ValueError, "non_existing_file.txt"),
            (ValueError, "non_existing_file.mov"),
            (TypeError, 5),
            (TypeError, 0.10),
            (TypeError, 5),
            (TypeError, {2: 5}),
            (TypeError, False),
            (TypeError, True)
        ]
)
def test_is_gas_csv_exceptions(exception, path):
    """Test the error handling of is_gas_csv function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'path' to function

    Returns:
        None
    """
    with pytest.raises(exception):
        is_gas_csv(path)


@pytest.mark.task24
def test_get_dest_dir_from_csv_file(example_config):
    """Test functionality of get_dest_dir_from_csv_file in utilities module.

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
            from Figure 1 in assignment2.md

    Returns:
        None
    """

    input_files = [
        example_config / "pollution_data/by_src/src_agriculture/H2.csv",
        example_config / "pollution_data/by_src/src_airtraffic/CO2.csv",
        example_config / "pollution_data/by_src/src_oil_and_gas/CH4.csv",
        example_config / "pollution_data/by_src/src_oil_and_gas/h2O.csv",
        example_config / "pollution_data/by_src/src_oil_and_gas/cO2.csv"
    ]

    expected = [
        example_config / "pollution_data_restructured/by_gas/gas_H2",
        example_config / "pollution_data_restructured/by_gas/gas_CO2",
        example_config / "pollution_data_restructured/by_gas/gas_CH4",
        example_config / "pollution_data_restructured/by_gas/gas_H20",
        example_config / "pollution_data_restructured/by_gas/gas_CO2",
    ]

    for input_i, expected_i in zip(input_files, expected):
        output_i = get_dest_dir_from_csv_file(".", input_i)
        assert output_i == expected_i  # Check output string is correct
        assert output_i.exists()  # Then check directory exists and is a dir
        assert output_i.is_dir()


@pytest.mark.task24
@pytest.mark.parametrize(
        "exception, dest_parent, file_path",
        [
            (TypeError, Path(__file__).parent.absolute(), 5),
            (TypeError, Path(__file__).parent.absolute(), 5.0),
            (TypeError, Path(__file__).parent.absolute(), []),
            (TypeError, Path(__file__).parent.absolute(), {}),
            (TypeError, Path(__file__).parent.absolute(), True),
            (TypeError, Path(__file__).parent.absolute(), False),
            (ValueError, Path(__file__).parent.absolute(), "foo"),
            (ValueError, Path(__file__).parent.absolute(), "foo.txt"),
            (ValueError, Path(__file__).parent.absolute(), "foo.csv"),
            (NotADirectoryError, (Path(__file__).parent / "..").resolve() / "non_existing_directory",
             (Path(__file__).parent / "..").resolve() / "pollution_data/by_src/src_industry/CH4.csv"),
            (
            NotADirectoryError, (Path(__file__).parent / "..").resolve() / "pollution_data/by_src/src_industry/CH4.csv",
            (Path(__file__).parent / "..").resolve() / "pollution_data/by_src/src_industry/CO2.csv")
        ]
)
def test_get_dest_dir_from_csv_file_exceptions(exception, dest_parent, file_path):
    """Test the error handling of get_dest_dir_from_csv_file function

    Parameters:
        exception (concrete exception): The exception to raise
        dest_parent (str or pathlib.Path): The parameter to pass as 'dest_parent' to the function
        file_path (str or pathlib.Path): The parameter to pass as 'file_path' to the function

    Returns:
        None
    """

    with pytest.raises(exception):
        get_dest_dir_from_csv_file(dest_parent, file_path)


@pytest.mark.task26
def test_merge_parent_and_basename():
    """Test functionality of merge_parent_and_basename from utilities module

    Parameters:
        None

    Returns:
        None
    """

    assert merge_parent_and_basename('/User/.../assignment2/pollution_data/by_src/src_agriculture/CO2.csv') \
           == 'src_agriculture_CO2.csv'
    assert merge_parent_and_basename('some_dir/some_sub_dir') == 'some_dir_some_sub_dir'
    assert merge_parent_and_basename('some_dir/some_file.txt/') == 'some_dir_some_file.txt'
    assert merge_parent_and_basename("dir/sub_dir@/test_file.txt/impossible_path") == "test_file.txt_impossible_path"
    assert merge_parent_and_basename(r"pollution_data\by_src\src_agriculture\CH4.csv") == "src_agriculture_CH4.csv"
    assert merge_parent_and_basename(r"by_src\src_industry\h2o.csv") == "src_industry_h2o.csv"


@pytest.mark.task26
@pytest.mark.parametrize(
        "exception, path",
        [
            (TypeError, 33),
            (TypeError, 0.1),
            (TypeError, []),
            (TypeError, {}),
            (TypeError, True),
            (TypeError, False),
            (ValueError, "directory"),
            (ValueError, "file.txt"),
            (ValueError, "/directory/"),
            (ValueError, "\\directory\\"),
        ]
)
def test_merge_parent_and_basename_exceptions(exception, path):
    """Test the error handling of merge_parent_and_basename function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'pass' to the function

    Returns:
        None
    """
    with pytest.raises(exception):
        merge_parent_and_basename(path)
