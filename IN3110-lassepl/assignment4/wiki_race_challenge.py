"""
Bonus task
"""
from __future__ import annotations

import time
import networkx as nx
from collections import deque

from requesting_urls import get_html
from filter_urls import find_articles_english


def find_path(start: str, finish: str, max_depth: int = 20) -> list[str]:
    """Find the shortest path from `start` to `finish` using only english wikipedia article URLS.
    Uses a breadth-first search on each article link and appends edges to a networkx.Graph() graph article collection.
    Then when the finish article's link is found, use Dijkstra's Algorithm on the now created graph
    to find the shortest path from 'start' to 'finish'.

    Summary:
    Each link found on a given article gets added as a edge node to the parent article's node.
    Given enough finite time the total graph when the finish link is found should give
    the shortest path using Dijkstra's Algorithm from the start node to the finish node.

    Inspired by Peder Ward's article: https://towardsdatascience.com/beating-wikirace-by-finding-the-optimal-path-with-neo4j-and-dijkstras-algorithm-1e11193c55bb

    IN3110 GRADING NOTE: This can sometimes take VERY long, sometimes its faster depending on which link it began with.
    On my desktop pc it varies from 2min to 8 min +-.


    Arguments:
      start (str): wikipedia article URL to start from
      finish (str): wikipedia article URL to stop at
      max_depth (int): maximum link depth from the start article to search for the finish article, defaults to 20

    Returns:
      urls (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
        -> Returns an empty list if no path was found within the max depth.
    """
    print(f"Finding shortest path between '{start}' and '{finish}' within {max_depth=}, please be patient...\n")

    # Create the graph
    graph = nx.Graph()

    # Initialize deque for fast appends and pops; acts as the article queue
    queue = deque()
    queue.append(start)

    # Keep track of visited articles to avoid duplicate and possible infinite loops
    visited = set()

    depth = 0
    while queue:
        # Path not found within the max depth
        if depth >= max_depth:
            return []

        # Make a copy of the queue to not modifty it during iteration
        current_articles = list(queue)
        queue.clear()

        # Iterate through each link in queue
        for current_article in current_articles:
            if current_article in visited:
                continue

            # Add current article to the visited set
            visited.add(current_article)

            # Get all article URLs on the current page
            articles = find_articles_english(get_html(current_article))

            # End if finish is found in this new articles set (current article has a link to the finish article)
            if finish in articles:
                graph.add_edge(current_article, finish)
                return nx.shortest_path(graph, source=start, target=finish)

            # Otherwise add each new article as a graph edge node to the current article's node, also add it to queue
            for article in articles:
                if article not in visited:
                    queue.append(article)
                    graph.add_edge(current_article, article)

        depth += 1

    return []  # Path not found


if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"

    start_time = time.time()  # time the elapsed run time
    path = find_path(start, finish)
    elapsed_time = time.time() - start_time
    if path:  # found shortest path
        print(f"Found shortest path of {len(path) - 1} links in {elapsed_time:.3g}s from '{start}' to '{finish}'.")
        print("Link path:")
        print(*path, sep="\n")  # print each link on separate lines

    else:  # no path found within max depth
        print(f"No path found within max depth in {elapsed_time:.3g}s from '{start}' to '{finish}'")
