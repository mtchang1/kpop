"""
Note: The article's timestamp on the site is assumed to be of the same
      timezone as the server (if not specified by the site).
"""

import urllib2
import string
from bs4 import BeautifulSoup
import sqlite3
import time as timelib

user_agent = 'Mozilla/5'
headers = { 'User-Agent' : user_agent }

#scrape allkpop.com
#sending out GET request
request = urllib2.Request("http://allkpop.com/tag/b-a-p", None, headers)
response = urllib2.urlopen(request)

#parse html
soup = BeautifulSoup(response.read())
results = soup.find_all('article')
news = []

for result in results:
    try:
        time = result.find('span', class_="timestamp").contents[2].strip()
        t=timelib.strptime(time,"%b %d, %Y at %I:%M %p")
        epochtime = timelib.mktime(t)
    except ValueError as details:
        #fail gracefully and go on to next article
        print "Timestamp parsing error: %s" % details
        continue
    except AttributeError:
        #no more articles left
        break
    temp = result.find('h2').find('a')
    #is unicode() necessary?
    title = unicode(temp.string).strip()
    url = temp['href']
    img = result.find('div',class_='row-col-left').find('img')['src']
    text = unicode(result.find('p').string).strip()
    news.append(('allkpop.com', time, epochtime,  url, img, text, title))

#kpopstarz.com
#send Get request
request = urllib2.Request("http://www.kpopstarz.com/archives/"
                          "articles/tags/b-a-p", None, headers)
response = urllib2.urlopen(request)

#parse html
soup = BeautifulSoup(response.read())
results = soup.find_all("div", class_="summary")
news2 = [] 

for result in results:
    time = unicode(result.find('span', class_="date").string)
    #stripping off timezone because library doesn't support it for some reason
    #webfaction library
    try:
        t = timelib.strptime(time[:-4],"%B %d, %Y | %H:%M %p")
        epochtime = timelib.mktime(t)
    except ValueError as details:
        #fail gracefully and go on to next article
        print "Timestamp parsing error: %s" % details
        continue
    temp = result.find('h3').find('a')
    title = unicode(temp.string)
    url = "http://www.kpopstarz.com" + temp['href']
    blurb = unicode(result.find('p').string)
    img = result.find('a').find('img')['src']
    #print url
    news2.append(('kpopstarz.com',time, epochtime, url, img, blurb, title)) 

allnews = news+news2

#store in database

#db_dir = root_dir + '/news.db'
conn = sqlite3.connect('news.db')
c = conn.cursor()
create_table1 = \
    """
    CREATE TABLE IF NOT EXISTS articles
        (title TEXT PRIMARY KEY, url TEXT UNIQUE, time TEXT, epochtime REAL, 
         dbtime TEXT, site TEXT, img TEXT, abstract TEXT);
    """
create_table2 = \
    """
    CREATE TABLE IF NOT EXISTS sites (domain TEXT PRIMARY KEY);
    """
insert_trigger = \
    """
    CREATE TRIGGER IF NOT EXISTS new_article AFTER INSERT ON articles
    begin
        UPDATE articles SET dbtime = datetime('now','localtime')
        WHERE rowid = new.rowid;
    end;
    """
update_trigger = \
    """
    CREATE TRIGGER IF NOT EXISTS update_article AFTER UPDATE OF url ON articles
    begin
        UPDATE articles SET dbtime = datetime('now','localtime')
        WHERE rowid = new.rowid;
    end;
    """
c.execute(create_table1)
c.execute(create_table2)
c.execute(insert_trigger)
c.execute(update_trigger)
 
for article in allnews:
    c.execute("UPDATE OR FAIL articles SET "
              "site=?, time=?, epochtime=?, url=?, img=?, abstract=? "
              "WHERE title=?", article)
    if c.rowcount == 0:
        c.execute("INSERT OR REPLACE INTO articles "
              "(site, time, epochtime, url, img, abstract, title) "
              "VALUES (?,?,?,?,?,?,?)", article)

sites = ['allkpop.com','kpopstarz.com']
for site in sites:
    c.execute("INSERT OR IGNORE INTO sites (domain) VALUES (?)", (site,))

conn.commit()
conn.close()
