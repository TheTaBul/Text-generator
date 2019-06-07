#!/usr/bin/python3

import collections
import random
import sys

class TextGenerator:
	def __init__(self):
		self.possible_next_words = dict()
	def source(self, source_file):
		with open(source_file, 'r') as f:
			for line in f:
				words = [str.lower() for str in line.split()]
				for i in range(len(words)):
					words[i] = ''.join(
							[s for s in words[i] if s.isalpha() or s in '\'-'])
				for i in range(len(words)-1):
					word, next_word = words[i], words[i+1]
					try:
						self.possible_next_words[word][next_word] += 1
					except KeyError:
						self.possible_next_words[word] =\
								collections.Counter({next_word: 1})
	def generate(self, output_file, number_of_words):
		words = list(self.possible_next_words.keys())
		word = random.choice(words)
		column_width = 0
		with open(output_file, 'w+') as f:
			for _ in range(number_of_words):
				if column_width + len(word) >= 80:
					column_width = f.write('\n' + word + ' ')
				else:
					column_width += f.write(word + ' ')
				try:
					word = random.choice(
							list(self.possible_next_words[word].elements()))
				except KeyError:
					word = random.choice(words)
			f.write('\n')


t = TextGenerator()
argc = len(sys.argv)
if argc < 3 :
	wrong_usage =\
		'Usage: ./textgen.py '\
		+ '<SOURCE_FILE> <OUTPUT_FILE> <number of words to generate>\n'\
		+ 'If no <OUTPUT_FILE> is specified it will be created.'
	print(wrong_usage)
elif argc == 3:
	try:
		t.source(sys.argv[1])
		t.generate('generated.txt', int(sys.argv[2]))
	except FileNotFoundError:
		file_not_found = 'File ' + sys.argv[1] + ' not found.'
		print(file_not_found)
elif argc == 4:
	try:
		t.source(sys.argv[1])
	except FileNotFoundError:
		file_not_found = 'File ' + sys.argv[1] + ' not found.'
		print(file_not_found)
	try:
		t.generate(sys.argv[2], int(sys.argv[3]))
	except FileNotFoundError:
		file_not_found = 'File ' + sys.argv[2] + ' not found.'
		print(file_not_found)
else:
	unknown_options = 'Unknown options: ' + ' '.join(sys.argv[3:])
	print(unknown_options)
