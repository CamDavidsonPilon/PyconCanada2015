# move all Python files to one folder

import os
import shutil

PATH = os.path.dirname(os.path.realpath(__file__))

target_folders = [PATH + '/../data/raw_repos/', PATH + '/../data/pypi/unpacked']
save_directory = PATH + '/../data/python_files/'

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

total = 0
for folder in target_folders:
    print folder
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.py'):
                total += 1
                new_file_name = "%s-%s"%(root.strip(folder).replace('/', '-'), file)
                dst = save_directory + new_file_name
                print dst
                shutil.copyfile(os.path.join(root, file), dst) 

print "Moved %d python files to %s" % (total, save_directory)