"""
Task 1.2, 1.3

Filtering URLs from HTML
"""

from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse


def find_urls(
        html: str,
        base_url: str = "https://en.wikipedia.org",
        output: str | None = None,
) -> set[str]:
    """
    Find all the url links in a html text using regex

    Arguments:
        html (str): html string to parse
        base_url (str): the base url to the wikipedia.org pages
        output (Optional[str]): file to write to if wanted
    Returns:
        urls (Set[str]) : set with all the urls found in html text
    """
    urls = set()

    # Create and compile regular expression(s):
    # finds all <a> tags including the contents
    a_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)

    # collects the url part of a href attribute match in a group
    href_pat = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)

    # 1. find all the anchor tags
    for a_tag in a_pat.findall(html):
        # 2. then find the urls href attribute
        href_attr = href_pat.search(a_tag)

        if not href_attr:  # no matches, skip
            continue

        # Get the url from the first group
        url = href_attr.group(1)

        # Parse url: add a default protocol scheme if missing
        parsed_url = urlparse(url, scheme="https")

        # filter out path fragments
        parsed_url = parsed_url._replace(fragment="")

        # If missing both path and netloc, this was a fragment-only link, skip it
        if not parsed_url.path and not parsed_url.netloc:
            continue

        if parsed_url.netloc:
            url = parsed_url.geturl()
        else:  # has no netloc -> url is relative path: add the given base url
            url = urljoin(base_url, parsed_url.geturl())

        # Add the now FULL url to the set
        urls.add(url)

    # Write to file if requested
    if output:
        print(f"Writing to: '{output}'")
        with open(output, "w") as outfile:
            outfile.writelines(line + "\n" for line in urls)  # add linebreak between lines
    return urls


def find_articles(
        html: str,
        output: str | None = None,
        base_url: str = "https://en.wikipedia.org"
) -> set[str]:
    """Finds all the wiki articles inside a html text. Makes call to find_urls(), and filters out non-wikipedia urls.
    arguments:
        - text (str) : the html text to parse
        - output (str, optional): the file to write the output to if wanted
    returns:
        - (Set[str]) : a set with urls to all the articles found
    """
    # Get ALL urls in the html
    urls = find_urls(html, base_url)

    pattern = r"""
    (?:https://|http://)    # starts with https:// or http://
    [a-zA-Z\-_]{2,}         # two or more letters/hyphen/underscore representing the language of the article
    \.wikipedia\.org/wiki/  # .wikipedia.org/wiki/ base path
    (?:/*\S+)*              # ends with any amount of: forward slash followed by any non-whitespace char
    """

    # Find all matches
    articles = re.findall(pattern, " ".join(urls), re.VERBOSE)

    # Filter out any articles with colon after the protocol (https:)
    articles = set(article for article in articles if ":" not in article[6:])

    # Write to file if wanted
    if output:
        with open(output, "w") as outfile:
            outfile.writelines(line + "\n" for line in articles)  # add linebreak between lines
    return articles


def find_articles_english(
        html: str,
        output: str | None = None,
        base_url: str = "https://en.wikipedia.org"
) -> set[str]:
    """Finds all the ENGLISH wiki articles inside a html text. Makes call to find_urls(), and filters out
    non-wikipedia urls. This is faster than creating a separate function using find_articles() then filtering
    out non-english articles. This is specifically used for the bonus task wiki_race_challenge.py
    arguments:
        - text (str) : the html text to parse
        - output (str, optional): the file to write the output to if wanted
    returns:
        - (Set[str]) : a set with urls to all the articles found
    """
    # Get ALL urls in the html
    urls = find_urls(html, base_url)

    pattern = r"""
    (?:https://|http://)    # starts with https:// or http://
    en                      # english wikipedia article
    \.wikipedia\.org/wiki/  # .wikipedia.org/wiki/ base path
    (?:/*\S+)*              # ends with any amount of: forward slash followed by any non-whitespace char
    """

    # Find all matches
    articles = re.findall(pattern, " ".join(urls), re.VERBOSE)

    # Filter out any articles with colon after the protocol (https:)
    articles = set(article for article in articles if ":" not in article[6:])

    # Write to file if wanted
    if output:
        with open(output, "w") as outfile:
            outfile.writelines(line + "\n" for line in articles)  # add linebreak between lines
    return articles


def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attribute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)

    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()

    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
