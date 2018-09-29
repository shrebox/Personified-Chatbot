import json
import re
import nltk
from rake_nltk import Rake
from gensim.models import KeyedVectors
from nltk import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

st = set(stopwords.words('english'))
stop_words=set()
for s in st:
	s=s.encode('ascii', 'ignore')
	stop_words.add(s)

# inputg = '../data/glove/glove.6B.300d.txt' # file used to make word vectors; can use some other sentence sets
input_wordvector_embeddings = 'wrd2vec' #wrd2vec is glove vectors of the words file
# glove2word2vec(inputg,input_wordvector_embeddings)
model = KeyedVectors.load_word2vec_format(input_wordvector_embeddings, binary=False)
print "glove loading done"

r = Rake() 

def jaccard(a,b):

    a1=set(a)
    b1=set(b)
    return len(a1.intersection(b1))/(1.0*len((a1).union(b1)))


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
          ans=jaccard(qadict[index]['tag'],querytags)+(1-sentence_similarilty_wmd(model,qadict[index]['ans'],query))
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
              ans=jaccard(quote['tag'],querytags)+(1-sentence_similarilty_wmd(model,quote['quote'],query))
              if ans>maxx:
                  maxx=ans
                  maxx_quote=quote['quote']

   return maxx_quote
           
def sentence_similarilty_wmd(model,sentence1,sentence2): # lower score means more similar


  c=0
  s1=word_tokenize(sentence1.lower())
  for ss in s1:
      if ss not in stop_words:
          c=c+1
          
  sentence1 = sentence1.lower().split()

  s2=word_tokenize(sentence2.lower())
  for ss in s2:
      if ss not in stop_words:
          c=c+1

  sentence2 = sentence2.lower().split()
  return model.wmdistance(sentence1, sentence2)/(c*1.0)


def rogue2_bleu(gt,pred):
    tokens = nltk.word_tokenize(gt)
    bigramgt = set(nltk.bigrams(tokens))
    tokens = nltk.word_tokenize(pred)
    bigrampred = set(nltk.bigrams(tokens))

    return (len(bigramgt.intersection(bigrampred)))/(len(bigramgt)*1.0),(len(bigramgt.intersection(bigrampred)))/(len(bigrampred)*1.0)
    
query=raw_input("Enter query\n")         
tag=r.extract_keywords_from_text(query)
ranked_tags=r.get_ranked_phrases()
print 'Quote='+str(get_quote(query,ranked_tags))
print 'QNA='+str(get_qna(query,ranked_tags).encode('utf-8'))



    
