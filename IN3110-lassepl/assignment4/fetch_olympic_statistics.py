"""
Task 4

collecting olympic statistics from wikipedia
"""

from __future__ import annotations

import re
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from bs4 import BeautifulSoup

from requesting_urls import get_html

# Countries to submit statistics for
scandinavian_countries = ["Norway", "Sweden", "Denmark"]

# Summer sports to submit statistics for
summer_sports = ["Sailing", "Athletics", "Handball", "Football", "Cycling", "Archery"]


def report_scandi_stats(url: str, sports_list: list[str], work_dir: str | Path) -> None:
    """
    Given the url, extract and display following statistics for the Scandinavian countries:

      -  Total number of gold medals for for summer and winter Olympics
      -  Total number of gold, silver and bronze medals in the selected summer sports from sport_list
      -  The best country in number of gold medals in each of the selected summer sports from sport_list

    Display the first two as bar charts, and the last as an md. table and save in a separate directory.

    Parameters:
        url (str) : url to the 'All-time Olympic Games medal table' wiki page
        sports_list (list[str]) : list of summer Olympic games sports to display statistics for
        work_dir (str | Path) : (absolute) path to your current working directory

    Returns:
        None
    """

    # Make a call to get_scandi_stats
    # Plot the summer/winter gold medal stats
    # Iterate through each sport and make a call to get_sport_stats
    # Plot the sport specific stats
    # Make a call to find_best_country_in_sport for each sport
    # Create and save the md table of best in each sport stats

    work_dir = Path(work_dir)
    stats_dir = work_dir / "olympic_games_results"

    # Create dirs if they don'tt exist
    if not work_dir.exists():
        work_dir.mkdir()
    if not stats_dir.exists():
        stats_dir.mkdir()

    # Get url and total summer/winter gold medals
    country_dict = get_scandi_stats(url)

    # Create summer/winter gold medals bar plot
    country_golds_dict = {}
    for country, info_dict in country_dict.items():
        country_golds_dict[country] = info_dict["medals"]  # reformat dict as {'Country': {'Summer': x, 'Winter': y}}
    plot_scandi_stats(country_golds_dict, stats_dir / "total_medal_ranking.png")


    # Init dataframe for best countries for each sport
    df = pd.DataFrame(["None"]*len(sports_list), sports_list, columns=["Best country"])
    df.index.name = "Sport"

    # Iterate through all chosen sports and create bar plots and .md table
    for sport in sports_list:
        results: dict[str, dict[str, int]] = {}

        # Iterate through each country and create medals bar plots
        for country, info_dict, in country_dict.items():

            # Store sport's medal stats of country
            results[country] = get_sport_stats(info_dict["url"], sport)

            # Replace any None dicts with dicts of zeros.
            if not results[country]:
                results[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}

        # Bar plot
        plot_scandi_stats(results, stats_dir / f"{sport}_medal_ranking.png")


        # Find best country for the sport of gold medals and store it in the dataframe
        df.loc[sport] = find_best_country_in_sport(results, "Gold")

    # Save dataframe of best countries for gold medals as markdown table
    path = stats_dir / "best_of_sport_by_Gold.md"
    with open(path, "w", encoding="utf-8") as f:
        print(f"Saving markdown table of best countries by gold medals to '{path}'...")
        f.write(df.to_markdown())


