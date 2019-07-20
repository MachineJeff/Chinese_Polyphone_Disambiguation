# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:25:47 2019
@Author: yichao.li
@Description:Use model to label polyphone
"""
import sys
sys.path.append("..")
import torch
from torch import nn
from DataProcessing.preprocessing import BatchIterator
from DataProcessing import configure


class DisambiguationLSTM(nn.Module):
    def __init__(self, n_word, word_dim, word_hidden, n_pronounce):
        super(DisambiguationLSTM, self).__init__()
        self.word_embedding = nn.Embedding(n_word, word_dim)
        self.lstm = nn.LSTM(
            input_size=word_dim,
            hidden_size=word_hidden,
            num_layers=configure.num_layer,
            batch_first=True,
            bidirectional=True
        )
        self.linear1 = nn.Linear(word_hidden*2, n_pronounce)

    def forward(self, x):
        x = self.word_embedding(x)
        x, _ = self.lstm(x)     # x.size():  (1,5,256)
        x = x.squeeze(0)        # 降一维
        x = self.linear1(x)     # 此时全连接层的输入是神经网络最后一层所有time step的输出
        return x

batch_iter = BatchIterator(configure.trn_file, configure.val_file, configure.tst_file, batch_size=configure.batch_size)
train_data, valid_data, test_data = batch_iter.create_dataset()
# train_iter, valid_iter, test_iter = batch_iter.get_iterator(train=train_data, valid=valid_data, test=test_data)


#需要重新加载四种数据，text.vocab label.vocab 以及他们的长度

s = 'v 了_ul <tail>'
model_path = 'param.pkl'


vocab = batch_iter.TEXT.vocab.stoi
locab = batch_iter.LABEL.vocab.itos

idx = []
for char in s.split():
	if(vocab.__contains__(char)):
		idx.append(vocab[char])
	else:
		idx.append(vocab['unk'])
idx = [idx]
idx = torch.LongTensor(idx)
print(idx)

model = DisambiguationLSTM(len(batch_iter.TEXT.vocab), 300, 300, len(batch_iter.LABEL.vocab))
model.load_state_dict(torch.load(model_path))
model.eval()
output = model(idx)
pre_y = torch.argmax(output,1)
pre_y = pre_y.unsqueeze(0)

pin = ''
for x in pre_y[0]:
	pin += ' ' + locab[x]

pin = pin.strip()
print(pin)


print(vocab)
print(type(vocab))
print()
# print(locab)
# print(type(locab))


# vocabfile = 'vocab.txt'
# with open(vocabfile, 'w', encoding = 'utf-8') as fp:
#     for i, x in enumerate(vocab):
#         fp.write(str(x))
#         fp.write("\n")

# locabfile = 'locab.txt'
# with open(locabfile, 'w', encoding = 'utf-8') as fp:
#     for x in locab:
#         fp.write(str(x))
#         fp.write("\n")

# print(len(vocab))
# print(len(batch_iter.TEXT.vocab))
# print()

# print(len(locab))
# print(len(batch_iter.LABEL.vocab))
