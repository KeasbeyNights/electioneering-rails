import re
import collections

RE = re.compile(r"<title>(?P<title>.*?)</title>.*?<text.*?>(?P<content>.*?)</text>", re.DOTALL)

Article = collections.namedtuple("Article", ["title", "content"])

def parse(f):
    return (Article(*item) for item in RE.findall(f.read()))

#print list(parse(open("Wikipedia-commercials.xml","r")))[0]
