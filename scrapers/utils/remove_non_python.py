# run a script that removes all non-python files, recursively. 
import os


PATH = os.path.dirname(os.path.realpath(__file__))

target_folders = [PATH + '/../data/raw_repos/', PATH + '/../data/pypi/unpacked']

total = 0
for folder in target_folders:
    print folder
    for root, dirs, files in os.walk(folder):
        for file in files:
            if not file.endswith('.py'):
                total += 1
                os.remove(os.path.join(root, file))

print "Removed %d non-python files" % total
