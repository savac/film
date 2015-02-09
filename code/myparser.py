"""
Parser to modify the sentence.

Feel free to modify and improve directly on this file.

"""

def parse(sentence):
	sentence.replace('|','') # Remove conflicts with VW format
	return sentence