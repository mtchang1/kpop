#!/usr/bin/python
import urllib
import urllib2
import string
import sys
from bs4 import BeautifulSoup
import sqlite3

user_agent = 'Mozilla/5'
headers = { 'User-Agent' : user_agent }

#allkpop.com
#sending out GET request
request = urllib2.Request("http://allkpop.com/tag/b-a-p", None, headers)
response = urllib2.urlopen(request)

#extracting information
soup = BeautifulSoup(response.read())
results = soup.find_all('article')
news = []

for result in results:
    try:
        time = result.find('span', class_="timestamp").contents[2]
    except AttributeError:
        break
    temp = result.find('h2').find('a')
    title = unicode(temp.string)
    url = temp['href']
    news.append((time, url, title))

#kpopstarz.com
user_agent = 'Mozilla/5'
headers = { 'User-Agent' : user_agent }

request = urllib2.Request("http://www.kpopstarz.com/archives/articles/tags/b-a-p", None, headers)
response = urllib2.urlopen(request)

soup = BeautifulSoup(response.read())
results = soup.find_all("div", class_="summary")
news2 = [] 

for result in results:
    time = unicode(result.find('span', class_="date").string)
    temp = result.find('h3').find('a')
    title = unicode(temp.string)
    url = "http://www.kpopstarz.com" + temp['href']
    blurb = unicode(result.find('p').string)
    img = result.find('a').find('img')['src']
    print url
    news2.append((time, url, title, blurb, img)) 


#store in database
conn = sqlite3.connect('news.db')
c = conn.cursor()
for article in news:
    try:
        c.execute('INSERT INTO links (time, url, title) values (?,?,?)',article)
    except sqlite3.IntegrityError as detail:
        #print detail
        print "Already added: %s" % article[2]
conn.commit()
conn.close()
