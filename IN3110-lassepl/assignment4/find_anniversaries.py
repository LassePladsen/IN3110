"""
Task 3

Collecting anniversaries from Wikipedia
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from requesting_urls import get_html

# Month names to submit for, from Wikipedia:Selected anniversaries namespace
months_in_namespace = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def extract_anniversaries(html: str, month: str) -> list[str]:
    """Extract all the passages from the html which contain an anniversary, and save their plain text in a list.
        For the pages in the given namespace, all the relevant passages start with a month href
         <p>
            <b>
                <a href="/wiki/April_1" title="April 1">April 1</a>
            </b>
            :
            ...
        </p>

    Parameters:
        - html (str): The html to parse
        - month (str): The month in interest, the page name of the Wikipedia:Selected anniversaries namespace

    Returns:
        - ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parentheses); Event 2; Event 3, something, something\n'
                                {Month} can be any month in the namespace and {day} is a number 1-31
    """
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Get all the paragraphs:
    paragraphs = soup.find_all("p")

    # only match the paragraphs starts with '<p><b><a href="/wiki/{Month}_{day}"' with optional <b> tag
    pattern = rf"""
    ^<p>\s*(<b>)*\s*                            # starts with paragraph tag, then optional space, optional b tag, optional space
    <a\shref="/wiki/{month.capitalize()}_\d     # then the a tag with the link formatted as explained
    """

    # Filter the passages to keep only the highlighted anniversaries
    ann_list = [
        i.text  # .text gets the paragraph text
        .strip()  # .strip strips the blank spaces at the ends
        for i in paragraphs if re.search(pattern, str(i), re.VERBOSE)
    ]

    return ann_list


def anniversary_list_to_df(ann_list: list[str]) -> pd.DataFrame:
    """Transform the list of anniversaries into a pandas dataframe.

    Parameters:
        ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parenthesis); Event 2; Event 3, something, something\n'
                                {Month} can be any month in months list and {day} is a number 1-31
    Returns:
        df (pd.Dataframe): A (dense) dataframe with columns ["Date"] and ["Event"] where each row represents a single event
    """
    # Store the split parts of the string as a table; drop the colon and the Month text
    ann_table = [i.partition(":") for i in ann_list]
    ann_table = [(i[0], i[2].split(";")) for i in ann_table]

    # Headers for the dataframe
    headers = ["Date", "Event"]
    df = (
        pd.DataFrame(ann_table, columns=headers)
        .explode("Event")  # expand list in Events column to seperate entry'
        .applymap(lambda x: x.strip() if isinstance(x, str) else x)  # strip edge whitespaces on all values
        .replace("", np.nan)  # replace empty entry strings to np.nan
        .dropna()  # drop these empty np.nan entries
        .reset_index(drop=True)  # remove index column, replace with dates
    )
    return df


def anniversary_table(
    namespace_url: str, month_list: list[str], work_dir: str | Path
) -> None:
    """Given the namespace_url and a month_list, create a markdown table of highlighted anniversaries for all of the months in list,
        from Wikipedia:Selected anniversaries namespace
    Parameters:
        - namespace_url (str):  Full url to the "Wikipedia:Selected_anniversaries/" namespace
        - month_list (list[str]) - List of months of interest, referring to the page names of the namespace
        - work_dir (str | Path) - (Absolute) path to your working directory
    Returns:
        None
    """
    # Loop through all months in month_list
    # Extract the html from the url (use one of the already defined functions from earlier)
    # Gather all highlighted anniversaries as a list of strings
    # Split into date and event
    # Render to a df dataframe with columns "Date" and "Event"
    # Save as markdown table

    work_dir = Path(work_dir)
    output_dir = work_dir / "tables_of_anniversaries"

    # Create output directory if it doesn't already exist
    if not output_dir.exists():
        output_dir.mkdir()

    for month in month_list:
        # Get month html
        page_url = namespace_url + month
        html = get_html(page_url)

        # Get the list of anniversaries
        ann_list = extract_anniversaries(html, month)

        # Render to a dataframe
        df = anniversary_list_to_df(ann_list).set_index("Date")  # remove the index column, replace with the dates

        # Convert to an .md table
        table = df.to_markdown()

        # Save the output
        with open(output_dir / f"anniversaries_{month.lower()}.md", "w", encoding="utf-8") as f:
            f.write(table)


if __name__ == "__main__":
    # make tables for all the months
    work_dir = "."
    namespace_url = "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
    anniversary_table(namespace_url, months_in_namespace, work_dir)
