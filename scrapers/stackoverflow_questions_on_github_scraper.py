# stackoverflow on github scraper

import re
from requests import get
from bs4 import BeautifulSoup

"""
Example search: https://github.com/search?l=python&o=desc&q=+%22stackoverflow.com%2Fquestions%22+language%3APython&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93
"""

# The API is being a PITA, I might just scrape the search results. Apparently I must specify a user/repo/org to search

def search_results_page_url(page):
    url = 'https://github.com/search?p=%d&l=python&o=desc&q="stackoverflow.com/questions"+language:Python&s=indexed&type=Code&utf8=✓'% page
    return url



def yield_code_from_page(page):
    github_raw_content_url = 'https://raw.githubusercontent.com'
    html = get(search_results_page_url(page)).text
    soup = BeautifulSoup(html)
    results = soup.find_all(title=re.compile('\.py$'))

    for a_tag in results:
        raw_href = a_tag.attrs['href'].replace('blob/', '')
        yield get(github_raw_content_url + raw_href).text

def find_stackoverflow_questions_in_file(code):
    so_regex = re.compile('stackoverflow.com/questions/[\d]+')

    for link in so_regex.findall(code):
        yield link


def run(max_page=99, save_location='./data/github_stackover_flow_questions.csv'):
    with open(save_location, 'w') as open_file:
        for i in range(1, max_page + 1):
            for code in yield_code_from_page(i):
                for link in find_stackoverflow_questions_in_file(code):
                    open_file.write(link + "\n")
            print "Completed page %d" % i

    print "Saved to %s" % save_location


if __name__=="__main__":
    run()
