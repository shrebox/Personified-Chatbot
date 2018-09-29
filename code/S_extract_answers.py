import json
import re
from rake_nltk import Rake

r = Rake() 

def jaccard(a,b):

    a1=set(a)
    b1=set(b)
    return len(a1.intersection(b1))/(1.0*len((a1).union(b1)))

def sen_sim(a,b):
    return 0

def cleantext(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  return cleantext

def get_qna(query,querytags):

  maxx=0
  maxx_qna=''
  with open('tagged_qna.json', 'r') as f:
      qadict = json.load(f)    
      for index in qadict:
          ans=jaccard(qadict[index]['tag'],querytags)+sen_sim(qadict[index]['ans'],query)
          if ans>maxx:
              maxx=ans
              maxx_qna=qadict[index]['ans']
              
  return maxx_qna

 

def get_quote(query,querytags):
    
   maxx=0
   maxx_quote=''
   with open('tagged_quotes.json', 'r') as f:
      quotesdict = json.load(f)    
      for book in quotesdict:        
          qlist=quotesdict[book]
          for quote in qlist:
              ans=jaccard(quote['tag'],querytags)+sen_sim(quote['quote'],query)
              if ans>maxx:
                  maxx=ans
                  maxx_quote=quote['quote']

   return maxx_quote
           

query=raw_input("Enter query\n")         
tag=r.extract_keywords_from_text(query)
ranked_tags=r.get_ranked_phrases()
print 'Quote='+str(get_quote(query,ranked_tags))
print 'QNA='+str(get_qna(query,ranked_tags))

    

