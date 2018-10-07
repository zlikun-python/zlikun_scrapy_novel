# -*- coding: utf-8 -*-
import re

matcher = re.search(r'/(\d+).html$', 'https://www.biquge5200.cc/79_79067/148312116.html')
# <class 're.Match'> <re.Match object; span=(34, 49), match='/148312116.html'>
print(type(matcher), matcher)

assert int(matcher.group(1)) == 148312116
