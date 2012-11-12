# Jason Mow (jmow@seas.upenn.edu)
# Nate Close (closen@seas.upenn.edu)

from csv import DictReader
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# extracts the top words having more than 5 occurences
def extract_top_words(csv_file):
    reader = DictReader(open(csv_file))
    corpus = list()
    for item in reader:
        corpus.append(item['situation'])

    # get list of words
    fdist = FreqDist()
    for sent in corpus:
        if not sent is None:
            for word in word_tokenize(sent.lower()):
                fdist.inc(word)

    ret = list()
    for word in fdist.keys():
        if fdist[word] > 5:
            ret.append(word)
    return ret

# returns list of number of times each word appears in entry
def map_entry(entry, top_words):
    # initialize list of zeros
    ret = [0] * len(top_words)
    wordIndices = dict()
    for idx, w in enumerate(top_words):
        wordIndices[w] = idx
    for word in word_tokenize(entry.lower()):
        if word in top_words:
            ret[wordIndices[word]] += 1
    return ret

def get_mpqa_lexicon(lexicon_path):
    mpqa_dict = dict()
    f = open(lexicon_path)
    for line in f.readline():
        # split lines
        li = line.split(' ')
        word = ""
        ty = ""
        pol = ""
        for elt in li:
            x = elt.split('=')
            if x[0] == 'word1':
                word = x[1]
            elif x[0] == "type":
                ty = x[1]
            elif x[0] == "priorpolarity":
                pol = x[1]
        # adds a list even if only 1 tuple
        tup = (ty, pol)
        tupleList = list()
        if word in mpqa_dict.keys():
            tupleList = mpqa_dict[word]
            tupleList.append(tup)
        else:
            tupleList.append(tup)
            mpqa_dict[word] = tupleList
        

