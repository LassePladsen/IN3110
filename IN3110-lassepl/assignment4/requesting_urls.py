"""
Task 1.1 - requesting HTML documents with HTTP
"""
from __future__ import annotations

import requests


def get_html(url: str, params: dict | None = None, output: str | None = None):
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
    assert response.status_code == 200,\
        f"Request was not as anticipated (status code 200), status code is {response.status_code}."

    # Get html from response
    html_str = response.text

    if output:
        # if output is specified, the response url and text content are written to the file `output`
        with open(output, "w") as outfile:
            outfile.write(url)
            outfile.write(html_str)

    return html_str
