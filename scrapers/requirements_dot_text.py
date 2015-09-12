import re
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import csv
import os

"""
Example search: https://github.com/search?l=text&q=requirements.txt+language%3APython+extension%3Atxt+in%3Apath+path%3A%2F&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93
"""

# The API is being a PITA, I might just scrape the search results. Apparently I must specify a user/repo/org to search

def search_results_page_url(page):
    url = 'https://github.com/search?l=text&p=%d&o=desc&q=requirements.txt+language:Python+extension:txt+in:path+path:/&ref=searchresults&type=Code&s=indexed'% page
    return url


def now():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def yield_requirements_txt_from_page(page):
    github_raw_content_url = 'https://raw.githubusercontent.com'
    html = get(search_results_page_url(page)).text
    soup = BeautifulSoup(html)
    search_results = soup.find_all("p", class_="title")

    for search_result in search_results:
        a_tags = search_result.find_all('a')
        repo_name = a_tags[0].text
        raw_href = a_tags[1].attrs['href'].replace('blob/', '')
        yield repo_name, get(github_raw_content_url + raw_href).text

def parse_requirements_txt_to_one_line(requirements):
    """
    explcitly skip requirements that begin with -e, or #
    """

    library_re = re.compile('^([\w-]+)[>]?[\=]?')
    libraries = []
    for requirement in requirements.split('\n'):
        if requirement == '' or requirement.startswith('#') or requirement.startswith('-e'):
            continue

        regex_result = library_re.match(requirement)
        if regex_result:
            library = regex_result.groups()[0]
            library = library.lower().strip()
            libraries.append(library)
        else:
            print "%s did not match regex" % requirement

    return ",".join(libraries)


def run(max_page=99, save_location='/data/requirements_txt.psv'):
    save_location = os.path.dirname(os.path.realpath(__file__)) + save_location
    with open(save_location, 'a') as open_file:
        writer = csv.writer(open_file, delimiter='|')

        for i in range(1, max_page + 1):
            sleep(5)
            for repo_name, requirements_txt in yield_requirements_txt_from_page(i):
                results = parse_requirements_txt_to_one_line(requirements_txt)
                writer.writerow([repo_name, now(), results])
            print "Completed page %d" % i

    print "Saved to %s" % save_location


if __name__=="__main__":
    run()