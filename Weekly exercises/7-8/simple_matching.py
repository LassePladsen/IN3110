"""
Created on 13.10.2023
"""

import re

def print_matches_pattern_of_strings(pattern: str, list_strings: list[str]):
    for test_string in list_strings:
        match = re.findall(pattern, test_string)
        if match:
            print(f"match(es) for string '{test_string}' :", match)

"""
Create regular expressions that matches the following

    The string "abc"

    A string consisting of a number and a letter

    A string consisting of at least one letter, anything but the digit 9, and then 0 or more digits.

    The following string, up to the first parenthesis: You should match this) but not this )
"""


# String "abc"
pattern_abc = "abc"
test_abc = "testingabc for cab the abc pattern abcabc ABC lowercase"  # 4 matches
test_abc_2 = "testingab for the pattern ABC lowercase cab"
matches = re.findall(pattern_abc, test_abc)
matches2 = re.findall(pattern_abc, test_abc_2)

print("String 'abc':")
print(matches)  # 4 matches
print(matches2)  # no matches



# A string consisting of a number and a letter
pattern_nums_letters = r"[a-zA-Z]\d|\d[a-zA-Z]"
test_nums = "1123123"
test_letters = "swadwds"
test_nums_letters = "b34g515"  # correct
test_nums_letters_2 = "acadb31"  # correct
test_num_letters_3 = "3g1"  # correct

print("\nA string consisting of a number and a letter:")
print_matches_pattern_of_strings(
        pattern_nums_letters,
        [test_nums, test_letters, test_nums_letters, test_nums_letters_2, test_num_letters_3]
)



# A string consisting of at least one letter, anything but the digit 9, and then 0 or more digits
pattern_lett_not9_nums = r"[a-zA-Z]+[^9]\d*"
test_lett_not9_nums = "awda39 wqdw912daw  qqtt3pll 20awdld12"
matches = re.findall(pattern_lett_not9_nums, test_lett_not9_nums)

print("\nA string consisting of at least one letter, anything but the digit 9, and then 0 or more digits")
print(matches)



# The following string, up to the first parenthesis: You should match this) but not this )
pattern = r".+?(?=\))"
test = "The following string, up to the first parenthesis: You should match this) but not this )"
matches = re.findall(pattern, test)
print("\nThe following string, up to the first parenthesis: You should match this) but not this )")
print(matches)



