# flat is better than nested 

from collections import Counter
from code_walker import DirectoryWalker



def find_maximum_nest(fw):
    max_nest = 0
    file_with_max_next = ''
    for file in fw:
        for line in file.readlines():
            line = line.lstrip()
            if not line.startswith('import') and not line.startswith('from'):
                continue

            if line.startswith('from'):
                if max_nest < line.count('.') + 2:
                    max_nest = line.count('.') + 2
                    file_with_max_next = str(file)
            else:
                if max_nest < line.count('.') + 1:
                    max_nest = line.count('.') + 1
                    file_with_max_next = str(file)
    return max_nest, file_with_max_next



def run():
    dw = DirectoryWalker(1.)
    results = []
    for fw in dw:
        max_nest, _ = find_maximum_nest(fw)
        results.append(max_nest)
        if max_nest >= 9:
            print fw, max_nest, _

    return Counter(results)


if __name__=="__main__":
    print run()