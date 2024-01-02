"""
Created on 13.10.2023
"""

import re

"""
Substitution
Enclose the group of b’s in parentheses in the following strings: 'aaaabbbccc', 'aaab'.
"""



# 'aaaabbbccc'
pattern = r"(.*?)(b+)(.*?)"
replace = r"\1(\2)\3"
string = 'aaaabbbccc'
new = re.sub(pattern, replace, string)
print(f"'aaaabbbccc'  ->  '{new}'")


# 'aaab'
string = 'aaab'
new = re.sub(pattern, replace, string)
print(f"'aaab'  ->  '{new}'")
