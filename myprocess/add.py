# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:39:06 2019
@Author: yichao.li
@Description:
	1.Format the new corpus and save it into csv file
	2.add the new polyphones into the polyphone dictionary
@Sample:
	正在为{wei4}各国经济的发展提供历史机遇。
	--->>>
	正在为{wei4}各国经济的发展提供历史机遇。=NA NA wei4 NA NA NA NA NA NA NA NA NA NA NA NA
"""
import sys
sys.path.append("..")
import csv
import pandas as pd
import DataProcessing.configure as config
from commonfun import *
from dictionary import *

# Load data
data = []
with open(config.adddata,'r') as fp:
	for line in fp.readlines():
		line = line.strip('\n')
		data.append(line)


# Deduplicate data
data = deduplicate(data)

#Load the polyphones dictionary
loading = dictionary(config.polyphone)
dic = loading.load()

# Format the new corpus
# And
# Find the new polyphones
dex = []
pinyin = []
newpolychar = set()

for i in range(len(data)):
	x = data[i]
	ind = []
	pin = []
	s = ''
	index = 0
	while(index < len(x)):
		if(x[index] == '{'):
			left = index
			ind.append(left-1)

			temp = x[left - 1]
			if(not dic.__contains__(temp)):
				newpolychar.add(temp)
			while(True):
				if(x[index] == '}'):
					break
				index += 1
			right = index
			pin.append(x[left+1:right])
			index += 1
		else:
			s += x[index]
		index += 1
	data[i] = s
	dex.append(ind)
	pinyin.append(pin)

print(data[:3])
print(dex[:3])
print(pinyin[:3])

pinxvlie = []
for i in range(len(data)):
	text = data[i]
	loca = dex[i]
	pin = pinyin[i]

	textindex = 0		#文本字符指针
	locaindex = 0		#多音字位置指针
	pinindex = 0		#拼音位置指针

	textsum = len(text)	#字符数目
	pinsum = len(pin)	#多音字数目

	s = ''

	while(textindex < textsum):
		if(is_chinese(text[textindex])):
			if(locaindex < pinsum):
				if(textindex == int(loca[locaindex])):
					s += ' ' + pin[pinindex]
					textindex += 1
					locaindex += 1
					pinindex += 1
				else:
					s += ' ' + 'NA'
					textindex += 1
			else:
				s += ' ' + 'NA'
				textindex += 1
		else:
			textindex += 1
	s = s.strip()
	pinxvlie.append(s)
print(pinxvlie[:3])


# Fix
'''
@Time : 2019-06-25
@Description : Fix dictionary, some hanzi with ‘{}’ label is not real polyphone.
'''
for i in range(len(data)):
	text = data[i]
	label = pinxvlie[i].split(' ')

	indexchar = 0
	indexpinyin = 0
	while(indexchar < len(text)):
		if(is_chinese(text[indexchar])):
			if(not dic.__contains__(text[indexchar])):
				label[indexpinyin] = 'NA'

			indexchar += 1
			indexpinyin += 1
		else:
			indexchar += 1

	pinxvlie[i] = ' '.join(label)

# Save it into csv file
newdata = []
for i in range(len(data)):
	newdata.append(data[i]+'='+pinxvlie[i])

newye = pd.DataFrame({'cor': newdata})
newye.to_csv(config.addcsv, sep=',', index=False)


# # add the new polyphones into the polyphone dictionary
# newpolychar = list(newpolychar)
# with open(config.polyphone,'a',encoding = 'utf-8') as fp:
# 	for x in newpolychar:
# 		fp.write('\n')
# 		fp.write(str(x))