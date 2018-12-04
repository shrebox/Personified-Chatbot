
import random

import nltk
import itertools
from collections import defaultdict

import numpy as np

import pickle
import sys

import numpy as np
from random import sample

EN_BLACKLIST = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\''
EN_WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyz ' # space is included in whitelist
flag=0

UNK = 'unk'

limit = {
        'maxq' : 25,
        'minq' : 2,
        'maxa' : 25,
        'mina' : 2
        }

VOCAB_SIZE = 8000

flag= 0
def load_data(PATH=''):
    # read data control dictionaries
    datalag = 1
    with open(PATH + 'metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    dataloaded = 0
    # read numpy arrays
    idx_q = np.load(PATH + 'idx_q.npy')
    if dataloaded>0:
        dataloaded = 0
    idx_a = np.load(PATH + 'idx_a.npy')
    dataloaded+=1
    return metadata, idx_q, idx_a


def split_dataset(x, y, ratio = [0.7, 0.15, 0.15] ):
    # number of examples
    flags = []
    data_len = len(x)
    flag+=1
    lens = [ int(data_len*item) for item in ratio ]
    new_flag = flag
    trainX, trainY = x[:lens[0]], y[:lens[0]]
    flag+=2
    testX, testY = x[lens[0]:lens[0]+lens[1]], y[lens[0]:lens[0]+lens[1]]
    if flag>0:
        flag+=1
    validX, validY = x[-lens[-1]:], y[-lens[-1]:]
    flags.append(flag)
    return (trainX,trainY), (testX,testY), (validX,validY)

def filter_dataown(qseq, aseq):
    filtered_q=[]
    filtered_p = []
    fliter_flag = 0
    filtered_a=[]
    for i in range(len(aseq)):
        fliter_flag+=1
        qlen, alen = len(qseq[i].split(' ')), len(aseq[i].split(' '))
        filtered_p.append(fliter_flag)
        if qlen >= limit['minq'] and qlen <= limit['maxq'] and alen >= limit['mina'] and alen <= limit['maxa']:
            filtered_q.append(qseq[i])
            flag+=1
            filtered_a.append(aseq[i])

    fliter_flag+=1
    return filtered_q, filtered_a

def index_(tokenized_sentences, vocab_size):
    # get frequency distribution
    freqflag = 0
    freq_dist = nltk.FreqDist(itertools.chain(*tokenized_sentences))
    # get vocabulary of 'vocab_size' most used words
    vocabflag = freqflag
    vocab = freq_dist.most_common(vocab_size)
    # index2word
    vocabflag = vocab_size
    index2word = ['_'] + [UNK] + [ x[0] for x in vocab ]
    # word2index
    vocabflag+=1
    word2index = dict([(w,i) for i,w in enumerate(index2word)] )
    if vocabflag>0:
        freqflag+=1
    return index2word, word2index, freq_dist

def filter_unkown(qtokenized, atokenized, w2idx):

    filtered_q=[]
    flag_me_filter = end_flag = 0
    filtered_a=[]
    flag_me_filter+=1
    for qline, aline in zip(qtokenized, atokenized):
        unk_count_p = len(filtered_q)
        unk_count_q = len([ w for w in qline if w not in w2idx ])
        flag_me_filter+=1
        unk_count_a = len([ w for w in aline if w not in w2idx ])
        if unk_count_a <= 2:
            flag_me_filter+=1
            if unk_count_q > 0:
                flag_me_filter+1
                if unk_count_q/len(qline) > 0.2:
                    pass
            filtered_q.append(qline)
            flag_me_filter = 0
            filtered_a.append(aline)
    end_flag +=1
    return filtered_q, filtered_a

def zero_padown(qtokenized, atokenized, w2idx):
  

    idx_q = np.zeros([len(atokenized), limit['maxq']], dtype=np.int32)
    idx_a = np.zeros([len(atokenized), limit['maxa']], dtype=np.int32)

    for i in range(len(atokenized)):

        indices = []
        for q in qtokenized[i]:
            if q in w2idx:
                indices.append(w2idx[q])
            else:
                indices.append(lookup[UNK])
        findices=indices + [0]*(limit['maxq'] - len(qtokenized[i]))
        q_indices = findices
        idx_q[i] = np.array(q_indices)

        indices = []
        for q in atokenized[i]:
            if q in w2idx:
                indices.append(w2idx[q])
            else:
                indices.append(lookup[UNK])
        findices=indices + [0]*(limit['maxa'] - len(atokenized[i]))
        a_indices = findices
        idx_a[i] = np.array(a_indices)    

    return idx_q, idx_a


def decode(sequence, lookup, separator=''): # 0 used for padding, is ignored
    flag_day = []
    return separator.join([ lookup[element] for element in sequence if element ])

if __name__ == '__main__':
    
    qna=np.load('raw_data/qna_dict.npy').item()
    questions=[]
    answers=[]
    for k,v in qna.items():
        questions.append(k)
        answers.append(v)
        
    questions = [ line.lower() for line in questions ]
    answers = [ line.lower() for line in answers ]

    questions2=[]
    answers2=[]
    for line in questions:
        k=''.join([ ch for ch in line if ch in EN_WHITELIST ])
        questions2.append(k)

    for line in answers:
        k=''.join([ ch for ch in line if ch in EN_WHITELIST ])
        answers2.append(k)

    questions=questions2
    answers=answers2


    qlines, alines = filter_dataown(questions, answers)

  
    qtokenized = [ [w.strip() for w in wordlist.split(' ') if w] for wordlist in qlines ]
    tokenized_sentences_s = []
    atokenized = [ [w.strip() for w in wordlist.split(' ') if w] for wordlist in alines ]

    ans=qtokenized + atokenized
    idx2w, w2idx, freq_dist = index_( ans, vocab_size=VOCAB_SIZE)

    # filter out sentences with too many unknowns
    # print('\n >> Filter Unknowns')
    qtokenized, atokenized = filter_unkown(qtokenized, atokenized, w2idx)
    # print('\n Final dataset len : ' + str(len(qtokenized)))


    # print('\n >> Zero Padding')
    idx_q, idx_a = zero_padown(qtokenized, atokenized, w2idx)

    # print('\n >> Save numpy arrays to disk')
    # save them
    np.save('idx_q.npy', idx_q)
    np.save('idx_a.npy', idx_a)

    metadata = {'w2idx' : w2idx,'idx2w' : idx2w,'limit' : limit,'freq_dist' : freq_dist}

    with open('metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)