def get_scandi_stats(
        url: str,
) -> dict[str, dict[str, str | dict[str, int]]]:
    """Given the url, extract the urls for the Scandinavian countries,
       as well as number of gold medals acquired in summer and winter Olympic games
       from 'List of NOCs with medals' table.

    Parameters:
      url (str): url to the 'All-time Olympic Games medal table' wiki page

    Returns:
      country_dict: dictionary of the form:
        {
            "country": {
                "url": "https://...",
                "medals": {
                    "Summer": 0,
                    "Winter": 0,
                },
            },
        }

        with the tree keys "Norway", "Denmark", "Sweden".
    """
    # Get html
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    # find the first table, which is the "List of NOCs with medals (sortable & unranked)" table
    table = soup.find("table", class_="wikitable")

    # Assert that we have the right table just to be sure
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    assert "Team" in headers, "Table header 'Team' missing in table headers"
    assert "Summer Olympic Games" in headers, "Table header 'Summer Olympic Games' missing in table headers"
    assert "Winter Olympic Games" in headers, "Table header 'Winter Olympic Games' missing in table headers"
    assert "Combined total" in headers, "Table header 'Combined total' missing in table headers"

    country_dict: dict[str, dict[str, str | dict[str, int]]] = {}
    base_url = "https://en.wikipedia.org"

    # Iterate through the table rows
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all(["th", "td"])
        if not cols:
            continue

        # Separate column text
        cols_text = [col.get_text(strip=True) for col in cols]

        # Get <a> tag with url
        a_tag = cols[0].find("a", href=True)
        if a_tag:

            # Extract country name from the <a> tag
            country = a_tag.get_text()

            # Check for scandinavian country row
            if country in scandinavian_countries:
                # Then extract data from this scandinavian country's row:

                # Find wiki url from the first column's link
                url = a_tag["href"]

                # Find the gold medals
                gold_summer, gold_winter = int(cols_text[2]), int(cols_text[7])

                country_dict[country] = {
                    "url": base_url + url,
                    "medals": {
                        "Summer": gold_summer,
                        "Winter": gold_winter
                    }
                }

    return country_dict


def get_sport_stats(country_url: str, sport: str) -> dict[str, int]:
    """Given the url to country specific performance page, get the number of gold, silver, and bronze medals
      the given country has acquired in the requested sport in summer Olympic games.

    Parameters:
        - country_url (str) : url to the country specific Olympic performance wiki page
        - sport (str) : name of the summer Olympic sport in interest. Should be used to filter rows in the table.

    Returns:
        - medals (dict[str, int]) : dictionary of number of medal acquired in the given sport by the country
                          Format:
                          {"Gold" : x, "Silver" : y, "Bronze" : z}
    """

    # Parse html
    html = get_html(country_url)
    soup = BeautifulSoup(html, "html.parser")

    # Init dict
    medals = {
        "Gold": 0,
        "Silver": 0,
        "Bronze": 0,
    }

    for season in ["summer", "winter"]:
        # Find first tag with class 'mw-headline' (the table headers) that matches the summer/winter table
        table_hd = soup.find(class_="mw-headline", string=re.compile(f"Medals by {season} sport", re.IGNORECASE))
        if not table_hd:
            continue

        # Then find the table right below
        table = table_hd.find_next("table")

        # Iterate through its rows
        rows = table.find_all("tr")
        for row in rows:
            # Get columns
            cols = row.find_all(["th", "td"])
            if not cols:
                continue

            # Separate column text
            cols_text = [col.get_text(strip=True) for col in cols]

            # Skip first and last row
            if "Sport" in cols_text[0] or "Totals" in cols_text[0]:
                continue

            # Get entries
            sport_row, gold, silver, bronze, _ = cols_text

            # If right sport: return its values in the dict
            if sport.lower() == sport_row.lower():
                medals["Gold"] = int(gold)
                medals["Silver"] = int(silver)
                medals["Bronze"] = int(bronze)
                return medals


def find_best_country_in_sport(
        results: dict[str, dict[str, int]], medal: str = "Gold"
) -> str:
    """Given a dictionary with medal stats in a given sport for the Scandinavian countries, return the country
        that has received the most of the given `medal`.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - medal (str) : medal type to compare for. Valid parameters: ["Gold" | "Silver" |"Bronze"]. Should be used as a key
                          to the medal dictionary.
    Returns:
        - best (str) : name of the country(ies) leading in number of gold medals in the given sport
                       If one country leads only, return its name, like for instance 'Norway'
                       If two countries lead return their names separated with '/' like 'Norway/Sweden'
                       If all or none of the countries lead, return string 'None'
    """
    valid_medals = {"Gold", "Silver", "Bronze"}
    if medal not in valid_medals:
        raise ValueError(
                f"{medal} is invalid parameter for ranking, must be in {valid_medals}"
        )

    # Get the requested medals and determine the best:

    # Iterate through all countries and medal counts
    best = 0
    best_country = ""
    for country, counts in results.items():
        medal_count = counts[medal]

        # Check if is better or equal than current best
        if medal_count > best:  # This one is better
            # Save as new best
            best = medal_count
            best_country = country

        elif medal_count == best:  # tied
            best_country += "/" + country

        # Check if all three are tied -> return "None" winner
        if best_country.count("/") >= len(results.keys()) - 1:
            best_country = "None"

    # Do a last check for if there is any anomalies like 'None/Sweden' and replace with None,
    # this happens when none has any of the given medal
    if "None" in best_country and "/" in best_country:
        best_country = "None"

    return best_country


