"""Extract and visualize monthly average global temperatures using 
https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/all/1/1880-2023 
and https://www.ncei.noaa.gov/access/monitoring/global-temperature-anomalies#mean

Assignment 5 bonus task 5.7
"""

from typing import Optional
from functools import lru_cache

import pandas as pd
import altair as alt
import requests
from bs4 import BeautifulSoup


def get_html(url: str, params: Optional[dict] = None, output: Optional[str] = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """

    # passing the optional parameters argument to the get function
    response = requests.get(url, params=params)

    # Assert successful request response status code
    assert (
        response.status_code == 200
    ), f"Request was not as anticipated (200), ot {response.status_code}."

    # Get html from response
    html_str = response.text

    if output:
        # if output is specified, the response url and text content are written to the file `output`
        with open(output, "w") as outfile:
            outfile.write(url)
            outfile.write(html_str)

    return html_str


@lru_cache
def scrape_mean_temperatures(
    url: str = "https://www.ncei.noaa.gov/monitoring-content/monitoring-references/faq/anomalies/text/mean.html",
    unit: str = "C",
) -> pd.DataFrame:
    """Scrapes monthly global mean temperature data from the table on
    'https://www.ncei.noaa.gov/access/monitoring/global-temperature-anomalies#mean'
    into a DataFrame.

    Args:
        url: The url to scrape the data from. Defaults to "https://www.ncei.noaa.gov/monitoring-content/monitoring-references/faq/anomalies/text/mean.html"
        unit: The temperature unit, either Celsuis as 'C' or Fahrenheit as 'F'

    Returns:
        DataFrame containing global mean temperature for land & sea for each month,
        columns=('Month', 'Temperature')
    """

    unit = unit.upper()
    assert unit in ["C", "F"], f"Unexpected unit: '{unit}', expected 'C' or 'F'"

    # Get and parse html
    # NOTE: The table is loaded with JavaScript on the site
    # 'https://www.ncei.noaa.gov/access/monitoring/global-temperature-anomalies#mean'
    # which means we instead retrieved the source html file
    # 'https://www.ncei.noaa.gov/monitoring-content/monitoring-references/faq/anomalies/text/mean.html
    html = get_html(url)

    # Find the table of values
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="estimated-means").find("tbody")  # find table body

    months = list(range(1, 13))
    temps = list()

    # Iterate through the table rows
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all(["th", "td"])
        if not cols:
            continue

        # Separate column text, use land & sea temperature
        _, _, _, land_sea = [col.get_text(strip=True) for col in cols]

        # Get the data of the correct unit
        if unit == "C":
            land_sea = land_sea.split("°")[0]
        elif unit == "F":
            land_sea = land_sea.split("°")[1].lstrip("C")

        temps.append(land_sea)

    # Create the dataframe, skip the last temperature which is from the annual data
    df = pd.DataFrame({"Month": months, f"Temperature": temps[:-1]})
    df["Temperature"] = df["Temperature"].astype(float)

    return df


@lru_cache
def extract_anomaly_data(filename: str = "data.csv") -> pd.DataFrame:
    """Extracts global temperature anomalies from a csv file into a DataFrame,
    data downloaded from 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/all/1/1880-2023'
    so the csv format should be the same: the fourth row should have the column names
    "Year,Anomaly" then the rest of the rows are the data in that order. The "Year"
    column also contains the month index as the last two numbers, e.g. "202313".

    Args:
        filename: csv filename to extract data from. Defaults to "data.csv".

    Returns:
        DataFrame containing the data with the columns ["Year", "Anomaly", "Month"]
    """

    # pandas will raise the FileNotFoundError with good error message for us

    # Get the data from the csv
    df = pd.read_csv(filename, skiprows=4)

    # Split the year and month from the 'Year' column (202313 -> [2023, 13])
    years = df["Year"].astype(str).str[:4].astype(int)
    months = df["Year"].astype(str).str[4:].astype(int)

    df["Year"] = years
    df["Month"] = months

    return df


def get_monthly_mean_temperatures(
    df1: Optional[pd.DataFrame] = None,
    df2: Optional[pd.DataFrame] = None,
    unit: str = "C",
) -> pd.DataFrame:
    """Calculate global monthly mean temperatures for several years all loaded from
    https://www.ncei.noaa.gov.

    Args:
        df1: DataFrame from extract_anomaly_data()
        df2: DataFrame from scrape_mean_temperatures()
        unit: Temperature unit, either "C" or "F". Defaults to "C".

    Returns:
        Combined DataFrame containing mean temperatures with columns
        ("Year", "Temperature", "Month", "Highest year", "Highest temperature",
        "Lowest temperature", "Lowest year")
    """

    if df1 is None:
        df1 = extract_anomaly_data()

    if df2 is None:
        df2 = scrape_mean_temperatures(unit=unit)

    # Merge df1 and df2 on "Year" and "Month"
    df = df1.merge(df2, on=["Month"])

    # Add "Temperature" values to "Anomaly" values to get total mean temperatures
    df["Temperature"] = df["Anomaly"] + df["Temperature"]
    df.drop(columns=["Anomaly"], inplace=True)  # Delete the anomaly column

    # Find highest temperatures
    highest_temps = df.groupby("Month")["Temperature"].transform("max")
    highest_years = (
        df[df["Temperature"].isin(highest_temps)].groupby("Month")["Year"].first()
    )

    # Add highest temperatures and years to the DataFrame
    df["Highest temperature"] = highest_temps
    df["Highest year"] = df["Month"].map(highest_years)

    # Find lowest temperatures
    lowest_temps = df.groupby("Month")["Temperature"].transform("min")
    lowest_years = (
        df[df["Temperature"].isin(lowest_temps)].groupby("Month")["Year"].first()
    )

    # Add lowest temperatures and years to the DataFrame
    df["Lowest temperature"] = lowest_temps
    df["Lowest year"] = df["Month"].map(lowest_years)

    return df.sort_values(by="Year").reset_index(drop=True)


def plot_mean_temperatures(df: Optional[pd.DataFrame] = None) -> alt.Chart:
    """Plots the global mean temperatures for each month for each year. The x-axis is
    the month, the y-axis is temperature, and each year gets its own line-graph.

    Args:
        df: DataFrame containing the mean temperature for each month and year, from
            get_monthly_mean_temperatures(). Defaults to calling get_monthly_mean_temperatures()

    Returns:
        altair Chart containing the plotted mean temperatures.
    """

    if df is None:
        df = get_monthly_mean_temperatures()

    # Set opacity and color based on year, if the year is the current one then its red and full opacity
    length = len(df["Year"].unique()) - 1
    opacity_scale = alt.Scale(
        domain=df["Year"].unique(),
        range=[0.1] * length + [1],
    )
    color_scale = alt.Scale(
        domain=df["Year"].unique(),
        range=["blue"] * length + ["red"],
    )

    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="Month",
            y="Temperature",
            color=alt.Color("Year:Q", scale=color_scale, legend=None),
            opacity=alt.Opacity("Year:Q", scale=opacity_scale),
            tooltip=[
                "Month",
                "Temperature",
                "Year",
                "Highest temperature",
                "Highest year",
                "Lowest temperature",
                "Lowest year",
            ],
        )
        .interactive()
    )


def main() -> None:
    """Allow running this module as a script for testing; plots the global mean
    temperatures for each month and year and shows it (requires
    altair viewer or vscode/jupyter notebook)

    Args:
        None

    Returns:
        None"""

    plot_mean_temperatures().show()


if __name__ == "__main__":
    main()
