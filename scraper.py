import urllib
import urllib2
import string
import sys
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5'
headers = { 'User-Agent' : user_agent }

#sending out GET request (I think)
request = urllib2.Request("http://allkpop.com/tag/b-a-p", None, headers)
response = urllib2.urlopen(request)

#need to implement: go through all b-a-p/page/* until title of page: not found

#extracting information
soup = BeautifulSoup(response.read())
results = soup.find_all('article')
news = []
#something else
for result in results:
    print result
    try:
        time = result.find('span', class_="timestamp").contents[2]
    except AttributeError:
        break
    #NEED TO: sort date by year month day time
    temp = result.find('h2').find('a')
    title = unicode(temp.string)
    url = temp['href']
    news.append((time, url, title))

print(news)
