"""
Parser to modify the sentence.

Feel free to modify and improve directly on this file.

"""

import nltk

#nltk.set_proxy('http://proxy.example.com:3128', ('USERNAME', 'PASSWORD')) #if you use a proxy
#nltk.download() # Remove when you have download the data (punkt and maxent_treebank_pos_tagger models).

stemmer = nltk.stem.porter.PorterStemmer();

def parse(sentence):
	sentence = sentence.replace('|','') # Remove conflicts with VW format
	sentence = sentence.replace(':','&') # Remove conflicts with VW format
	sentence = sentence.lower() # Convert all to lower-case
	
	tokens = nltk.word_tokenize(sentence) # Transform the sentence into a list of tokens
	pos = nltk.pos_tag(sentence)
	
	# Can use words from the list here
		
	new_tokens = []
	
	# Keep only stems
	for token in tokens:
		new_tokens.append(stemmer.stem(token) + '\\' + pos(token))
	
	# Re-build the sentence
	sentence = ''
	for w in new_tokens:
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
		sentence += w + ' '	
	sentence = sentence[:-1]
	
	# Stick tokens and pos-tags together
	pos = ''
	for t in tags:
		if t[1]!=':':
			pos += t[0] + '_' + t[1] + ' '
	pos = pos[:-1]

	return (sentence, pos)

def parse_simple(sentence):
	sentence = sentence.replace('|','') # Remove conflicts with VW format
	sentence = sentence.replace(':','&') # Remove conflicts with VW format
	sentence = sentence.lower() # Convert all to lower-case
	
	tokens = nltk.word_tokenize(sentence) # Transform the sentence into a list of tokens

	return tokens

