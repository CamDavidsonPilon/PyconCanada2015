# lda script
import logging
import os
import gensim
import random
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


corpus = Corpus(CodeWalker())
corpora.MmCorpus.serialize(PATH + '/../scrapers/data/test_corpus.mm', corpus)
mm = corpora.MmCorpus(PATH + '/../scrapers/data/test_corpus.mm')
print mm

num_topics = 80
lda = gensim.models.ldamodel.LdaModel(corpus=mm, num_topics=num_topics, id2word=corpus.dictionary, update_every=1, chunksize=10000, passes=1)

for topic in lda.show_topics(num_topics):
    print 
    print topic

