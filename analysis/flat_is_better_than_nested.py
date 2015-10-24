# flat is better than nested 

from collections import Counter
from code_walker import DirectoryWalker



def find_maximum_nest(fw):
    max_nest = 0
    line_with_max_next = ''
    for file in fw:
        for line in file.readlines():
            line = line.lstrip()
            if not line.startswith('import ') and not line.startswith('from '):
                continue

            if line.startswith('from '):
                if max_nest < line.count('.') + 2:
                    max_nest = line.count('.') + 2
                    line_with_max_next = line
            else:
                if max_nest < line.count('.') + 1:
                    max_nest = line.count('.') + 1
                    line_with_max_next = line
    return max_nest, line_with_max_next



def run():
    dw = DirectoryWalker(1.)
    results = []
    for fw in dw:
        max_nest, _ = find_maximum_nest(fw)
        results.append(max_nest)
        if max_nest >= 5:
            print max_nest, '"' + _ + '"', fw

    return Counter(results)


if __name__=="__main__":
    print run()