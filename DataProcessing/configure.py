# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:39:06 2019
@Author: yichao.li
@Description:Some configure parameter
"""

trn_rate = 0.7
val_rate = 0.15

trn_file = '../data/train.csv'
val_file = '../data/valid.csv'
tst_file = '../data/test.csv'

# Polyphone dictionary
polyphone = '../data/polychar.txt'

# Origin data
origindata = '../data/metadata_txt_pinyin.csv'
offcontidata = '../data/offcontidata.csv'

# Add data
adddata = '../data/addcorpus.txt'
addcsv = '../data/addcorpus.csv'

# Prediction
wrong = '../data/wrong.csv'
correct = '../data/correct.csv'

# BLSTM
batch_size = 64
epochs = 10
num_layer = 3

model_path = 'param.pkl'