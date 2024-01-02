"""
Created on 13.10.2023
"""

import re


def print_match_for_regex(pattern: str, string_list: list[str]):
    for string in string_list:
        match = re.findall(pattern, string)
        if match:
            print(f"Match for '{string}'.")


"""
Reasonable url
"""


pattern = r"w{3}\.[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,}"
string = 'www.google.com'  # match
string2 = 'ww.google.com'
string3 = 'www.google.c'
string4 = 'www..com'
string5 = 'www.a.com'  # match

print_match_for_regex(pattern, [string, string2, string3, string4, string5])