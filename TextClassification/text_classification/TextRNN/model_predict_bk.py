#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: li
@file: model_predict_bk.py
@time: 2020/2/14 10:09 下午
"""
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import os
import argparse
import tensorflow as tf
import tensorflow.contrib.keras as kr

# from rnn_model import TRNNConfig, TextRNN
from bi_rnn_model import TBRNNConfig, TextBiRNN
from cnnews_loder import read_category, read_vocab

try:
    bool(type(unicode))
except NameError:
    unicode = str


class RNNModel:
    def __init__(self):
        self.config = TBRNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextBiRNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.dropout_keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', dest='model', default="RNN", type=str, required=True, choices=['RNN', 'BiRNN'],
                        help="模型")
    args = parser.parse_args()
    _model = args.model

    base_dir = '../data/cnews'
    vocab_dir = os.path.join(base_dir, 'cnews.vocab.txt')
    if _model == "RNN":
        save_dir = './checkpoints/textrnn'
    if _model == "BiRNN":
        save_dir = './checkpoints/textbirnn'
    save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径

    rnn_model = RNNModel()
    test_demo = ['三星ST550以全新的拍摄方式超越了以往任何一款数码相机',
                 '热火vs骑士前瞻：皇帝回乡二番战 东部次席唾手可得新浪体育讯北京时间3月30日7:00']
    for i in test_demo:
        print(rnn_model.predict(i))