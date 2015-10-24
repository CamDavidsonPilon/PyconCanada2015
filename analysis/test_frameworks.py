# testing framework

# look at mentions of pytest, nose, unitest or testify in import statements
from collections import Counter
from code_walker import DirectoryWalker


def find_testing_package(fw):
    for file in fw:
        for line in file.readlines():
            line = line.lstrip()
            if not line.startswith('import ') and not line.startswith('from '):
                continue

            for testing_pkg in ['pytest', 'nose', 'unittest', 'testify']:
                if testing_pkg in line:
                    return testing_pkg


def run():
    dw = DirectoryWalker(1.)
    results = []
    for fw in dw:
        testing_pkg = find_testing_package(fw)
        results.append(testing_pkg)

    return Counter(results)


if __name__=="__main__":
    print run()