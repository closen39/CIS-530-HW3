# Jason Mow (jmow@seas.upenn.edu)
# Nate Close (closen@seas.upenn.edu)

"""
GENERAL COMMENTS:
We were unable to complete section 5.4 because the files we are supposed
to generate are too big to hold on our eniac disk space. As such, we cannot
submit a scores_adv.txt file with these results. Similarly, we were unable to 
generate the testing files which will be used to calculate the set
performance. We were able to scale the data for named_entities 
which is included in our submission. 
"""

from csv import DictReader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from BeautifulSoup import BeautifulSoup as Soup

def get_all_files(directory):
    files = PlaintextCorpusReader(directory, '.*')
    return files.fileids()

# extracts the top words having more than 5 occurences
def extract_top_words(directory):
    #reader = DictReader(open(csv_file))
    files = [directory + '/' + str(x) for x in get_all_files(directory)]
    corpus = list()
    for file1 in files:
        f1 = open(file1)
        corpus.append(f1.read().rstrip())

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
        try:
            tuples = mpqa_dict[word]
        except:
            tuples = list()
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
        try:
            tuples = mpqa_dict[word]
        except:
            tuples = list()
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
        try:
            data = geninq_dict[word]
        except:
            data = [0,0]
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
        try:
            data = geninq_dict[word]
        except:
            data = [0,0,0,0]
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
        adjs= [x.parent.word.string for x in doc.findAll("pos") if "JJ" in x.string]
        # print adjs
        for adj in adjs:
            counts.inc(adj.lower())

    ret = list()
    for word in counts.keys():
        if counts[word] > 5:
            ret.append(word)
    
    return ret

def map_adjectives(text, adj_list):
    ret = [0] * len(adj_list)
    for idx, adj in enumerate(adj_list):
        if adj in text:
            ret[idx] = 1
    return ret

def process_corpus(data_dir, features):
    out = open("svm_data" + str(features), "w")
    pmap = open (data_dir + '/price_mapping.out')
    tmap = open (data_dir + '/text_mapping.out')
    vec = list()
    if features == 1:
        vec = extract_top_words(data_dir + '/all_files')
        for priceline in pmap:
            textline = tmap.next().strip()
            price = priceline.split("\t")
            text = textline.split("\t")
            if price[0] == 0 or len(text) == 1:
                continue

            change = price[1].split(",")[1]
            if len(change) == 0:
                percentage = "0"
            elif change[0] == "-":
                percentage = "-1"
            else:
                percentage = "+1"

            features = map_entry(text[1], vec)
            outstring = percentage + " "
            for idx, feature in enumerate(features):
                outstring += str(idx+1) + ":" + str(feature) + " "

            out.write(outstring.rstrip() + "\n")
    elif features == 2:
        mpqa = get_mpqa_lexicon('/project/cis/nlp/data/corpora/mpqa-lexicon/subjclueslen1-HLTEMNLP05.tff')
        geninq = get_geninq_lexicon('/project/cis/nlp/data/corpora/inquirerTags.txt')
        i = 1
        for priceline in pmap:
            textline = tmap.next().strip()
            price = priceline.split("\t")
            text = textline.split("\t")
            if price[0] == 0 or len(text) == 1:
                continue

            change = price[1].split(",")[1]
            if len(change) == 0:
                percentage = "0"
            elif change[0] == "-":
                percentage = "-1"
            else:
                percentage = "+1"

            mpqa_feat = get_mpqa_features_wordtype(text[1], mpqa)
            geninq_feat = get_geninq_features_strength(text[1], geninq)
            outstring = percentage + " "
            for feat in mpqa_feat:
                outstring += str(i) + ":" + str(feat) + " "
                i += 1
            for feat in geninq_feat:
                outstring += str(i) + ":" + str(feat) + " "
                i += 1
            out.write(outstring.rstrip() + "\n")
    elif features == 3:
        vec = extract_named_entities('/home1/j/jmow/school/cis530/hw3/xmlTrainingOut')
        i = 0
        for priceline in pmap:
            textline = tmap.next().strip()
            price = priceline.split("\t")
            text = textline.split("\t")
            if price[0] == 0 or len(text) == 1:
                continue

            change = price[1].split(",")[1]
            if len(change) == 0:
                percentage = "0"
            elif change[0] == "-":
                percentage = "-1"
            else:
                percentage = "+1"

            outstring = percentage + " "
            for idx, feature in enumerate(vec[i]):
                outstring += str(idx+1) + ":" + str(feature) + " "

            out.write(outstring.rstrip() + "\n")
            i += 1
    elif features == 4:
        vec = extract_adjectives('/home1/j/jmow/school/cis530/hw3/xmlTrainingOut')
        for priceline in pmap:
            textline = tmap.next().strip()
            price = priceline.split("\t")
            text = textline.split("\t")
            if price[0] == 0 or len(text) == 1:
                continue

            change = price[1].split(",")[1]
            if len(change) == 0:
                percentage = "0"
            elif change[0] == "-":
                percentage = "-1"
            else:
                percentage = "+1"

            features = map_adjectives(text[1], vec)
            outstring = percentage + " "
            for idx, feature in enumerate(features):
                outstring += str(idx+1) + ":" + str(feature) + " "

            out.write(outstring.rstrip() + "\n")
    elif features == 5:
        top_words = extract_top_words(data_dir + '/all_files')
        mpqa = get_mpqa_lexicon('/project/cis/nlp/data/corpora/mpqa-lexicon/subjclueslen1-HLTEMNLP05.tff')
        geninq = get_geninq_lexicon('/project/cis/nlp/data/corpora/inquirerTags.txt')
        entities = extract_named_entities('/home1/j/jmow/school/cis530/hw3/xmlTrainingOut')
        entityCount = 0
        adjs = extract_adjectives('/home1/j/jmow/school/cis530/hw3/xmlTrainingOut')
        i = 1

        for priceline in pmap:
            textline = tmap.next().strip()
            price = priceline.split("\t")
            text = textline.split("\t")
            if price[0] == 0 or len(text) == 1:
                continue

            change = price[1].split(",")[1]
            if len(change) == 0:
                percentage = "0"
            elif change[0] == "-":
                percentage = "-1"
            else:
                percentage = "+1"

            outstring = percentage + " "

            lexical_feat = map_entry(text[1], vec)
            for feat in lexical_feat:
                outstring += str(i) + ":" + str(feat) + " "
                i += 1

            mpqa_feat = get_mpqa_features_wordtype(text[1], mpqa)
            geninq_feat = get_geninq_features_strength(text[1], geninq)
            for feat in mpqa_feat:
                outstring += str(i) + ":" + str(feat) + " "
                i += 1
            for feat in geninq_feat:
                outstring += str(i) + ":" + str(feat) + " "
                i += 1
            for feat in entities[entityCount]:
                outstring += str(i) + ":" + str(feat) + " "
                i += 1

            adj_feat = map_adjectives(text[1], adjs)
            for feat in adj_feat:
                outstring += str(i) + ":" + str(feat) + " "

            out.write(outstring.rstrip() + "\n")
            entityCount += 1

def main():
    # process_corpus('/home1/c/cis530/hw3/data/training', 1)
    process_corpus('/home1/c/cis530/hw3/data/training', 2)
    # process_corpus('/home1/c/cis530/hw3/data/training', 3)
    process_corpus('/home1/c/cis530/hw3/data/training', 4)
    process_corpus('/home1/c/cis530/hw3/data/training', 5)

if  __name__ =='__main__':
    main()
