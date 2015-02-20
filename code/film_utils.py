import numpy as np
import csv
from myparser import parse_simple
from gensim.models import word2vec

def compare_submissions(f_a, f_b):
    f1 = open(f_a, "r")
    f2 = open(f_b, 'r')
    f1.readline()
    f2.readline()
    a = np.zeros((5, 5))
    while True:
        f1_line = f1.readline()
        f2_line = f2.readline()
        if f2_line == "":
            break
        
        f1_line = f1_line.split(",")
        f2_line = f2_line.split(",")

        a[int(float(f1_line[1]))][int(float(f2_line[1]))]+=1
    np.set_printoptions(suppress=True)
    print a
    return a

def combine_features(f_a, f_b):
    f1 = open(f_a, "r")
    f2 = open(f_b, 'r')
    f3 = open('../data/t_combined.txt', 'wb')
    while True:
        f1_line = f1.readline()
        f2_line = f2.readline()
        if f2_line == "":
            break
        
        f2_line = f2_line.split("|tag")
        f2_line = f2_line[1].split("|count")
        f3.write(f1_line.rstrip() + ' |tag' + f2_line[0] + '\n')

def get_sentences(tsv_file):
    txt_file = '../data/sentences.txt'
    with open(tsv_file,'r') as tsvin, open(txt_file,'wb') as txtout:
        tsvin.readline() # Skip header
        tsvin = csv.reader(tsvin, delimiter='\t')
        
        sflag = 0
        for row in tsvin:
            s0 = int(row[1])
            if sflag != s0:
                sflag = s0
                txtout.write(row[2].lower() + '\n')

def get_sentences_list(tsv_file):
    res = []
    with open(tsv_file,'r') as tsvin:
        tsvin.readline()
        tsvin = csv.reader(tsvin, delimiter='\t')
        
        sflag = 0
        for row in tsvin:
            s0 = int(row[1])
            if sflag != s0:
                sflag = s0
                res.append(parse_simple(row[2].lower()))
    return res

def add_w2v_features(f_original='../data/train.txt', w2v_model_file='../data/w2v_model.txt', f_combined='../data/t_combined.txt'):
    f_in = open(f_original, "r")
    model = word2vec.Word2Vec.load_word2vec_format(w2v_model_file, binary=True)
    f_out = open(f_combined, 'wb')
    while True:
        row_old = f_in.readline()
        if row_old == "":
            break
        
        # get the phrase
        row = row_old.split("|phrase")
        row = row[1].split("|")
        row = row[0].split(" ")
        
        # do something dumb and average the vectors for the all the words in the phrase
        m = np.zeros(model.layer1_size)
        n = 0
        for w in row:
            try:
                n+=1
                m+=model[w]
            except KeyError:
                pass
        if n > 0:
            m = m/n

        to_write = ' |vec' 
        for k in range(0,model.layer1_size):
            to_write += ' v' + str(k) +':'
            to_write += str(m[k])
        
        f_out.write(row_old.strip('\n') + to_write + '\n')
