# lda script
import logging
import os
import gensim
import random
import argparse
from gensim import corpora, models, similarities
from code_walker import CodeWalker

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO 

PATH = os.path.dirname(os.path.realpath(__file__))


class Corpus(object):

    def __init__(self, iterator, no_below=15, no_above=0.3):
        self.iterator = iterator
        self.dictionary = gensim.corpora.Dictionary(self.iterator)
        self.dictionary.filter_extremes(no_below=no_below, no_above=no_above)

    def __iter__(self):
        for tokens in self.iterator:
            yield self.dictionary.doc2bow(tokens)


def create_corpus():
    corpus = Corpus(CodeWalker())
    corpora.MmCorpus.serialize(PATH + '/../scrapers/data/test_corpus.mm', corpus)
    corpus.dictionary.save_as_text(PATH + '/../scrapers/data/test_dictionary.txt')
    

def train_model(ntopics):
    mm = corpora.MmCorpus(PATH + '/../scrapers/data/test_corpus.mm')
    id2word = gensim.corpora.Dictionary.load_from_text(PATH + '/../scrapers/data/test_dictionary.txt')

    lda = gensim.models.ldamodel.LdaModel(corpus=mm, num_topics=ntopics, id2word=id2word, update_every=1, chunksize=10000, passes=1)

    for topic in lda.show_topics(ntopics):
        print 
        print topic

    save_model(lda)


def save_model(model):
    print "saving model."
    model.save(PATH + '/../scrapers/data/saved_lda_model.model')


if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Run LDA over code.')
    parser.add_argument('--ntopics', type=int)
    parser.add_argument('--createdict', default=False) 

    args = parser.parse_args()

    if args.createdict != False:
        create_corpus()
    train_model(args.ntopics)