# Define your own plotting functions and optional helper functions


def plot_scandi_stats(
        results: dict[str, dict[str, int]],
        output_path: str | Path,
) -> None:
    """Plot the number of medals in for each of the scandi countries as bars. Can plot two types of dictionary stats:
    either a summer vs winter gold medal count plot or a gold vs silver vs bronze medal count for a summer sport plot.

    Parameters:
      results (dict[str, dict[str, int]]) : a nested dictionary of country names and the corresponding medal stats.
                            Format:
                                EITHER {"country_name": {"Summer" : x, "Winter" : y}}
                                OR {"country_name": {"Gold" : x, "Silver" : y, "Bronze": z}}
      output_path (str | Path) : output file path for the saved figure
    Returns:
      None
    """

    # Initialize plotting figure and axes
    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(9, 5))

    # First check what type of stats
    if "Summer" in list(results.values())[0]:  # stats are summer/winter gold medals count

        # Iterate through the countries' stats
        i = 0
        bar_width = 0.3
        for country, stats_dict in results.items():

            # Get medal counts
            summer_medals = stats_dict["Summer"]
            winter_medals = stats_dict["Winter"]

            # Plot the bar plots
            bar1 = ax.bar(i - bar_width / 2, summer_medals, bar_width, color="#d62738")
            bar2 = ax.bar(i + bar_width / 2, winter_medals, bar_width, color="#1f77b4")

            # Show the bar values
            ax.bar_label(bar1)
            ax.bar_label(bar2)
            i += 1

        # Fix axis ticks
        ax.set_xticks(range(len(results.keys())), results.keys())

        # Increase ymax a bit
        top = ax.get_ylim()[1]
        ax.set_ylim(top=top * 1.5)

        # Save figure
        ax.set_title("Number of gold medals for scandinavian countries in Olympic Games")
        ax.set_xlabel("Countries")
        ax.set_ylabel("Number of gold medals")
        plt.legend(["Summer", "Winter"])
        print(f"Saving scandinavian Olympic Games gold medals bar plot to '{output_path}'...")
        plt.savefig(output_path)

    elif "Gold" in list(results.values())[0]:  # stats are gold/silver/bronze medals counts

        # Iterate through the countries' stats
        i = 0
        bar_width = 0.2
        for country, stats_dict in results.items():

            # Get medal counts
            golds = stats_dict["Gold"]
            silvers = stats_dict["Silver"]
            bronzes = stats_dict["Bronze"]

            # Plot the bar plots
            bar1 = ax.bar(i - bar_width, golds, bar_width, color="gold")
            bar2 = ax.bar(i, silvers, bar_width, color="silver")
            bar3 = ax.bar(i + bar_width, bronzes, bar_width, color="orange")

            # Show the bar values
            ax.bar_label(bar1)
            ax.bar_label(bar2)
            ax.bar_label(bar3)
            i += 1

        # Fix axis ticks
        ax.set_xticks(range(len(results.keys())), results.keys())

        # Increase ymax a bit
        top = ax.get_ylim()[1]
        ax.set_ylim(top=top * 1.5)

        # Save figure
        sport = str(output_path.stem).split("_")[0]
        ax.set_title(f"Number of medals in {sport} for scandinavian countries in Olympic Games")
        ax.set_xlabel("Countries")
        ax.set_ylabel(f"Number of medals in {sport}")
        plt.legend(["Gold", "Silver", "Bronze"])
        print(f"Saving scandinavian Olympic Games medals in {sport} bar plot to '{output_path}'...")
        plt.savefig(output_path)


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
    work_dir = "."
    report_scandi_stats(url, summer_sports, work_dir)
