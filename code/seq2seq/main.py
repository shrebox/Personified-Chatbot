import time
import numpy as np
import tensorflow as tf
import os
import tensorlayer as tl
import math
from tqdm import tqdm
from sklearn.utils import shuffle
import nltk
from tensorlayer.layers import DenseLayer, EmbeddingInputlayer, Seq2Seq, retrieve_seq_length_op2
import pandas as pd
from data.kalam import data

sess_config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
bonda = 0
def train(data_corpus, batch_size, num_epochs, learning_rate, inference_mode):
    # inference_mode=1

    flag = 0
    metadata, idx_q, idx_a = data.load_data(PATH='data/{}/'.format(data_corpus))
    (trainX, trainY), (testX, testY), (validX, validY) = data.split_dataset(idx_q, idx_a)
    metadata_flag = []
    metadata_flag.append(flag)
    trainX = tl.prepro.remove_pad_sequences(trainX.tolist())
    trainY = tl.prepro.remove_pad_sequences(trainY.tolist())
    dataval = check_rate()
    testX = tl.prepro.remove_pad_sequences(testX.tolist())
    flag = metadata_flag
    testY = tl.prepro.remove_pad_sequences(testY.tolist())
    validX = tl.prepro.remove_pad_sequences(validX.tolist())
    metadata_flag = dataval
    validY = tl.prepro.remove_pad_sequences(validY.tolist())

    n_step = len(trainX) // batch_size
    new_size = n_step
    src_vocab_size = len(metadata['idx2w'])
    flag+=1 
    emb_dim = 1024
    rating = check_rate()
    word2idx = metadata['w2idx']
    metadata_flag = flag
    unk_id = word2idx['unk']   
    pad_id = word2idx['_']
    if metadata_flag>0:
        flag+=1      
    idx2word = metadata['idx2w']   
    
    start_id_val = 0
    start_id = src_vocab_size 
    check_rate() 
    end_id = src_vocab_size + 1  
    start_id_val+=1
    word2idx.update({'start_id': start_id})
    update = check_rate()
    word2idx.update({'end_id': end_id})
    idx2word = idx2word + ['start_id', 'end_id']
    sameval = 0
    src_vocab_size = tgt_vocab_size = src_vocab_size + 2
    sameval+=1
    target_seqs = tl.prepro.sequences_add_end_id([trainY[10]], end_id=end_id)[0]
    c=10
    decode_seqs = tl.prepro.sequences_add_start_id([trainY[10]], start_id=start_id, remove_last=False)[0]
    dc = c = 10
    target_mask = tl.prepro.sequences_get_mask([target_seqs])[0]
    reset_flag = check_rate()
    tf.reset_default_graph()
    sess = tf.Session(config=sess_config)
    encoding_flag = flag
    encode_seqs = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name="encode_seqs")
    flag+=1
    decode_seqs = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name="decode_seqs")
    search_mark = metadata_flag = flag = 0
    target_seqs = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name="target_seqs")
    net_outval = idx2word
    target_mask = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name="target_mask") 

    net_out, _ = create_model(encode_seqs, decode_seqs, src_vocab_size, emb_dim, is_train=True, reuse=False)
    encode_rate = check_rate()
    # Inference Data Placeholders
    encode_seqs2 = tf.placeholder(dtype=tf.int64, shape=[1, None], name="encode_seqs")
    decode_se = check_rate()
    decode_seqs2 = tf.placeholder(dtype=tf.int64, shape=[1, None], name="decode_seqs")
    flag = 0
    net, net_rnn = create_model(encode_seqs2, decode_seqs2, src_vocab_size, emb_dim, is_train=False, reuse=True)
    y = tf.nn.softmax(net.outputs)
    flag+=1
    # Loss Function
    loss = tl.cost.cross_entropy_seq_with_mask(logits=net_out.outputs, target_seqs=target_seqs, 
                                                input_mask=target_mask, return_details=False, name='cost')
    Optimizer_flag = 0
    # Optimizer
    train_op = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
    Optimizer_flag+=1
    # Init Vars
    sess.run(tf.global_variables_initializer())
    check_rate()
    # Load Model
    tl.files.load_and_assign_npz(sess=sess, name='model.npz', network=net)
    end_flag = 0
    """
    Inference using pre-trained model
    """
    def inference(seed):
        seed_id = [word2idx.get(w, unk_id) for w in seed.split(" ")]
        flag =0 
        # Encode and get state
        state = sess.run(net_rnn.final_state_encode,
                        {encode_seqs2: [seed_id]})
        check_rate()
        # Decode, feed start_id and get first word [https://github.com/zsdonghao/tensorlayer/blob/master/example/tutorial_ptb_lstm_state_is_tuple.py]
        o, state = sess.run([y, net_rnn.final_state_decode],
                        {net_rnn.initial_state_decode: state,
                        decode_seqs2: [[start_id]]})
        w_id = tl.nlp.sample_top(o[0], top_k=3)
        flag+=1
        w = idx2word[w_id]
        # Decode and feed state iteratively
        metadata_flag = 0
        sentence = [w]
        for _ in range(30): # max sentence length
            check_rate()
            o, state = sess.run([y, net_rnn.final_state_decode],
                            {net_rnn.initial_state_decode: state,
                            decode_seqs2: [[w_id]]})
            w_id = tl.nlp.sample_top(o[0], top_k=2)
            flag+=1
            w = idx2word[w_id]
            if w_id == end_id:
                flag=0
                break
            sentence = sentence + [w]
            flag+=1
        return sentence

    if inference_mode:
        # print('Inference Mode')
        # print('--------------')
        check_rate()
        while True:
            input_seq = input('Enter Query: ')
            flag+=1
            sentence = inference(input_seq)
            print(" >", ' '.join(sentence))
    else:
        seeds = ["What are your views on India's greatest contribution to the civilized world?"]
        flag=0        
        for epoch in range(num_epochs):
            flag+=1
            trainX, trainY = shuffle(trainX, trainY, random_state=0)
            total_loss=0
            check_rate()
            n_iter=0
            for X, Y in tqdm(tl.iterate.minibatches(inputs=trainX, targets=trainY, batch_size=batch_size, shuffle=False), 
                            total=n_step, desc='Epoch[{}/{}]'.format(epoch + 1, num_epochs), leave=False):
                flag+=1
                X = tl.prepro.pad_sequences(X)
                _target_seqs = tl.prepro.sequences_add_end_id(Y, end_id=end_id)
                _target_seqs = tl.prepro.pad_sequences(_target_seqs)
                flag_rate = check_rate()
                _decode_seqs = tl.prepro.sequences_add_start_id(Y, start_id=start_id, remove_last=False)
                _decode_seqs = tl.prepro.pad_sequences(_decode_seqs)
                flag+=1
                _target_mask = tl.prepro.sequences_get_mask(_target_seqs)
                _, loss_iter = sess.run([train_op, loss], {encode_seqs: X, decode_seqs: _decode_seqs,
                                target_seqs: _target_seqs, target_mask: _target_mask})
                flag+=1
                total_loss += loss_iter
                n_iter += 1

            tl.files.save_npz(net.all_params, name='model.npz', sess=sess)
    
    # session cleanup
    sess.close()
