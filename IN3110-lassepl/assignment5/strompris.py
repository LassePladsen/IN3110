#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime
from typing import Optional
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", message=".*convert_dtype.*")
warnings.filterwarnings("ignore", category=FutureWarning)


# task 5.1:


def fetch_day_prices(
    date: Optional[datetime.date] = None, location: str = "NO1"
) -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Args:
        date: The date to fetch the prices for, must be after October 1st 2023.
            Defaults to the day the function is called.
        location: The location code. Defaults to NO1 (Oslo).

    Returns:
        DataFrame containing the day prices for the given location with the columns
        'time_start', 'NOK_per_kWh', and 'EUR_per_kWh'
    """

    # Set default date to today
    if date is None:
        date = datetime.date.today()

    else:
        # Assert date is after October 1st 2023
        assert date >= datetime.date(
            2023, 10, 1
        ), f"Date should be after October 1st, 2023, got {date}"

    # Format month and day with leading zero
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)

    # Get data
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{month}-{day}_{location}.json"
    r = requests.get(url)

    # Check status ok
    assert 200 <= r.status_code < 300, f"Status code is not ok: {r.status_code}"

    # Convert json data to dataframe
    df = pd.DataFrame(r.json())

    # Drop columns
    df = df.drop("EXR", axis=1).drop("time_end", axis=1)

    # Convert time starts to datetime objects
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )

    # Reorder columns to time then price
    df = df.loc[:, ::-1]

    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
}

# task 1:


def fetch_prices(
    end_date: Optional[datetime.date] = None,
    days: int = 7,
    locations: list[str] = list(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Args:
        end_date: End date to fetch prices up to, starting from (end_date - days)
            and ending at end_date. Defaults to the date the function is called.
        days: Number of days to fetch prices for up to the end_date. Defaults to 7.
        locations: List of location codes to fetch prices for.
            Defaults to every region (from 'NO1' to 'NO6' inclusive).

    Returns:
        DataFrame containing all prices for each day and location sorted by time with
        the columns: 'time_start', 'location_code', 'location', 'NOK_per_kWh', 'EUR_per_kWh'
    """

    if end_date is None:
        end_date = datetime.date.today()

    # Create a list containing last 'days' date objects
    dates = [end_date - datetime.timedelta(days=day) for day in range(days - 1, -1, -1)]

    # Initialize dataframe for the later concatenation
    cols = ["time_start", "location_code", "location", "NOK_per_kWh", "EUR_per_kWh"]
    df = pd.DataFrame(columns=cols)

    # Concatenate dataframes
    for date in dates:
        for location in locations:
            assert (
                location in LOCATION_CODES
            ), f"Location '{location}' not found in '{list(LOCATION_CODES.keys())}'"
            # Concatenate location dataframes from fetch_day_prices() for current date
            dfi = fetch_day_prices(date=date, location=location)
            dfi["location_code"] = location
            dfi["location"] = LOCATION_CODES[location]

            df = pd.concat([df, dfi])

    # Sort by time_start
    df.sort_values(by="time_start", inplace=True)

    # Reset index numbering
    df.reset_index(drop=True, inplace=True)

    return df


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time. x-axis is time_start, y-axis is NOK_per_kWh, and
    each location has its own line graph in the figure

    Args:
        df: The DataFrame to plot with the format from fetch_prices(), which have the
            columns: 'time_start', 'location_code', 'location', 'NOK_per_kWh', 'EUR_per_kWh'
            (although the 'location_code' column is unneeded)

    Returns:
        altair.Chart containing the plotted prices
    """

    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="time_start",
            y="NOK_per_kWh",
            color="location",
            tooltip=["time_start", "NOK_per_kWh", "EUR_per_kWh", "location"],
        )
        .interactive()
    )


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError


# Task 5.6
# Maps activity names to energy usage in kW
ACTIVITIES = {
    "shower": 30,
    "baking": 2.5,
    "heat": 1,
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10.0
) -> alt.Chart:
    """
    Plot price for one activity by name, given a DataFrame of prices and its
    duration in minutes

    Args:
        df: DataFrame containing electricity prices in the format from the function
            fetch_prices(), which have the columns: 'time_start', 'location_code',
            'location', 'NOK_per_kWh', 'EUR_per_kWh' (although the 'location_code'
            column is unneeded)
        activity: Which activity to plot prices for,
            in ['shower', 'baking' 'heat']. Defaults to 'shower'.
        minutes: Number of minute to plot the activity price for. Defaults to 10.

    Returns:
        altair.Chart containing the plotted prices for the activity and number of minutes
    """

    assert (
        activity in ACTIVITIES
    ), f"Activity '{activity}' not found in {list(ACTIVITIES.keys())}"

    assert (
        minutes <= 60
    ), f"Activity price time must be an hour or less, got: '{minutes}'"

    # Calculate prices for the number of minutes
    price = ACTIVITIES[activity]
    df["activity"] = activity
    df["minutes"] = minutes

    # NOK/kWh * kW * h = NOK
    df["total_NOK"] = df["NOK_per_kWh"] * price * minutes / 60

    return (
        alt.Chart(df)
        .mark_line()
        .encode(x="time_start", y="total_NOK", tooltip=["time_start", "total_NOK"])
        .interactive()
    )


def main() -> None:
    """Allow running this module as a script for testing; creates the price chart plot
    for the last 7 days from the day this function is ran and shows it (requires
    altair viewer or vscode/jupyter notebook)

    Args:
        None

    Returns:
        None
    """
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
