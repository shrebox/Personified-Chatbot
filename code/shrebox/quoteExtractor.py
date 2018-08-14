# # -*- coding: utf-8 -*-

# # This is a simple python script that requests the name of a book/author 
# # and prints out the top 30 relevant quotes as found on Goodreads (www.goodreads.com)

# # This script uses BeautifulSoup-4 to perform the final html parsing to retrieve the quotes and
# # a python wrapper for the Goodreads API to retrieve the relevant bookID from the given string raw_input

# # Link to the python wrapper: https://github.com/sefakilic/goodreads 

# from goodreads import client
# import re
# import urllib
# from bs4 import BeautifulSoup

# def cleanedUpQuote(quote):              # To remove stray html tags from the retrieved results
#     quote = re.sub('<.*?>','',quote)
#     return quote


# CONSUMER_KEY = "<Insert your CONSUMER_KEY>"
# CONSUMER_SECRET ="<Insert your CONSUMER_SECRET>"


# gc = client.GoodreadsClient(CONSUMER_KEY,CONSUMER_SECRET)

# gc.authenticate(CONSUMER_KEY,CONSUMER_SECRET)

# bookName = raw_input("Enter the name of your favorite book(Enter Author's name to retrive top quotes from the author): ")

# print "Hold on while we retrieve the top quotes..."


# bookIdList = gc.search_books(bookName)

# baseUrl = 'https://www.goodreads.com/work/quotes/'
# editedBookName = bookName.replace(' ','-')
# s = bookIdList[0]+'-'+editedBookName
# finalUrl = baseUrl + s;
# # print finalUrl

# print "..............."
# print 
# print 

# html = urllib.urlopen(finalUrl).read()
# soup = BeautifulSoup(html,"lxml")

# # print soup
# quotesPart = soup.findAll("div",class_="quoteText")

# for item in quotesPart:
#     tex = str(item)

#     matchQ = re.findall('“(.*)”',tex)
#     print cleanedUpQuote(matchQ[0])
#     print 


from goodreads import client
from lxml import html
import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import re
import urlparse
import random

# gc = client.GoodreadsClient('rskLlD77MN7AaQ89Od2AJg', 'VjalvAPZEyzyqvDcPWzY8yg6e832Jh5NPZffuiVkw')
gc = client.GoodreadsClient('IQZV2Svrg4aSntB0h8MFA', '8SjkCk5nVVBiqapZaYk6FyKWriKQTMNLuQabC04zw')

def quotes_from_url(quotes_URL): 
	if quotes_URL == '0': 
		return []

	quotes_page = BeautifulSoup(requests.get(quotes_URL).text, "lxml")
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
	# print book_array	
	if len(book_array) > 0: 
		book = book_array[0]
	else:
		return '0'
	book_page = BeautifulSoup(requests.get(book.link).text, "lxml")
	# print book_page
	link_to_quotes = book_page.find_all('a', href=True, text = re.compile('Quotes from')) 
	# print link_to_quotes
	if len(link_to_quotes) > 0: 
		return urlparse.urljoin('http://www.goodreads.com/', link_to_quotes[0]['href'])
	else: 
		return '0'

def author_url(author_name):
	author = gc.find_author(author_name)
	if author is None: 
		return ['0']

	author_page = BeautifulSoup(requests.get(author.link).text, "lxml")
	link_to_quotes = author_page.find_all('a', href=True, text = re.compile('Quotes by'))
	if len(link_to_quotes) > 0: 
		ext = link_to_quotes[0]['href']

	else: 
		return ['0']

	URLs = []
	
	for n in range(1,2):
		page_ext = '?page=' + str(n)
		page_url = urlparse.urljoin('http://www.goodreads.com/', ext, page_ext)
		page = BeautifulSoup(requests.get(page_url).text, "lxml")
		if len(page.body.findAll(text=re.compile('^Sorry, no quotes found$'))) == 0: 
			URLs.append(page_url)
		else: 
			break

	return URLs

print "hi"

book_titles = ['Absalom, Absalom!', 'House of Mirth', 'Count of Monte Cristo', 'Fire in the Blood', 'Lolita']
authors = ['William Faulkner', 'Edith Wharton', 'Italo Calvino', 'Vladimir Nabokov']

URLs = []

print "book urls"

for book_title in book_titles: 
	URLs.append(book_url(book_title))

print "author urls"

for author_name in authors: 
	URLs.extend(author_url(author_name))

final_quotes = []

print "quotes from urls"

for url in URLs: 
	final_quotes.extend(quotes_from_url(url))

random.shuffle(final_quotes)

print "printing quotes.txt"

with open('quotes.txt', 'w') as f:
    for quotes in final_quotes:
        f.write(quotes[0]+ '\n')
        f.write(quotes[1] + ' ' + quotes[2] + '\n')