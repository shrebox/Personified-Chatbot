from lxml import html
import requests
from bs4 import BeautifulSoup, Comment, NavigableString
import re
import urlparse
import random
import json

i = 1
final_data = {}
while True and i<759:

    request = requests.get('http://abdulkalam.nic.in/Answer/Questions{0}.html'.format(i))
    soup = BeautifulSoup(request.text, 'lxml')

    reviews = soup.find_all("div",{"class": "speech"})

    if len(reviews)!=0:
        for items in reviews:
            question = str(items.find("li" ,{"style":"padding:0px 0px 20px 20px;"})).split('">')[1].split('</')[0].lstrip().rstrip()
            answer =""
            try:
                answer = str(items.find("li" ,{"style":"padding:0px 0px 10px 20px;"})).split('">')[1].split('</')[0].lstrip().rstrip()
            except:
                answer = str(items.find("li" ,{"style":"padding:0px 10px 10px 20px;"})).split('">')[1].split('</')[0].lstrip().rstrip()
            final_data[question] = answer
            print i,question,answer
    i+=1


        # #If there is no more page break loop.
        # if len(reviews) != 0:
        #     for item in reviews:
        #         review = item.find("div", {"class": "tipText"}).text
        #         date = item.find("span",{"class":"tipDate"}).text
        #         # upv = item.findAll("div",{"class":"tipUpvoteDownvoteButton"})
        #         # print temp, upv
        #         # actionb = item.find("div",{"class":"actionButtons"}   )
        #         # upvote = actionb.find("span",{"class":"tipUpvoteCount"}).text
        #         tlist = []
        #         tlist.append(review.encode('utf-8'))
        #         tlist.append(date)
        #         if idval not in final_reviews:
        #             final_reviews[idval] = []
        #         final_reviews[idval].append(tlist)
        #         # print temp, review.encode('utf-8'), date
        #         temp+=1
        #     i += 1
        # else:
        #     break


# with open('ques_ans.json', 'r') as f:
#     qadict = json.load(f)
#     c=0
#     for index in qadict:
#             c=c+1
#     c=c+1

#     questions,answers=get_ques_ans()
  
#     for i in range(len(questions)):
#             print i
#             if c not in qadict:
#                 qadict[c]={}
#                 if 'ques' not in qadict[c]:
#                         qadict[c]['ques']=questions[i]
#                 if 'ans' not in qadict[c]:
#                         qadict[c]['ans']=answers[i]
#             c=c+1
            
#     data=json.dumps(qadict)
#     with open("ques_ans2.json","w") as f:
#             f.write(data)           
