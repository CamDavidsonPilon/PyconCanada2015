# lda script
import logging
import re
import os
import gensim
import keyword
import random
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO 


PATH = os.path.dirname(os.path.realpath(__file__))
CAMELCASE_TO_UNDERSCORE_RE = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

class CodeWalker(object):
    
    folders = PATH + '/../scrapers/data'

    python_keywords = map(lambda s: s.lower(), keyword.kwlist)

    python_types = ['true', 'false', 'none']

    python_builtin_functions = ['abs', 'divmod', 'input', 'open', 'staticmethod', 'all', 'enumerate', 'int', 'ord', 'str', 
                                'any', 'eval', 'isinstance', 'pow', 'sum', 'basestring', 'execfile', 'issubclass', 'print', 
                                'super', 'bin', 'file', 'iter', 'property', 'tuple', 'bool', 'filter', 'len', 'range', 'type', 
                                'bytearray', 'float', 'list', 'raw_input', 'unichr', 'callable', 'format', 'locals', 'reduce', 
                                'unicode', 'chr', 'frozenset', 'long', 'reload', 'vars', 'classmethod', 'getattr', 'map', 
                                'repr', 'xrange', 'cmp', 'globals', 'max', 'reversed', 'zip', 'compile', 'hasattr', 'memoryview', 
                                'round', '__import__', 'complex', 'hash', 'min', 'set', 'delattr', 'help', 'next', 'setattr', 
                                'dict', 'hex', 'object', 'slice', 'dir', 'id', 'oct', 'sorted']

    common_words = ['self', 'the', 'name', 'to', 'of', 'get', 'path', 'bhadron', 'mdst', 'data', 
                    'error', 'value', 'this', 'text', 'key', 'cb', 'lh', 'lhcb', 'lfn', 
                    'args', 'be', 'field', 'user',  'add', 'string', 
                    'node', 'it', 'info', 'default', 'line', 'append', 'by', 'start', 'message',
                    'init', 'that', 'code', '0000', 'model', 'index', 'size', 'each', 'on', 'an', 
                    'obj', 'result', 'base', 'end', 'join', 'output', 'ref', 'param', 'number', 'new', 
                    'server', 'content', 'xsc', 'time', 'feature', 'no', 'equal', 'use', 'create', 
                    'out', 'exception', 'kwargs', 'you', 'item', 'parser', 
                    'method', 'tree', 'project', 'are', 'token', 'parameters', 'group', 'count', 'attr',
                    'test', 'os', 'url', 'request', 'version', 'license', 'response', 'config', 'html', 'http', 'options', 
                    'log', 'sys', 'db', 'image', 'python', 'write', 'values', 'option', 'root',]

    stop_words =  set(python_keywords + python_builtin_functions + python_types + common_words)
    
    def __init__(self, subsample_rate=0.2):
        self.subsample_rate = subsample_rate

    def convert_camel_case_to_underscore(self, word):
        return CAMELCASE_TO_UNDERSCORE_RE.sub(r'_\1', word).lower()

    def clean_and_split_codewords(self, word):
        """
        HTTPResonse => http, response
        aNewWorld => a, new, world
        a_new_world => a, new, world

        """
        for subword in self.convert_camel_case_to_underscore(word).split('_'):
            if subword and len(subword) > 1 \
               and re.match('^u\w{4}$', subword) is None \
               and re.match('^x\w{2}$', subword) is None \
               and subword not in self.stop_words:
                yield subword
    

    def __iter__(self):
        for root, dirs, files in os.walk(self.folders):
            for file in files:
                if file.endswith('.py'):
                    if hash(file + root) % int(1./self.subsample_rate) != 0:
                        continue
                    try:
                        with open(os.path.join(root, file), 'r') as open_file:
                            lines = open_file.read()
                            results = []
                            for raw_word in re.findall('(\w+)', lines):
                                for clean_words in self.clean_and_split_codewords(raw_word):
                                    results.append(clean_words)
                            yield results
                    except IOError:
                        pass
                    

class Corpus(object):

    def __init__(self, iterator, no_below=5):
        self.iterator = iterator
        self.dictionary = gensim.corpora.Dictionary(self.iterator)
        self.dictionary.filter_extremes(no_below=10)

    def __iter__(self):
        for tokens in self.iterator:
            yield self.dictionary.doc2bow(tokens)


corpus = Corpus(CodeWalker())
corpora.MmCorpus.serialize(PATH + '/../scrapers/data/test_corpus.mm', corpus)
mm = corpora.MmCorpus(PATH + '/../scrapers/data/test_corpus.mm')
print mm

num_topics = 60
lda = gensim.models.ldamodel.LdaModel(corpus=mm, num_topics=num_topics, id2word=corpus.dictionary, update_every=1, chunksize=10000, passes=1)

for topic in lda.show_topics(num_topics):
    print 
    print topic