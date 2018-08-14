# -*- coding: utf-8 -*-
import re
import urllib
from bs4 import BeautifulSoup


def clean_quote(quote, references):  # To remove stray html tags from the retrieved results
    quote = re.sub('<.*?>', '', quote)
    quote = '“' + quote + '”' + ' ― '

    ref_length = len(references)
    if (ref_length > 0):
        quote = quote + references[0]
        for i in range(1, ref_length - 1):
            quote = quote + ', ' + references[i]
        if (ref_length > 1):
            quote = quote + ', ' + references[-1]
    return quote


quote_tag = input("Enter quote tag: ")
query_url = 'https://www.goodreads.com/quotes/tag/' + quote_tag
page = 1
all_quotes = ''
print("Retrieving all quotes tagged as \"%s\"..." % quote_tag)
print("...............")

while(1):
    paged_query_url = query_url + '?page=' + str(page)
    print(paged_query_url)
    try:
        query = urllib.request.urlopen(paged_query_url)
        html = query.read()
        soup = BeautifulSoup(html, "lxml")
        quotes = soup.findAll("div", class_="quoteText")
        if (len(quotes) == 0):
            break

        for item in quotes:
            tex = str(item)
            quote = re.findall('“(.*)”', tex)
            ref = re.findall('<a .*>(.*)<\/a>', tex)
            all_quotes = all_quotes + clean_quote(quote[0], ref) + '\n'

        page = page + 1
    except urllib.error.HTTPError as err:
        print("Request error: ", err.reason)
        break
    except urllib.error.URLError as err:
        print("Some other error happend:", err.reason)
        break

# export all quotes
with open('quotes1_' + quote_tag + '.txt', 'w') as fp:
    fp.write(all_quotes)
