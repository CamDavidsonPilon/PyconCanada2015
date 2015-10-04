# lda script
import logging
import re
import os
import gensim
import keyword
import random
from gensim import corpora, models, similarities

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO 


PATH = os.path.dirname(os.path.realpath(__file__))
CAMELCASE_TO_UNDERSCORE_RE = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
dictionary = corpora.dictionary.Dictionary()


class CodeWalker(object):
    
    folders = PATH + '/../scrapers/data'

    python_keywords = map(lambda s: s.lower(), keyword.kwlist)

    python_types = ['int', 'float', 'long', 'complex', 'true', 'false', 'str', 
                     'unicode', 'list', 'tuple', 'bytearray', 'buffer', 'xrange',
                     'set', 'frozenset', 'dict']

    python_builtin_functions = ['abs', 'divmod', 'input', 'open', 'staticmethod', 'all', 'enumerate', 'int', 'ord', 'str', 
                                'any', 'eval', 'isinstance', 'pow', 'sum', 'basestring', 'execfile', 'issubclass', 'print', 
                                'super', 'bin', 'file', 'iter', 'property', 'tuple', 'bool', 'filter', 'len', 'range', 'type', 
                                'bytearray', 'float', 'list', 'raw_input', 'unichr', 'callable', 'format', 'locals', 'reduce', 
                                'unicode', 'chr', 'frozenset', 'long', 'reload', 'vars', 'classmethod', 'getattr', 'map', 
                                'repr', 'xrange', 'cmp', 'globals', 'max', 'reversed', 'zip', 'compile', 'hasattr', 'memoryview', 
                                'round', '__import__', 'complex', 'hash', 'min', 'set', 'delattr', 'help', 'next', 'setattr', 
                                'dict', 'hex', 'object', 'slice', 'dir', 'id', 'oct', 'sorted']

    common_words = ['self', 'the', 'name', 'to', 'of', 'none', 'get', 'path', 'bhadron', 'mdst', 'data', 
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
    
    def __init__(self, subsample_rate=0.05):
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
               and subword not in self.stop_words:
                yield subword
    

    def __iter__(self):
        for root, dirs, files in os.walk(self.folders):
            for file in files:
                if file.endswith('.py'):
                    if random.random() <= 1 - self.subsample_rate:
                        continue
                    try:
                        with open(os.path.join(root, file), 'r') as open_file:
                            lines = open_file.read()
                            for raw_word in re.findall('(\w+)', lines):
                                for clean_words in self.clean_and_split_codewords(raw_word):
                                    yield clean_words
                    except IOError:
                        pass
                    
   

    def iter_dictionaries(self):
        for root, dirs, files in os.walk(self.folders):
            for file in files:
                if file.endswith('.py'):
                    if random.random() <= 1 - self.subsample_rate:
                        continue
                    try:
                        with open(os.path.join(root, file), 'r') as open_file:
                            lines = open_file.read()
                            result = []
                            for raw_word in re.findall('(\w+)', lines):
                                for clean_words in self.clean_and_split_codewords(raw_word):
                                    result.append(clean_words)
                        yield dictionary.doc2bow(result, allow_update=True)
                    except IOError:
                        pass
                    
def get_most_common_words(n=100):
    from collections import Counter
    c = Counter()
    cw = CodeWalker()
    for word in cw:
        c.update([word])

    return map(lambda v: v[0], c.most_common(n))

cw = CodeWalker()
corpora.MmCorpus.serialize(PATH + '/../scrapers/data/test_corpus.mm', cw.iter_dictionaries())
mm = corpora.MmCorpus(PATH + '/../scrapers/data/test_corpus.mm')
print mm

num_topics=100
lda = gensim.models.ldamodel.LdaModel(corpus=mm, num_topics=num_topics, id2word=dictionary, update_every=1, chunksize=10000, passes=1)

for topic in lda.show_topics(num_topics):
    print 
    print topic