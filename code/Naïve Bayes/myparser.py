"""
Parser to modify the sentence.

Feel free to modify and improve directly on this file.

"""

import nltk

#nltk.download('punkt')
#nltk.download('maxent_treebank_pos_tagger')

stemmer = nltk.stem.porter.PorterStemmer();

""" Parse a sentence
    return a list of tokens
"""				
def parse(sentence):
	#sentence = sentence.replace('|','') # Remove conflicts with VW format
	#sentence = sentence.replace(':','&') # Remove conflicts with VW format

	sentence = sentence.lower()
	tokens = nltk.word_tokenize(sentence) # Transform the sentence into a list of tokens
	#pos = nltk.pos_tag(sentence)
#	return tokens
	# Can use words from the list here
	new_tokens = []
	
	# Keep only stems
	for token in tokens:
		tmp = token if token.isupper() else token.lower()
#		tmp = token.lower()
		new_tokens.append(stemmer.stem(tmp)) #  + '\\' + pos(token))
	return new_tokens
	

def to_sentence(l):
	# Re-build the sentence
	sentence = ''
	for w in l:
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
