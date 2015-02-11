"""
Parser to modify the sentence.

Feel free to modify and improve directly on this file.

"""

import nltk

#nltk.set_proxy('http://proxy.example.com:3128', ('USERNAME', 'PASSWORD')) #if you use a proxy
#nltk.download() # Remove when you have download the data (punkt model and stopwords corpus).

stop_words = []

def parse(sentence):
	sentence = sentence.replace('|','') # Remove conflicts with VW format
	sentence = sentence.replace(':','&') # Remove conflicts with VW format
	sentence = sentence.lower() # Convert all to lower-case
	
	tokens = nltk.word_tokenize(sentence) # Transform the sentence into a list of tokens
	
	# Can use words from the list here
		
	# Re-build the sentence
	sentence = ''
	for w in tokens:
		if not w in stop_words:
			sentence += w + ' '	
	sentence = sentence[:-1]
	return sentence


def parse_and_tag(sentence):
	sentence = sentence.replace('|','') # Remove conflicts with VW format
	sentence = sentence.replace(':','&') # Remove conflicts with VW format
	sentence = sentence.lower() # Convert all to lower-case
	
	tokens = nltk.word_tokenize(sentence) # Transform the sentence into a list of tokens
	tags = nltk.pos_tag(tokens) # [('I', 'PRP'), ('have', 'VBP'), ('a', 'DT'), ('dream', 'NN'), ('.', '.')]
	
	# Can use words from the list here
		
	# Re-build the sentence
	sentence = ''
	for w in tokens:
		if not w in stop_words:
			sentence += w + ' '	
	sentence = sentence[:-1]
	
	# Stick tokens and pos-tags together
	pos = ''
	for t in tags:
		pos += t[0] + '_' + t[1] + ' '
	pos = pos[:-1]

	return (sentence, pos)
