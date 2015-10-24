# 2-spaces or 4-spaces?
from code_walker import FileWalker, DirectoryWalker
from collections import Counter



number_of_whitespaces = lambda s: len(s) - len(s.lstrip(" "))

def count_of_indents(file):
    d = []
    previous_line = ""
    for line in file.readlines():
        if line.startswith("#") or line.startswith('"') or line.startswith('"""') \
            or line.startswith("'") or line.startswith("("):
            continue
        if line.strip() == '':
            continue

        delta = number_of_whitespaces(line) - number_of_whitespaces(previous_line)
        if delta > 0:
            d.append(delta)

        previous_line = line

    return Counter(d)


def run_over_all_files(filewalker):

    results = []
    for file in filewalker:
        counter = count_of_indents(file)
        if counter:
            most_common = counter.most_common(1)[0][0]
            results.append(most_common)
    return Counter(results)


def run_over_directories():
    dw = DirectoryWalker(1.)
    results = []
    for fw in dw:
        counter = run_over_all_files(fw)
        if counter:
            most_common = counter.most_common(1)[0][0]
            results.append(most_common)
    return Counter(results)



if __name__ == "__main__":
    print run_over_directories()
