# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/3 10:51
# @author   :Mo
# @function :train of fast text with baidu-qa-2019 in question title

import pathlib
import sys
import os

project_path = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)
sys.path.append(project_path)
print(project_path)

from keras_textclassification.conf.path_config import path_embedding_random_char, path_hyper_parameters_fast_text
from keras_textclassification.conf.path_config import path_baidu_qa_2019_train, path_baidu_qa_2019_valid
from keras_textclassification.conf.path_config import path_model_fast_text_baiduqa_2019
from keras_textclassification.etl.text_preprocess import PreprocessText
from keras_textclassification.m09_TextCRNN.graph import CRNNGraph as Graph

if __name__=="__main__":
    hyper_parameters = {'model': {   'label': 17,
                                     'batch_size': 16,
                                     'embed_size': 30,
                                     'filters': [2, 3, 4], # 论文中 filters=3
                                     'filters_num': 300, # 论文中 filters_num=150,300
                                     'channel_size': 1,
                                     'dropout': 0.5,
                                     'decay_step': 100,
                                     'decay_rate': 0.9,
                                     'epochs': 20,
                                     'len_max': 50,
                                     'vocab_size': 20000, #这里随便填的，会根据代码里修改
                                     'lr': 1e-3,
                                     'l2': 0.001,
                                     'activate_classify': 'softmax',
                                     'embedding_type': 'random', # 还可以填'random'、 'bert' or 'word2vec"
                                     'is_training': True,
                                     'model_path': path_model_fast_text_baiduqa_2019,
                                     'path_hyper_parameters': path_hyper_parameters_fast_text,
                                     'num_rnn_layers': 1, # 论文是2，但训练实在是太慢了
                                     'rnn_type': 'LSTM', # type of rnn, select 'LSTM', 'GRU', 'CuDNNGRU', 'CuDNNLSTM', 'Bidirectional-LSTM', 'Bidirectional-GRU'
                                     'rnn_units': 256,  # large 650, small is 300
                                     },
                        'embedding':{ 'embedding_type': 'random',
                                      'corpus_path': path_embedding_random_char,
                                      'level_type': 'char',
                                      'embed_size': 30,
                                      'len_max': 50,
                                      }, #  We also initialize the word vector for the unknown words from the uniform distribution [-0.25, 0.25].
                         }
    import time
    time_start  = time.time()

    graph = Graph(hyper_parameters)
    ra_ed = graph.word_embedding
    pt = PreprocessText()
    x_train, y_train = pt.preprocess_baidu_qa_2019_idx(path_baidu_qa_2019_train, ra_ed, rate=0.01)
    x_val, y_val = pt.preprocess_baidu_qa_2019_idx(path_baidu_qa_2019_valid, ra_ed, rate=0.01)
    print(len(y_train))
    graph.fit(x_train, y_train, x_val, y_val)
    print("耗时:" + str(time.time()-time_start))