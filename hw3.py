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
        for word in word_tokenize(sent.lower()):
            fdist.inc(word)

    ret = list()
    ret.append(word for word in fdist.keys() if fdist.count(word) > 5)




