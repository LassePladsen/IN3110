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
Email
Write a regex that matches (reasonable) e-mail addresses.
"""


pattern = r"^[a-zA-Z0-9]+\.?[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,}$"
test1 = "lasse.pladsen@hotmail.com"  # match
test2 = "lasse.pladsen@hotmail.no"  # match
test3 = "lasse.pladsen@hotmail.n"
test4 = "lasse.pladsen@hot@mail.com"
test5 = "lasse.pla@dsen@hotmail.com"
test6 = "lasse@pladsen@hotmail.com"
test7 = ".pladsen@hotmail.com"
test8 = "lasse.@hotmail.com"
test9 = "lasse.pladsen.hotmail.com"
test10 = "lasse.pladsen.hotmail@com"
test11 = "lasse.pladsen@.com"
test12 = "lass_e.pl_adsen@hotmail.no"
test13 = "john@doe.no"  # match
test14 = "john@doe.com"  # match

print_match_for_regex(
        pattern,
        [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14]
)
