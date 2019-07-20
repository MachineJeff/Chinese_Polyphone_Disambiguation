# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:39:06 2019
@Author: yichao.li
@Description:POS token
"""
import sys
sys.path.append("..")
import csv
import jieba.posseg as pseg
import pandas as pd
import DataProcessing.configure as config
from commonfun import *
from dictionary import *

# Load data
file1 = config.offcontidata
file2 = config.addcsv

text = []
pinyin = []
with open(file1, 'r',encoding = 'utf-8') as fp:
	reader = csv.reader(fp)
	next(reader)
	for item in reader:
		line = ''.join(item)
		line = line.split("=")
		text.append(line[0])
		pinyin.append(line[1])

with open(file2, 'r',encoding = 'utf-8') as fp:
	reader = csv.reader(fp)
	next(reader)
	for item in reader:
		line = ''.join(item)
		line = line.split("=")
		text.append(line[0])
		pinyin.append(line[1])

print("text's length is {}".format(len(text)))
print("pinyin's length is {}".format(len(pinyin)))
print()


#Load the polyphones dictionary
loading = dictionary(config.polyphone)
dic = loading.load()


# Only save the chinese char and Chinese/English punctuation
for i in range(len(text)):
	x = text[i]
	text[i] = string_filter(x)


# Test if every char has pinyin
print("测试是否每个汉字都有对应的注音...")
tt = 0
for i in range(len(text)):
	x = text[i]
	y = pinyin[i]

	sum1 = 0
	for char in x:
		if(is_chinese(char)):
			sum1 += 1

	pro = y.split(' ')
	sum2 = len(pro)

	if(sum1 != sum2):
		tt = 1
		print("wrong location: {}".format(i))
		print(text[i])
if(tt == 0):
	print("No Problem!")


# Make pos tag
series = []
pinyinxvlie = []
lengword = []

for i in range(len(text)):
	
	words = pseg.cut(text[i])
	pronun = pinyin[i].split(' ')			##此时pronun是一个拼音列表，列表内元素为单个字符的拼音
	
	lengthPinyin = len(pronun)
	
	index = 0								##index指向拼音序列
	token = []
	label = []
	leng = []

	for item in words:
		if(item.flag != "x"):				##不要标点符号的影响
			lengthSeg = len(item.word)		##这个词的字符数目
			##标记该词是否有多音字
			tagMul = 0
			for j in range(lengthSeg):
				if (dic.__contains__(item.word[j])):
					tagMul = 1
					break
			number = 0

			##没有多音字就要将pos作为token，NA作为发音，且只算一个字符长度
			if(tagMul == 0):
				token.append(item.flag)
				label.append("NA")
				number += 1
				index += lengthSeg

			##有多音字要将"字_pos"作为token，非多音字用NA，多音字用原音
			else:
				for k in range(lengthSeg):
					temp = item.word[k] + '_' + item.flag
					token.append(temp)
					if(dic.__contains__(item.word[k])):
						try:
							label.append(pronun[index])
						except:
							print(i)
					else:
						label.append("NA")
					index += 1
					number += 1
			leng.append(number)
			#hanzi = ' '.join(token)
	lengb = []
	ss = 0
	for x in leng:
		ss += x
		lengb.append(ss)

	series.append(token)
	pinyinxvlie.append(label)
	lengword.append(lengb)

print(series[3])
print(pinyinxvlie[3])
print(lengword[3])

print("length of series is {}".format(len(series)))
print("length of pinyinxvlie is {}".format(len(pinyinxvlie)))


#测试代码,查看文本和拼音是不是都一样长了
print("测试是否文本和拼音是一样长了...")
tt = 0
for i in range(len(series)):
	l = len(series[i])
	r = len(pinyinxvlie[i])
	if(l != r):
		print("Forbidden!")
		tt = 1
		break
if(tt == 0):
	print("No Problem!")


#测试代码，查看lengword记录的是否有误
print("测试lengword记录的是否有误...")
tt = 0
for i in range(len(series)):
	
	l = len(lengword[i])
	r = lengword[i][l-1]

	t = len(series[i])

	if(t != r):
		print("Forbidden!")	
		tt = 1
		break
if(tt == 0):
	print("No Problem!")


# Add the <head> and <tail>
for i in range(len(series)):
	x = series[i]
	y = pinyinxvlie[i]

	x.insert(0,'<head>')
	y.insert(0,'NA')

	x.append('<tail>')
	y.append('NA')
	
	z = lengword[i]
	for n in range(len(z)):
		z[n] += 1
	temp = z[len(z)-1] + 1

	z.append(temp)
	z.insert(0,1)

print(series[3])
print(pinyinxvlie[3])
print(lengword[3])


# Make the Triad
finaltext = []
finalphone = []
for i in range(len(series)):
	##分别取出文本，发音，和数目对照表
	text = series[i]
	phone = pinyinxvlie[i]
	numb = lengword[i]

	gr = len(numb)						##词的数目

	##newnumb是为了方便后续处理
	newnumb = []
	newnumb.append(0)
	for i in range(gr-1):
		newnumb.append(numb[i])
	
	indexword = 0					##指向词的指针
	index = 0						##指向单个字符的指针

	while(index < len(text)):
		##当字符不是多音字时，字符指针加1，判断是否跳到下一个词了，必须要保证字符指针位置在词的指针包含当中
		if(phone[index] == 'NA'):
			index += 1
			if(index >= numb[indexword]):
				indexword += 1
		else:
			left = newnumb[indexword] - 1
			right = numb[indexword]

			leftstring = text[left]
			rightstring = text[right]

			leftchar = ''
			if(has_underline(leftstring)):
				leftchar = leftstring[2:]
			else:
				leftchar = leftstring
			rightchar = ''
			if(has_underline(rightstring)):
				rightchar = rightstring[2:]
			else:
				rightchar = rightstring

			subtext = text[left + 1:right]
			subtext.insert(0,leftchar)
			subtext.append(rightchar)
			
			subphone = phone[left + 1:right]
			subphone.insert(0,'NA')
			subphone.append('NA')

			finaltext.append(subtext)
			finalphone.append(subphone)

			index += 1
			if(index >= numb[indexword]):
				indexword += 1
				
print("length of finaltext is {}".format(len(finaltext)))
print("length of finalphone is {}".format(len(finalphone)))
print(finaltext[3])
print(finalphone[3])


finaltext2 = []
for i in range(len(finaltext)):
	hanzi = ' '.join(finaltext[i])
	finaltext2.append(hanzi)


#打乱顺序随机保存训练验证测试数据
(trdatatext, trdatalabel, vadatatext, vadatalabel, tedatatext, tedatalabel) = splitdata(finaltext2, finalphone, config.trn_rate, config.val_rate)


columns = ["text","label"]

traindata = pd.DataFrame({'label': trdatalabel,'text': trdatatext})
validdata = pd.DataFrame({'label': vadatalabel,'text': vadatatext})
testdata = pd.DataFrame({'label': tedatalabel,'text': tedatatext})

traindata.to_csv(config.trn_file, sep=',', index=False,columns=columns)
validdata.to_csv(config.val_file, sep=',', index=False,columns=columns)
testdata.to_csv(config.tst_file, sep=',', index=False,columns=columns)
