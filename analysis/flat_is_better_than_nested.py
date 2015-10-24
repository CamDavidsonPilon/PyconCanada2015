# flat is better than nested 

from collections import Counter
from code_walker import DirectoryWalker



def find_maximum_nest(fw):
    max_nest = 0
    for file in fw:
        for line in file.readlines():
            line = line.lstrip()
            if not line.startswith('import') and not line.startswith('from'):
                continue

            if line.startswith('from'):
                max_nest = max(line.count('.') + 2, max_nest)
            else:
                max_nest = max(line.count('.') + 1, max_nest)
    return max_nest



def run():
    dw = DirectoryWalker(1.)
    results = []
    for fw in dw:
        max_nest = find_maximum_nest(fw)
        results.append(max_nest)
        if max_nest >= 8:
            print fw

    return Counter(results)


if __name__=="__main__":
    print run()