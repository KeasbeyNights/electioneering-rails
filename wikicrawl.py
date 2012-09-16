import json
import urllib2
import urllib
import time
import traceback
import wikiparse
from bs4 import BeautifulSoup
from mongoengine import *
import re
import nltk.data
import html5lib


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
  data = ""
  for title in titles:
    print 'fetching', title
    firstlast = title.split(' ')
    #print firstlast
    title_url = firstlast[0] + '_' + firstlast[1]
    url = 'http://www.thepoliticalguide.com/Profiles/President/US/%s/' % title_url
    #print url
    try:
      data = urllib2.urlopen(url).read()
      #print data    
    except:
      traceback.print_exc()
    result[title] = data
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

def parse_data(poli, data):
  RE = re.compile(r'<div class=\"repitem\"><b>Positions that we are tracking for this rep: </b>(.+?)</div>')
  count = 1
  dat = RE.findall(data)
  issues =  dat[0].split(', ')
  print issues
  filename = poli.lower().replace(' ', '') + '.txt'
  f = open(filename,'w')
  topics = ['Abortion', 'Education', 'Energy and the Environment', 'Foreign Policy', 
    'Gay Marriage', 'Health Care', 'Immigration', 'Social Security', 'Taxes', 'The American Jobs Act', 
    'The Economy', 'The War in Iraq']
  for topic in dat:
    if topic in topics:
      f.write(topic)
      issue = Issue.objects(name = topic).first()
      if not issue:
        issue = Issue()
        issue.name = topic
      count+=1
      stance = dat[count].strip('=')
      repl = re.compile(r'(\[\[.*?\]\])|(\{\{.*?\}\})|(<ref.*?>)|</ref>')
      stance = repl.sub('', stance)
      sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
      for token in sent_detector.tokenize(stance):
        f.write(token.encode('ascii','ignore') + '\n')
      issue.politician_id = titles[poli].id
      issue.save()
      f.write('\n\n')
      break
    count+=1
    print '------------------------------------------------'


if __name__ == "__main__":
  MONGODB_HOST = 'mongodb://stingray:pennapps@ds037587-a.mongolab.com:37587/heroku_app7603312'
  MONGODB_DATABASE = 'heroku_app7603312'
  connect(MONGODB_DATABASE, host=MONGODB_HOST)
  global titles
  titles = get_titles()
  result = get_pages(titles.keys())
  for title in titles.keys():
    parse_data(title, result[title])


  
  

