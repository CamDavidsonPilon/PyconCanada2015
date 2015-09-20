# random_pypi_repos.py

import pandas as pd
from pandas.io.html import read_html
from random import randint
from requests import get
import shutil
import urllib2
from subprocess import call

def sample_from_list(n=10):
    df = pd.read_csv('./scrapers/data/list_of_pypi_packages_20150920.csv', header=0)
    n_packages = df.shape[0]

    for i in range(n):
        choice = randint(0, n_packages+1)
        yield df.ix[choice].values


def retrieve_tgz_from_pypi(package_name, package_name_version):
    first_letter_of_name = package_name[0]
    outfile = "./scrapers/data/pypi/raw/%s.tar.gz"%package_name

    url_base = lambda name, first_letter, version: "https://pypi.python.org/packages/source/%s/%s/%s.tar.gz" % (first_letter, name, version)
    url = url_base(package_name,first_letter_of_name,package_name_version)
    try:
        req = urllib2.urlopen(url)
    except Exception as e:
        print "Could not retrive from %s" % url
        return None

    with open(outfile, 'wb') as fp:
        shutil.copyfileobj(req, fp)
    print "Saved to %s" % outfile
    return outfile

def untar_unzip_tgz(file_location):
    outfolder = './scrapers/data/pypi/unpacked/'
    call(['tar', '-zxf', file_location, '-C', outfolder])
    call(['rm', file_location])


def run(sample=10):
    s = 0
    for name, version in sample_from_list(sample):
        saved_location = retrieve_tgz_from_pypi(name, version)
        if saved_location:
            s += 1
            untar_unzip_tgz(saved_location)

    print "Completed downloading %d packages from pypi" % s


if __name__ == "__main__":
    run()