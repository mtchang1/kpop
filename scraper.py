#!/usr/bin/python
import urllib2
import string
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
        time = result.find('span', class_="timestamp").contents[2].strip()
    except AttributeError:
        break
    temp = result.find('h2').find('a')
    title = unicode(temp.string).strip()
    url = temp['href']
    #image
    img = result.find('div',class_='row-col-left').find('img')['src']
    #abstract
    text = unicode(result.find('p').string).strip()
    news.append(('allkpop.com', time, url, title, img, text))

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
create_table1 = \
    """
    CREATE TABLE IF NOT EXISTS articles
        (title TEXT PRIMARY KEY, url TEXT UNIQUE, time TEXT, dbtime TEXT,
         site TEXT, img TEXT, abstract TEXT);
    """
create_table2 = \
    """
    CREATE TABLE IF NOT EXISTS sites (domain TEXT PRIMARY KEY);
    """
create_trigger = \
    """
    CREATE TRIGGER IF NOT EXISTS new_article AFTER INSERT ON articles
    begin
        UPDATE articles SET dbtime = datetime('now','localtime')
        WHERE rowid = new.rowid;
    end;
    """
c.execute(create_table1)
c.execute(create_table2)
c.execute(create_trigger)
    
for article in news:
    try:
        c.execute("INSERT INTO articles (site, time, url, title, img, abstract) "
                  "VALUES (?,?,?,?,?,?)", article)
    except sqlite3.IntegrityError as detail:
        #print detail
        print "Already added: %s" % article[2]

sites = ['allkpop.com']
for site in sites:
    c.execute("INSERT OR IGNORE INTO sites (domain) VALUES (?)", (site,))

conn.commit()
conn.close()
