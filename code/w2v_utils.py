from gensim.models import word2vec

from film_utils import get_sentences_list


# NB: using the W2V via the gensim (a python wrapper) does not seem to give
# the same results as when using w2v directly. It seems that using the 
# w2v directly gives more sensible word similarities. So we need to check 
# parameters used by the gensim.

#==================================================
# Code to use w2v directly
#==================================================
# Compute vectors
#time /home/sc/work/word2vec/word2vec -train ../data/sentences.txt -output vectors.txt -cbow 1 -size 20 -window 6 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15 -min-count 5
#/home/sc/work/word2vec/distance vectors.txt

# Cluster
#time /home/sc/work/word2vec/word2vec -train ../data/sentences.txt -output classes.txt -cbow 1 -size 200 -window 5 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 0 -iter 15 -min-count 1 -classes 500
#sort classes.txt -k 2 -n > classes.sorted.txt
#==================================================


#==================================================
# Train using gensim
#==================================================
def train(train_file='../data/train.tsv', model_file='../data/w2v_model.txt'):
    
    sentences = get_sentences_list(train_file)

    #time /home/sc/work/word2vec/word2vec -train ../data/sentences.txt -output vectors.txt -cbow 1 -size 20 -window 6 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15 -min-count 5
    model = word2vec.Word2Vec(sentences, workers=20, \
                size=20, min_count = 5, \
                window = 6, sample = 1e-4, negative=25, \
                sg=0, cbow_mean=0, alpha=0.05) # sg=0 to use CBOW, cont. bag of words

    # If you don't plan to train the model any further, calling 
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)

    # It can be helpful to create a meaningful model name and 
    # save the model for later use. You can load it later using Word2Vec.load()
    #model.save(model_name)
    model.save_word2vec_format(model_file, binary=False)


    #print model.most_similar("terrible")
    #print model.most_similar("funny")

    # Get the vector simply by calling; outpus is numpy float array
    # model['word']

    # Load the model later
    # model = Word2Vec.load_word2vec_format('/tmp/vectors.txt', binary=False)  # C text format
