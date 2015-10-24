import re
import os
import keyword

PATH = os.path.dirname(os.path.realpath(__file__))

CAMELCASE_TO_UNDERSCORE_RE = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

class DirectoryWalker(object):

    folders = PATH + '/../scrapers/data/raw_repos/'

    def __init__(self, subsample_rate=0.4):
        self.subsample_rate = subsample_rate

    def __iter__(self):
        for folder in os.listdir(self.folders):
            yield FileWalker(self.subsample_rate, folders=self.folders + folder)


class FileWalker(object):

    folders = PATH + '/../scrapers/data/'

    def __init__(self, subsample_rate=0.4, folders=None):
        if folders:
            self.folders = folders
        self.subsample_rate = subsample_rate

    def __iter__(self):
        for root, dirs, files in os.walk(self.folders):
            for file in files:
                if file.endswith('.py'):
                    if hash(file + root) % int(1./self.subsample_rate) != 0:
                        continue
                    try:
                        with open(os.path.join(root, file), 'r') as open_file:
                            yield open_file
                    except IOError:
                        pass

    def __repr__(self):
        return "<FileWalker for %s>" % self.folders

class CodeWalker(object):
    
    folders = PATH + '/../scrapers/data/'

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


    stop_words =  set(python_keywords + python_builtin_functions + python_types)
    
    def __init__(self, subsample_rate=0.4, use_stop_words=True):
        self.use_stop_words = use_stop_words
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
               and not subword.isdigit() \
               and re.match('^u\w{4}$', subword) is None \
               and re.match('^x\w{2}$', subword) is None \
               and (not self.use_stop_words or subword not in self.stop_words):
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
