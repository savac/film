"""
Parser to modify the sentence.

Feel free to modify and improve directly on this file.

"""

def parse(sentence):
	sentence = sentence.replace('|','') # Remove conflicts with VW format
	sentence = sentence.replace(':','&') # Remove conflicts with VW format
	sentence = sentence.lower() # Convert all to lower-case
	return sentence
