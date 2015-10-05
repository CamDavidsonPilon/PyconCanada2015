# most_common_words


from collections import Counter
from code_walker import CodeWalker

print "Dedup on files"
c = Counter()
cw = CodeWalker(use_stop_words=False)
for non_unique_words_in_file in cw:
    # dedup on words per file
    unique_words = set(non_unique_words_in_file)
    c.update(unique_words)

print c.most_common(100)

print "Do not dedup on files"
c = Counter()
cw = CodeWalker(use_stop_words=False)
for non_unique_words_in_file in cw:
    c.update(non_unique_words_in_file)

print c.most_common(100)