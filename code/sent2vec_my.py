import sent2vec
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
import numpy as np
import operator
from gensim.summarization import summarize

def sentence_similarity():
	model = sent2vec.Sent2vecModel()
	model.load_model('torontobooks_unigrams.bin')
	question = str(raw_input("Enter query sentence: "))
	a = [e[0] for e in model.embed_sentence(question).reshape(-1,1)]
	data = np.load('data.npy').item()

	similar_dic = {}
	for k,v in data.iteritems():
		b = [e[0] for e in model.embed_sentence(k).reshape(-1,1)]
		result=1-spatial.distance.cosine(a,b)
		similar_dic[k] = result

	sorted_list = sorted(similar_dic.items(), key=operator.itemgetter(1),reverse=True)

	# print data[sorted_list[0][0]]
	# print data[sorted_list[1][0]]
	# print data[sorted_list[2][0]]
	# print ""

	final_3_qna_dic = {}

	final_3_qna_dic[sorted_list[0][0]] = data[sorted_list[0][0]]
	final_3_qna_dic[sorted_list[1][0]] = data[sorted_list[1][0]]
	final_3_qna_dic[sorted_list[2][0]] = data[sorted_list[2][0]]

	topdata = final_3_qna_dic

	text = ""

	for k,v in topdata.iteritems():
		text+=v
		text+=" "

	sumresp = summarize(text, word_count = 50)

	return sumresp.replace('\n',' ')

print sentence_similarity()

#https://github.com/epfml/sent2vec
