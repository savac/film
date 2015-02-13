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
