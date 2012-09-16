import json
import urllib2
import urllib
import time
import traceback
from mongoengine import *
import re


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
  f = open('senators.txt')
  lines = f.readlines()
  f.close()
  for line in lines:
    names = line.split('\t')
    print names
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
    #print firstlast
    title_url = title.replace(' ','_')
    cand_url = titles[title][1]
    if(cand_url == 'senator'):
      cand_url = 'Senate'
    state = titles[title][2]
    state_url = state.replace(' ', '_')
    url = 'http://www.thepoliticalguide.com/Profiles/%s/%s/%s/' %(cand_url, state_url, title_url)
    print url
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
  topics = ['Abortion', 'Education', 'Energy and the Environment', 'Foreign Policy', 
    'Gay Marriage', 'Health Care', 'Immigration', 'TARP', 'Taxes', 'The Economy','The Second Amendment']
  print poli
  for topic in issues:
    if topic in topics:
      print topic
      f.write(topic)
      title_url = title.replace(' ','_')
      cand_url = titles[poli][1]
      if(cand_url == 'senator'):
       cand_url = 'Senate'
      state = titles[poli][2]
      state_url = state.replace(' ', '_')
      url_topic = topic.replace(' ', '_')
      url = 'http://www.thepoliticalguide.com/Profiles/%s/%s/%s/Views/%s/' %(cand_url, 
        state_url, title_url, url_topic)
      data = urllib2.urlopen(url).read()
      RE = re.compile(r'<h2>Summary</h2>.*?<p.*?>(.*?)<', re.DOTALL)
      summ_list = RE.findall(data)
      summ = ''
      voting = False
      if len(summ_list) > 0:
        summ = summ_list[0]
      else:
        RE2 = re.compile(r'<div class="(yes|no)vote"><p>(.*?)</p>')
        record = RE2.findall(data)
        if len(record) > 0:
          summ = record[0][1]
          voting = True
      if not voting:
        sent = summ.split('.')
        stance = ""
        for sentence in sent:
          for keyword in keywords[topic]:
            if keyword in sentence:
              if topic == 'The Economy' or topic == 'Jobs':
                stance = sentence
              else:
                stance = keyword
                if topic == 'Immigration':
                  if stance == 'support' or stance == 'DREAM':
                    stance = 'more open borders'
                  elif stance == 'against' or stance == 'oppose':
                    stance = 'stricter borders'
        if stance == "" and not sum == "":
          stance = sent[0]
      else:
        stance = summ
      issue = Issue.objects(Q(name = topic) & Q(politician_id=titles[poli][0].id)).first()
      if issue is None:
        issue = Issue()
        if(topic == 'The Second Amendment'):
          issue.name = 'Gun Policy'
        elif (topic == 'TARP'):
          issue.name = 'Jobs'
        elif topic == 'The Economy':
          issue.name = 'Entitlements'
        else:
          issue.name = topic
      print stance
      issue.stance = stance
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
  keywords['Gay Marriage'] = ['civil union', 'support', 'traditional', 'oppose', 'against']
  keywords['The Second Amendment'] = ['support', 'oppose', 'restriction']
  keywords['Health Care'] = ['Medicare', 'Medicaid', 'public option', 'mandates']
  keywords['Immigration'] = ['border', 'amnesty', 'oppose', 'support',' DREAM']
  keywords['TARP'] = ['support', 'oppose']
  keywords['Taxes'] = ['income', 'state', 'federal', 'propery', 'sales', 'sin', 'lower', 'raise', 'breaks']
  keywords['The Economy'] = ['stimulate the economy', 'Keynesian', 'supporter', 'oppose']
  titles = get_titles()
  result = get_pages(titles.keys())
  for title in titles.keys():
    parse_data(title, result[title])


  
  

