# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:39:06 2019
@Author: yichao.li
@Description:
	1.Cancel continuous reading for metadata_txt_pinyin.csv
	2.Save them into csv file
@Sample:
	揶揄得孙垚差点背过气儿。=ye2 yu2 de5 sun1 yao2 cha4 dian3 bei4 guo4 qir4
	--->>>
	揶揄得孙垚差点背过气儿。=ye2 yu2 de5 sun1 yao2 cha4 dian3 bei4 guo4 qi4 er2
"""

import sys
sys.path.append("..")
import csv
import pandas as pd
import DataProcessing.configure as config
from commonfun import *

# Load data
text = []
pinyin = []
with open(config.origindata, 'r',encoding = 'utf-8') as fp:
	reader = csv.reader(fp)
	for item in reader:
		line = ''.join(item)
		line = line.split("=")
		text.append(line[0])
		pinyin.append(line[1])
print(text[:3])
print(pinyin[:3])

newpi = []

for i in range(len(text)):
	te = text[i]
	pi = pinyin[i].split(' ')

	index1 = 0
	index2 = 0

	pin = ''

	while(index1 < len(te)):
		if(is_chinese(te[index1])):
			if(te[index1 + 1] == '儿'):
				if(index2 + 1 < len(pi)):
					if(pi[index2+1] != 'er2'):
						temp = pi[index2]
						temp = temp[:-2] + temp[-1]
						pin += ' ' + temp
						pin += ' ' + 'er2'
						index1 += 2
						index2 += 1
					else:
						pin += ' ' + pi[index2]
						index1 += 1
						index2 += 1
				else:
					temp = pi[index2]
					temp = temp[:-2] + temp[-1]
					pin += ' ' + temp
					pin += ' ' + 'er2'
					index1 += 2
					index2 += 1
			else:
				pin += ' ' + pi[index2]
				index1 += 1
				index2 += 1
		else:
			index1 += 1

	pin = pin.strip( )
	newpi.append(pin)	

newdata = []
for i in range(len(text)):
	x = text[i]
	y = newpi[i]
	s = x + '=' + y
	newdata.append(s)

newye = pd.DataFrame({'cor': newdata})
newye.to_csv(config.offcontidata, sep=',', index=False)
