# I-am-Kalam
Analyzing answer pattern of APJ Abdul Kalam and responding to a query following his answering pattern. <br />
We are applying RNNs to generate answers to user queries. <br/>

IR-IE model <br>
To run: $ python sen2vec_my.py

** sent2vec library needs to be installed.<br>
** pre trained model <a href='https://drive.google.com/file/d/0B6VhzidiLvjSOWdGM0tOX1lUNEk/view'>torontobooks_unigrams.bin</a> needs to be installed.

seq2seq model <br>
TO run: $ python main.py to train the system and save the model named as model.npz.<br>
Set inference_mode=1 for testing purpose and run python main.py.

References <br />
https://github.com/facebookarchive/NAMAS <br />
https://github.com/zwc12/Summarization <br />
<h5>For Similarity</h5> 
https://datascience.stackexchange.com/questions/23969/sentence-similarity-prediction <br />
https://rare-technologies.com/doc2vec-tutorial/ <br />
http://nlp.town/blog/sentence-similarity/ <br />
https://radimrehurek.com/gensim/models/keyedvectors.html <br />
https://machinelearningmastery.com/develop-word-embeddings-python-gensim/ <br />
https://github.com/epfml/sent2vec <br />

<h5>RNNs</h5>
https://pdfs.semanticscholar.org/ffbb/1d120c3c2881431933c6f928b851824913c4.pdf?_ga=2.35884901.416918627.1538253292-1431390683.1533485502<br />
https://arxiv.org/pdf/1603.06155.pdf <br />
Link: https://people.cs.umass.edu/~ashutoshchou/persona_chatbot_report.pdf <br />
Code: https://github.com/ashutosh-choudhary/conversational_agent_personified<br />
Blog: https://towardsdatascience.com/personality-for-your-chatbot-with-recurrent-neural-networks-2038f7f34636<br />
<br />
^some more links for code that have implemented kinda same thingy<br />
https://github.com/manumathewthomas/Chat-with-Joey<br />
https://github.com/inikdom/neural-chatbot<br />
https://github.com/tensorlayer/seq2seq-chatbot <br>
https://github.com/epfml/sent2vec


MAIN LINK
http://adventuresinmachinelearning.com/keras-lstm-tutorial/

Tada! (:)
