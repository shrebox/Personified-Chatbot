from goodreads import client
from lxml import html
import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import re
import urlparse
import random
import json

gc = client.GoodreadsClient('IQZV2Svrg4aSntB0h8MFA', '8SjkCk5nVVBiqapZaYk6FyKWriKQTMNLuQabC04zw')

def quotes_from_url(quotes_URL): 
	if quotes_URL == '0': 
		return []

	quotes_page = BeautifulSoup(requests.get(quotes_URL).text, "html.parser")
	quotes_raw = quotes_page.find_all('div', {'class': "quoteText"})

	quotes = [] ###list of lists of the form [quote, author, title]
	for raw in quotes_raw: 
		data = []
		quote_raw = ''.join(text.encode('ascii', 'ignore') for text in raw.find_all(text=True) if text.parent.name not in ["script", "a", "span"])
		quote = quote_raw.lstrip().rstrip().rstrip(',').rstrip()

		data.append(quote)
		
		for text in raw.find_all(text=True):
			if text.parent.name == "a":
				data.append(text.encode('ascii', 'ignore'))

		if len(data) < 3: 
			#signifies no title of work
			data.append('')

		quotes.append(data)

	return quotes

def book_url(book_title):
    book_array = gc.search_books(book_title)

    URLs=[]
    for book in book_array:
        
        book_page = BeautifulSoup(requests.get(book.link).text, "html.parser")
        link_to_quotes = book_page.find_all('a', href=True, text = re.compile('Quotes from')) 
        if len(link_to_quotes) > 0:
            URLs.append(urlparse.urljoin('http://www.goodreads.com/', link_to_quotes[0]['href'])) 

    print URLs
    if len(URLs)>0:
        return URLs
    
    return '0'
def author_url(author_name):
    author = gc.find_author(author_name)
    if author is None: 
            return ['0']

    author_page = BeautifulSoup(requests.get(author.link).text, "html.parser")

    link_to_quotes = author_page.find_all('a', href=True, text = re.compile('Quotes by'))
    if len(link_to_quotes)>0:
        ext=link_to_quotes[0]['href']
    else:
        return '0'
    

    URLs = []

    for n in range(1,2):
            page_ext = '?page=' + str(n)
            page_url = urlparse.urljoin('http://www.goodreads.com/', ext, page_ext)
            page = BeautifulSoup(requests.get(page_url).text, "html.parser")
            if len(page.body.findAll(text=re.compile('^Sorry, no quotes found$'))) == 0:
                    URLs.append(page_url)
            else: 
                    break

    return URLs


authors = ['APJ Abdul Kalam']


URLs = []

for author_name in authors: 
	URLs.extend(book_url(author_name))

for author_name in authors: 
	URLs.extend(author_url(author_name))

final_quotes = []

for url in URLs:
    final_quotes.extend(quotes_from_url(url))

quotelist={}
random.shuffle(final_quotes)
print final_quotes
with open('quotes.txt', 'w') as f:
    for quotes in final_quotes:
       
        if quotes[2]=='':
                title='Misc'
                if 'Misc' not in quotelist:
                        quotelist['Misc']=[]
        else:
                title=quotes[2]
                if title not in quotelist:
                        quotelist[title]=[]
                        
        quotelist[title].append(quotes[0])
        
data=json.dumps(quotelist)
with open("quotes.json","w") as f:
  f.write(data)

