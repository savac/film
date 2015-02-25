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


def add_w2v_synonyms(f_original='../data/train.txt', w2v_model_file='../data/w2v_model.txt', f_combined='../data/t_combined.txt'):
    f_in = open(f_original, "r")
    model = word2vec.Word2Vec.load_word2vec_format(w2v_model_file, binary=True)
    f_out = open(f_combined, 'wb')
    
    common100 = {1: 'the', 2: 'of', 3: 'and', 4: 'a', 5: 'to', 6: 'in', 7: 'is', 8: 'you', 9: 'that', 10: 'it', 
    11: 'he', 12: 'was', 13: 'for', 14: 'on', 15: 'are', 16: 'as', 17: 'with', 18: 'his', 19: 'they', 
    20: 'I', 21: 'at', 22: 'be', 23: 'this', 24: 'have', 25: 'from', 26: 'or', 27: 'one', 28: 'had', 29: 'by', 
    30: 'word', 31: 'but', 32: 'not', 33: 'what', 34: 'all', 35: 'were', 36: 'we', 37: 'when', 38: 'your', 39: 'can', 
    40: 'said', 41: 'there', 42: 'use', 43: 'an', 44: 'each', 45: 'which', 46: 'she', 47: 'do', 48: 'how', 49: 'their', 
    50: 'if', 51: 'will', 52: 'up', 53: 'other', 54: 'about', 55: 'out', 56: 'many', 57: 'then', 58: 'them', 59: 'these', 
    60: 'so', 61: 'some', 62: 'her', 63: 'would', 64: 'make', 65: 'like', 66: 'him', 67: 'into', 68: 'time', 69: 'has', 
    70: 'look', 71: 'two', 72: 'more', 73: 'write', 74: 'go', 75: 'see', 76: 'number', 78: 'way', 79: 'could', 
    80: 'people', 81: 'my', 82: 'than', 83: 'first', 84: 'water', 85: 'been', 86: 'call', 87: 'who', 88: 'oil', 89: 'its', 
    90: 'now', 91: 'find', 92: 'long', 93: 'down', 94: 'day', 95: 'did', 96: 'get', 97: 'come', 98: 'made', 99: 'may', 100: 'part', 101:'.'}
    common100 = common100.values()
    
    while True:
        row_old = f_in.readline()
        if row_old == "":
            break
        
        # get the phrase
        row = row_old.split("|phrase")
        row = row[1].split("|")
        row = row[0].split(" ")
        
        # do something dumb and average the vectors for the all the words in the phrase
        m = list()
        for w in row:
            try:
                if w not in common100:
                    m.append(str(model.most_similar(positive=[w])[0][0]))
            except KeyError:
                pass

        to_write = ' |synonyms ' + ' '.join(m)
        f_out.write(row_old.strip('\n') + to_write + '\n')

def add_w2v_classes(f_original='../data/train.txt', w2v_model_file='../data/w2v_model.txt', f_combined='../data/t_combined.txt'):
    f_in = open(f_original, "r")
    f_out = open(f_combined, 'wb')    

    d = {}
    with open(w2v_model_file) as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
    
    while True:
        row_old = f_in.readline()
        if row_old == "":
            break
        
        # get the phrase
        row = row_old.split("|phrase")
        row = row[1].split("|")
        row = row[0].split(" ")

        to_write = ' |classes'
        for w in row:
            try:
                to_write+= ' c' + d[w]
            except KeyError:
                pass
        
        f_out.write(row_old.strip('\n') + to_write + '\n')
