# -*- coding: utf-8 -*-
"""
Try a naive Bayes classifier using NLTK

Based on the tutorial at this address:
http://www.nltk.org/book/ch06.html

"""

import nltk
from myparser import parse, to_sentence
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
from scipy.sparse import csr_matrix, hstack
from sklearn.ensemble import RandomForestClassifier

def load_file(file):
	f = open(file, 'r')
	f.readline() # skip header
	documents = [];
	for line in f:
		field = line.split('\t')
		documents.append((parse(field[2]), int(field[3])))
	return documents
	
def get_top_n_words(documents, n):
	words = []
	for entry in documents:
		words += entry[0]
	all_words = nltk.FreqDist(words).most_common(n) # Frequency of each word (sorted)
	return [word_count[0] for word_count in all_words]
	
def documents_features(documents, vocabulary=None): # documents must be a list of strings
	vectoriser = TfidfVectorizer(sublinear_tf=True, vocabulary=vocabulary)
	return vectoriser.fit_transform(documents)

	
# Own features
def has_capitalised_token(tokens):
	for token in tokens:
		if token.isupper():
			return True
	return False
		
def pos_features(documents):
	pos_documents = []
	for document in documents:
		pos_documents.append(to_sentence([token_pos[1] for token_pos in nltk.pos_tag(document[0])]))
	vectoriser = TfidfVectorizer()
	return vectoriser.fit_transform(pos_documents)

if __name__ == '__main__':
	print('Loading file...')
	documents = load_file('../../data/train.tsv')
	random.shuffle(documents)
	#DEBUG: Subsample
	#documents = documents[:300]
	validation_size = int(len(documents) / 3)
	
	word_features = get_top_n_words(documents, 2000) # features restricted to 500
	
	print('Creating word features...')
	features_word = documents_features([to_sentence(document[0]) for document in documents])	
	print('Creating POS features...')
	features_pos = pos_features(documents)
	
	labels = [int(document[1]) for document in documents]
	print('Training...')
	featureset = hstack([features_word, features_pos], format='csr')
	#featureset = features_word
	
	train_set, test_set = featureset[validation_size:], featureset[:validation_size]
	train_labels, test_labels = labels[validation_size:], labels[:validation_size]

	
	nbc = MultinomialNB(0) # No smoothing (better perf)
	nbc.fit(train_set, train_labels)
	predictions_nbc = nbc.predict(test_set)
	print('Naïve Bayes classifier')
	print('Accuracy:', accuracy_score(predictions_nbc, test_labels))
	print(confusion_matrix(predictions_nbc, test_labels))
	
	
#	rfc = RandomForestClassifier(n_jobs=-1)
#	rfc.fit(train_set, train_labels)
#	predictions_rfc = rfc.predict(test_set)
#	print('Random forest classifier')
#	print('Accuracy:', accuracy_score(predictions_rfc, test_labels))
#	print(confusion_matrix(predictions_rfc, test_labels))
	
	