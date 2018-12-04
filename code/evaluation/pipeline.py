
import json
import re
from sent2vec_my import sentence_similarity
import nltk

def rogue2_bleu(gt,pred):
    tokens = nltk.word_tokenize(gt)
    bigramgt = set(nltk.bigrams(tokens))
    tokens = nltk.word_tokenize(pred)
    bigrampred = set(nltk.bigrams(tokens))
    return (len(bigramgt.intersection(bigrampred)))/(len(bigramgt)*1.0),(len(bigramgt.intersection(bigrampred)))/(len(bigrampred)*1.0)

def cleantext(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  return cleantext

with open('tagged_qna.json', 'r') as f:

      qadict = json.load(f)
      sumr=0
      sumb=0
      c=0
      for index in qadict:     
          c=c+1
          ques=cleantext(qadict[index]['ques'].strip())
          ansgt=cleantext(qadict[index]['ans'].strip())
          try:
            anspred=sentence_similarity(ques)
            ans=rogue2_bleu(ansgt,anspred)
            sumr=sumr+ans[0]
            sumb=sumb+ans[1]
          except:
            c=c-1

print('ROGUE-2')
print(sumr/(c*1.0))
print('BLEU')
print(sumb/(c*1.0))
          