# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:39:06 2019
@Author: yichao.li
@Description:Load the polyphone dictionary.
"""

class dictionary(object):
	"""load the dictionary"""
	def __init__(self, file):
		super(dictionary, self).__init__()
		self.file = file
	def load(self):
		char = []
		with open(self.file,'r',encoding = 'utf-8') as fp:
			for line in fp.readlines():
				line = line.strip('\n')
				char.append(line)
		print("number of polyphones is {}".format(len(char)))
		dic = dict.fromkeys(char)
		return dic