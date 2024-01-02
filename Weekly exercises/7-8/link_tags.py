"""
Created on 13.10.2023
"""

import re

"""
Link tags

Write a regex that matches the href-part of an HTML anchor tag if it is a (reasonably) valid URL. for instance

<a href="www.google.com">This is a link to Google</a>
"""


url_pattern = r"w{3}\.[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,}"
pattern = fr"<a href=\"{url_pattern}\">"
string = '<a href="www.google.com">This is a link to Google</a>'
match = re.search(pattern, string)
print(match)
