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
      & Q(party = names[3])).first()
    state = names[2]
    if candidate is None:
      candidate = Politician()
      candidate.name = names[0]
      candidate.candidate_type = names[1]
      candidate.party = names[3]
    candidate.save()
    titles[names[0]] = [candidate, names[1], state]
  return titles

def get_pages(names):
  result = {}
  data = ""
  for title in names:
    print 'fetching', title
    firstlast = title.split(' ')
    #print firstlast
    title_url = firstlast[0] + '_' + firstlast[1]
    cand_type = titles[title][1]
    state = titles[title][2]
    url = 'http://www.thepoliticalguide.com/Profiles/%s/%s/%s/' %(cand_type, state, title_url)
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
  stance = ""
  RE = re.compile(r'<div class=\"repitem\"><b>Positions that we are tracking for this rep: </b>(.+?)</div>')
  count = 1
  dat = RE.findall(data)
  issues =  dat[0].split(', ')
  filename = poli.lower().replace(' ', '') + '.txt'
  f = open(filename,'w')
  cand_type = titles[poli][1]
  state = titles[poli][2]
  topics = ['Abortion', 'Education', 'Energy and the Environment', 'Foreign Policy', 
    'Gay Marriage', 'Health Care', 'Immigration', 'TARP', 'Taxes', 'The Second Amendment']
  for topic in issues:
    if topic in topics:
      print topic
      f.write(topic)
      firstlast = poli.split(' ')
      title_url = firstlast[0] + '_' + firstlast[1]
      url_topic = topic.replace(' ', '_')
      url = 'http://www.thepoliticalguide.com/Profiles/%s/%s/%s/Views/%s' %(cand_type, 
        state, title_url, url_topic)
      data = urllib2.urlopen(url).read().encode('utf-8')
      RE = re.compile(r'<h2>Summary</h2>.*?<p.*?>(.*?)<', re.DOTALL)
      summ_list = RE.findall(data)
      if len(summ_list) > 0:
        summ = summ_list[0]
      else:
        summ = ""
      sent = summ.split('.')
      stance = ""
      for sentence in sent:
        for keyword in keywords[topic]:
          if keyword in sentence:
            stance = sentence
            break
      if stance == "" and not sum == "":
        stance = sent[0]
      issue = Issue.objects(name = topic, politician_id=titles[poli][0].id).first()
      if not issue:
        issue = Issue()
        if(topic == 'The Second Amendment'):
          issue.name = 'Gun Policy'
        elif (topic == 'TARP'):
          issue.name = 'Jobs'
        else:
          issue = topic
      print stance.encode('utf-8')
      issue.stance = stance.encode('utf-8')
      f.write(stance)
      issue.politician_id = titles[poli][0].id
      issue.save()
      f.write('\n\n')
    print '------------------------------------------------'


if __name__ == "__main__":
  MONGODB_HOST = 'mongodb://stingray:pennapps@ds037587-a.mongolab.com:37587/heroku_app7603312'
  MONGODB_DATABASE = 'heroku_app7603312'
  connect(MONGODB_DATABASE, host=MONGODB_HOST)
  global titles
  global keywords
  keywords = dict()
  keywords['Abortion'] = ['pro-life','pro-choice']
  keywords['Education'] = ['public school', 'public education', 'private school', 
                          'charter school', 'voucher']
  keywords['Energy and the Environment'] = ['oil', 'nuclear','wind','solar','coal']
  keywords['Foreign Policy'] = ['stance', 'leader', 'sanction']
  keywords['Gay Marriage'] = ['civil union', 'support', 'traditional', 'oppose']
  keywords['The Second Amendment'] = ['support', 'oppose', 'restriction']
  keywords['Health Care'] = ['Medicare', 'Medicaid', 'public option', 'mandates']
  keywords['Immigration'] = ['border', 'amnesty', 'oppose', 'support',' DREAM']
  keywords['TARP'] = ['support', 'oppose']
  keywords['Taxes'] = ['income', 'state', 'federal', 'propery', 'sales', 'sin', 'lower', 'raise', 'breaks']
  titles = get_titles()
  result = get_pages(titles.keys())
  for title in titles.keys():
    parse_data(title, result[title])


  
  

