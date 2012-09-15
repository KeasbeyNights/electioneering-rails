import json
import urllib2
import urllib
import time
import traceback
import wikiparse
from bs4 import BeautifulSoup
from mongoengine import *



class Politician(Document):
  name = StringField()
  candidate_type = StringField()
  party = StringField()

  meta = {'collection' : 'politicians'}

class Issue(Document):
  name = StringField()
  stance = StringField()
  politician_id = ObjectIdField()
  meta = {'collection' : 'issues'}

def get_titles():
  titles = {}
  f = open('candidates.txt')
  lines = f.readlines()
  f.close()
  for line in lines:
    names = line.split('\t')
    candidate = Politician.objects(Q(name = names[0]) & Q(candidate_type = names[1])
      & Q(party = names[2])).first()
    if candidate is None:
      candidate = Politician()
      candidate.name = names[0]
      candidate.candidate_type = names[1]
      candidate.party = names[2]
      candidate.save()
    titles[names[0]] = candidate
  return titles

def get_pages(titles):
  result = {}
  for title in titles:
    print 'fetching', title
    title_url = urllib.quote(title.encode('utf8'))
    try:
      data = json.loads(urllib2.urlopen('http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=%s&rvprop=content&format=json' % title_url).read())
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
  MONGODB_HOST = 'mongodb://stingray:pennapps@ds037587-a.mongolab.com:37587/heroku_app7603312'
  MONGODB_DATABASE = 'heroku_app7603312'
  connect(MONGODB_DATABASE, host=MONGODB_HOST)
  global titles
  titles = get_titles()
  result = get_pages(titles.keys())
  for title in titles.keys():
    parse_data(politician, result[title])
    print data.split('\n')[0]
    issue = Issue()
    issue.name = 'Sexual Education'
    issue.stance = data.split('\n')[0]
    politician = titles[title]
    issue.politician_id = politician.id
    issue.save()


  
  

