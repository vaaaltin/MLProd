# script.py

import parse
from reader import feed

tutorial = feed.get_article(1)
headlines = [
    r.named["header"]
    for r in parse.findall("\n## {header}\n", tutorial)
]
print("\n".join(headlines))