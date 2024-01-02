"""
Created on 13.10.2023
"""

import re

"""
More

    Write a python script that takes in a string written in CamelCase, and prints it in snake_case

    Write a regex that matches your full name, but only captures your first name

    Write a regex that matches your full name, but only captures your last name

    Write a Python script takes in names on the form firstname [optional number of middle names] lastname and outputs them on the form f. m. lastname i.e. only keep first letters of the first- and middle names.

    Is it possible to use (only) regular expressions to check if e.g. all brackets in an expression are balanced?
"""


# CamelCase (really TitleCase/PascalCase/UpperCamelCase) to snake_case
def camelcase_to_snakecase(camelcase_string: str) -> str:
    """Returns the CamelCase string converted to snake_case. Leaves numbers untouched."""
    pattern = r"([A-Z0-9]{1})([a-z0-9]*)"
    new = ""
    for match in re.findall(pattern, camelcase_string):
        new += match[0].lower() + "".join(match[1:]) + "_"
    new = new.rstrip("_")
    return new


print("# CamelCase (really TitleCase/PascalCase/UpperCamelCase) to snake_case:")
string = "1ThisIsATest2String"
print(string, camelcase_to_snakecase(string), sep=" -> ")

# Write a regex that matches your full name, but only captures your first name
string = "Lasse Pladsen"
pattern = r"Lasse(?=\sPladsen)"
match = re.search(pattern, string)
print("\n# Write a regex that matches your full name, but only captures your first name:")
print(match)

# Write a regex that matches your full name, but only captures your last name
string = "Lasse Pladsen"
pattern = r"(?<=Lasse\s)Pladsen"
match = re.search(pattern, string)
print("\n# Write a regex that matches your full name, but only captures your last name:")
print(match)


# Write a Python script takes in names on the form firstname [optional number of middle names]
# lastname and outputs them on the form f. m. lastname i.e. only keep first letters of the first- and middle names.
def abbreviate_name(name: str) -> str:
    """Returns a abbreviate/shortened name in the format 'first_name. middle_name_1. middle_name2. ... last_name'."""
    pattern = r"([a-zA-Z]+)"
    new = ""
    matches = re.findall(pattern, name)
    for match in matches[:-1]:
        new += match[0] + ". "
    new += matches[-1]
    return new


string = "Lasse Blad Pladsen"
print("\n# Write a Python script takes in names on the form firstname [optional number of middle names:")
print(string, abbreviate_name(string), sep=" -> ")


# Is it possible to use (only) regular expressions to check if e.g. all brackets in an expression are balanced?
def has_unclosed_brackets(string: str) -> bool:
    """Boolean check for if all brackets in the given string are balanced (every opened bracket is closed)."""
    # Count the number of open and close parentheses
    open_count = len(re.findall(r'\(', string))
    close_count = len(re.findall(r'\)', string))

    # If the counts are not equal, there are unclosed parentheses
    return open_count != close_count


print("\n# Is it possible to use (only) regular expressions to check if"
      " e.g. all brackets in an expression are balanced?:")
unbalanced_string = "aw(test) bracket [testing] ) for [failed balancing brackets )"
print(unbalanced_string, has_unclosed_brackets(unbalanced_string), sep=" -> ")

balanced_string = "aw(test [test2] ) bracket [testing () ] for [failed balancing brackets] "
print(balanced_string, has_unclosed_brackets(balanced_string), sep=" -> ")
