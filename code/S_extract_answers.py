import json
import re
from rake_nltk import Rake
from gensim.models import KeyedVectors

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
           
def sentence_similarilty_wmd(model,sentence1,sentence2): # lower score means more similar
  sentence1 = sentence1.lower().split()
  sentence2 = sentence2.lower().split()
  return model.wmdistance(sentence1, sentence2)

# inputg = '../data/glove/glove.6B.300d.txt' # file used to make word vectors; can use some other sentence sets
input_wordvector_embeddings = 'wrd2vec' #wrd2vec is glove vectors of the words file
# glove2word2vec(inputg,input_wordvector_embeddings)
model = KeyedVectors.load_word2vec_format(input_wordvector_embeddings, binary=False)
print "glove loading done"

query=raw_input("Enter query\n")         
tag=r.extract_keywords_from_text(query)
ranked_tags=r.get_ranked_phrases()
print 'Quote='+str(get_quote(query,ranked_tags))
print 'QNA='+str(get_qna(query,ranked_tags))

print sentence_similarilty_wmd(model,"this is a test sentence","testing is important task")
    

