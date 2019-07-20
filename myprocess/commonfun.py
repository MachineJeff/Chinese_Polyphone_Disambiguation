# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:39:06 2019
@Author: yichao.li
@Description:Some commonly used customized functions
"""
import string
import random

# Test if a char is Chinese
def is_chinese(char):
	if(char >= '\u4e00' and char <= '\u9fa5'):
		return True
	else:
		return False


# Remove duplicate parts of a list
def deduplicate(list_object):
	data = list(set(list_object))
	return data


# Only save Chinese char and C/E punctuation for a string
def string_filter(string_object):
	punc = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
	punc += string.punctuation
	
	newstring = ''
	for i in range(len(string_object)):
		if( (not is_chinese(string_object[i])) and (not string_object[i] in punc) ):
			pass
		else:
			newstring += string_object[i]
	return newstring


# Split data randomly into train/valid/test
def splitdata(text, label, trainrate, validrate):
	length = len(text)

	nu = 0
	trdatatext = []
	trdatalabel = []
	while(nu < int(length * trainrate)):
		i = random.randint(0, len(text)-1)
		trdatatext.append(text[i])
		trdatalabel.append(label[i])
		del text[i]
		del label[i]
		nu += 1

	nu = 0
	vadatatext = []
	vadatalabel = []
	while(nu < int(length * validrate)):
		i = random.randint(0, len(text)-1)
		vadatatext.append(text[i])
		vadatalabel.append(label[i])
		del text[i]
		del label[i]
		nu += 1

	tedatatext = text
	tedatalabel = label

	return (trdatatext, trdatalabel, vadatatext, vadatalabel, tedatatext, tedatalabel)


# Test if a string has underline
def has_underline(string_object):
	tag = False
	for x in string_object:
		if(x == '_'):
			tag = True
			break
	return tag
