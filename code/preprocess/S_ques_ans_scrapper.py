from lxml import html
import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import re
import urlparse
import random
import json

def get_ques_ans():
        soup = BeautifulSoup(requests.get('http://www.abdulkalam.com/kalam/theme/jsp/guest/QuestionAnswers.jsp?startIndex=0&txtnumrec=10').text, "html.parser")
        c=0
        questions=[]
        answers=[]
        while c<90:
                c=c+10
                if c>10:
                        ques = soup.find_all('a', {'data-parent': "#accordion"})
                        for q in ques:
                                q1=q.text.split('<')[0].split("View Answer")[0].split(".")[1:]
                                qs='.'.join(q1).strip()
                                questions.append(qs)
                                
                        ans  = soup.find_all('div', {'style': "margin: 0 0 10px;"})
                        for a in ans:
                                answers.append(a.text.split("</p>")[0].split("Answer:")[1].strip().replace('\r','').replace('\n',''))
                soup = BeautifulSoup(requests.get('http://www.abdulkalam.com/kalam/theme/jsp/guest/QuestionAnswers.jsp?startIndex='+str(c)+'&txtnumrec=10').text, "html.parser")

        return questions,answers

with open('ques_ans.json', 'r') as f:
    qadict = json.load(f)
    c=0
    for index in qadict:
            c=c+1
    c=c+1

    questions,answers=get_ques_ans()
  
    for i in range(len(questions)):
            print i
            if c not in qadict:
                qadict[c]={}
                if 'ques' not in qadict[c]:
                        qadict[c]['ques']=questions[i]
                if 'ans' not in qadict[c]:
                        qadict[c]['ans']=answers[i]
            c=c+1
            
    data=json.dumps(qadict)
    with open("ques_ans2.json","w") as f:
            f.write(data)           
