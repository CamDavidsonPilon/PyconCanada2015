# run a script that removes all non-python files, recursively. 
import os
target_folder = './scrapers/data/raw_repos/'


total = 0
for root, dirs, files in os.walk(target_folder):
    for file in files:
        if not file.endswith('.py'):
            total += 1
            os.remove(os.path.join(root, file))

print "Removed %d non-python files" % total