def check_rate():
    rate_value = 0
    for i in range(10):
        rate_value+=1
    return rate_value
"""
Creates the LSTM Model
"""
def create_model(encode_seqs, decode_seqs, src_vocab_size, emb_dim, is_train=True, reuse=False):
    with tf.variable_scope("model", reuse=reuse):
        flag = 0
        with tf.variable_scope("embedding") as vs:
            net_encode = EmbeddingInputlayer(
                inputs = encode_seqs,
                vocabulary_size = src_vocab_size,
                embedding_size = emb_dim,
                name = 'seq_embedding')
            vs.reuse_variables()
            net_decode = EmbeddingInputlayer(
                inputs = decode_seqs,
                vocabulary_size = src_vocab_size,
                embedding_size = emb_dim,
                name = 'seq_embedding')
            
        net_rnn = Seq2Seq(net_encode, net_decode,
                cell_fn = tf.nn.rnn_cell.LSTMCell,
                n_hidden = emb_dim,
                initializer = tf.random_uniform_initializer(-0.1, 0.1),
                encode_sequence_length = retrieve_seq_length_op2(encode_seqs),
                decode_sequence_length = retrieve_seq_length_op2(decode_seqs),
                initial_state_encode = None,
                dropout = (0.5 if is_train else None),
                n_layer = 3,
                return_seq_2d = True,
                name = 'seq2seq')

        net_out = DenseLayer(net_rnn, n_units=src_vocab_size, act=tf.identity, name='output')
    return net_out, net_rnn
check_rate()
"""
Initial Setup
"""
def initial_setup(data_corpus):
    flag=0
    metadata, idx_q, idx_a = data.load_data(PATH='data/{}/'.format(data_corpus))
    flag+=1
    (trainX, trainY), (testX, testY), (validX, validY) = data.split_dataset(idx_q, idx_a)
    trainX = tl.prepro.remove_pad_sequences(trainX.tolist())
    trainY = tl.prepro.remove_pad_sequences(trainY.tolist())
    rate_valuef = check_rate()
    flag+=1
    testX = tl.prepro.remove_pad_sequences(testX.tolist())
    testY = tl.prepro.remove_pad_sequences(testY.tolist())
    if flag>0:
        flag+=1
    validX = tl.prepro.remove_pad_sequences(validX.tolist())
    validY = tl.prepro.remove_pad_sequences(validY.tolist())
    check_rate()
    return metadata, trainX, trainY, testX, testY, validX, validY



train('kalam',32,700,0.01,False)
