"""
This script will random select repos, check if they are python, and if so, we download them locally.
"""

from random import randint
from requests import get
from git import Repo
import os
from time import sleep
from ConfigParser import ConfigParser


config = ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'credentials.cfg'))


TFA_token = config.get('github', 'tfa')

def repo_endpoint_with_offset(offset):
    return append_tfa_token("""https://api.github.com/repositories?since=%d""" % (offset))

def append_tfa_token(url):
    if not url.endswith('?'):
        url += '?'
    return "%s&access_token=%s" % (url, TFA_token)

def random_sampled_offset():
    MAX = 50000000
    return randint(0, MAX)

def is_python_repo(languages_breakdown):
    total = float(sum(languages_breakdown.values()))
    if total == 0:
        return False

    return languages_breakdown.get('Python', 0)/total > 0.33

# https://github.com/CamDavidsonPilon/lifetimes.git
def yield_repos():
    
    while True:
        #import pdb 
        #pdb.set_trace()
        random_repos = get(repo_endpoint_with_offset(random_sampled_offset()))
        if random_repos.status_code == 403:
            print "sleeping for 1 hour"
            # need to wait at least 1 hour
            sleep(60*60+1) 
            continue

        for repo in random_repos.json():
            if repo['fork']:
                continue

            languages_url = repo['languages_url']
            languages_breakdown = get(append_tfa_token(languages_url))
            if languages_breakdown.status_code == 403:
                break

            languages_breakdown = languages_breakdown.json()
            if languages_breakdown and is_python_repo(languages_breakdown):
                yield repo['full_name']


def clone_repo(full_name):

    def github_repo_url(full_name):
        return "https://github.com/%s.git"%full_name

    def save_dir(full_name):
        path = os.path.dirname(os.path.realpath(__file__))
        full_name = full_name.replace('/', '_')
        return path + "/data/raw_repos/" + full_name

    Repo.clone_from(github_repo_url(full_name), save_dir(full_name))
    print "Cloned repo %s" % full_name
    return True


def run(sample_size=1):

    total = 0
    for repo in yield_repos():
        total += clone_repo(repo)

    print "Cloned %d repos"


if __name__ == '__main__':
    run()

