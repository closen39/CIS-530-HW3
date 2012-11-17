# Jason Mow (jmow@seas.upenn.edu)
# Nate Close (closen@seas.upenn.edu)

from csv import DictReader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from BeautifulSoup import BeautifulSoup as Soup

def get_all_files(directory):
    files = PlaintextCorpusReader(directory, '.*')
    return files.fileids()

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
    for line in f:
        # split lines
        li = line.rstrip().split(' ')
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
    return mpqa_dict


def get_mpqa_features(text, mpqa_dict):
    neg = 0
    neutral = 0
    pos = 0
    for word in word_tokenize(text.lower()):
        tuples = mpqa_dict[word]
        for (x,y) in tuples:
            if y == "positive":
                pos += 1
            elif y == "neutral":
                neutral += 1
            elif y == "negative":
                neg += 1
            elif y == "both":
                pos += 1
                neg += 1
    return (pos, neg, neutral)

def get_mpqa_features_wordtype(text, mpqa_dict):
    weak_neg = 0
    weak_neutral = 0
    weak_pos = 0
    strong_neg = 0
    strong_neutral = 0
    strong_pos = 0
    for word in word_tokenize(text.lower()):
        tuples = mpqa_dict[word]
        for (x,y) in tuples:
            if x == 'strongsubj':
                if y == "positive":
                    strong_pos += 1
                elif y == "neutral":
                    strong_neutral += 1
                elif y == "negative":
                    strong_neg += 1
                elif y == "both":
                    strong_neg += 1
                    strong_pos += 1
            elif x == 'weaksubj':
                if y == "positive":
                    weak_pos += 1
                elif y == "neutral":
                    weak_neutral += 1
                elif y == "negative":
                    weak_neg += 1
                elif y == "both":
                    weak_neg += 1
                    weak_pos += 1
    return (strong_pos, strong_neg, strong_neutral, weak_pos, weak_neg, weak_neutral)

def get_geninq_lexicon(lexicon_path):
    geninq_dict = dict()
    f = open(lexicon_path)
    for line in f:
        pos, neg, strong, weak = 0, 0, 0, 0
        x = word_tokenize(line)
        word = x[0]
        if 'Pstv' in x:
            pos = 1
        if 'Ngtv' in x:
            neg = 1
        if 'Strng' in x:
            strong = 1
        if 'Weak' in x:
            weak = 1
        geninq_dict[word] = [pos, neg, strong, weak]
    return geninq_dict

def get_geninq_features(text, geninq_dict):
    pos = 0
    neg = 0
    for word in word_tokenize(text.lower()):
        data = geninq_dict[word]
        if data[0] == 1:
            pos += 1
        if data[1] == 1:
            neg += 1
    return (pos, neg)

def get_geninq_features_strength(text, geninq_dict):
    strong_pos = 0
    strong_neg = 0
    weak_pos = 0
    weak_neg = 0  
    for word in word_tokenize(text.lower()):
        data = geninq_dict[word]
        if data[0] == 1:
            if data[2] == 1:
                strong_pos += 1
            if data[3] == 1:
                weak_pos += 1
        if data[1] == 1:
            if data[2] == 1:
                strong_neg += 1
            if data[3] == 1:
                weak_neg += 1
    return (strong_pos, strong_neg, weak_pos, weak_neg)

# section 3.3
def extract_named_entities(xml_files_path):
    ret = list()
    files = [xml_files_path + '/' + str(x) for x in get_all_files(xml_files_path)]

    for file1 in files:
        handler = open(file1).read()
        doc = Soup(handler)
        ners = [x.string for x in doc.findAll("ner")]
        #print ners
        orgs, persons, locs = 0, 0, 0
        for ner in ners:
            if ner == 'LOCATION':
                locs += 1
            elif ner == 'ORGANIZATION':
                orgs += 1
            elif ner == 'PERSON':
                persons += 1
        ret.append([orgs, persons, locs])
    return ret

def extract_adjectives(xml_files_path):
    counts = FreqDist()
    files = [xml_files_path + '/' + str(x) for x in get_all_files(xml_files_path)]

    for file1 in files:
        handler = open(file1).read()
        doc = Soup(handler)
        adjs= [x.parent.word.string for x in doc.findAll("pos") if x.string == "JJ"]
        print adjs
        for adj in adjs:
            counts.inc(adj.lower())

    ret = list()
    for word in counts.keys():
        if counts[word] > 5:
            ret.append(word)
    
    return ret

def map_adjectives(filename, adj_list):
    ret = [0] * len(adj_list)
    f = open(filename)
    text = f.read().rstrip()
    for idx, adj in enumerate(adj_list):
        if adj in text:
            ret[idx] = 1
    return ret

def main():
    pass

if  __name__ =='__main__':
    main()
