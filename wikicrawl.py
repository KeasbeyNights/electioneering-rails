import json
import urllib2
import urllib
import time
import traceback
import wikiparse
from bs4 import BeautifulSoup

def get_titles():
  titles = []
  f = open('candidates.txt')
  lines = f.readlines()
  f.close()
  for line in lines:
    candidate = line.split('\t')[0]
    print candidate
    titles.append(candidate)
  return titles

def get_pages(titles):
  result = {}
  for title in titles:
    print 'fetching', title
    title_url = urllib.quote(title.encode('utf8'))
    try:
      #data = json.loads(urllib2.urlopen('http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=%s&rvprop=content&format=json' % title_url).read())
      #print data['query']['pages'].values()[0]['revisions'][0]['*']
      soup = BeautifulSoup(urllib2.urlopen('http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=%s&rvprop=content&format=json' % title_url).read())
      print soup.prettify()
      break
    except:
      traceback.print_exc()
    result[title] = data['query']['pages'].values()[0]['revisions'][0]['*']
  return result



def test_indexing(index):
  d = json.loads(open('wiki.json', 'r').read())
  conn = pyes.ES('zapjot-api-lb-624473521.us-west-1.elb.amazonaws.com:9200', default_indexes=[index])
  t = time.time()
  n = 0
  for (title, content) in d.items():
    print 'indexing', title, float(n) / float(time.time() - t), ' / s'
    conn.index({'title': title, 'content': content}, index, 'wikipage')
    n += 1

if __name__ == "__main__":
  result = get_pages(get_titles())
  f = open('results.txt', 'w')
  print type(result)
  f.flush()
  wikiparse.parse(f)

