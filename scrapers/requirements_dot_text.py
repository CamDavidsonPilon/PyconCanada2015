import re
from requests import get
from bs4 import BeautifulSoup

"""
Example search: https://github.com/search?l=text&q=requirements.txt+language%3APython+extension%3Atxt+in%3Apath+path%3A%2F&ref=searchresults&type=Code&utf8=%E2%9C%93
"""

# The API is being a PITA, I might just scrape the search results. Apparently I must specify a user/repo/org to search

def search_results_page_url(page):
    url = 'https://github.com/search?l=text&p=%d&q=requirements.txt+language:Python+extension:txt+in:path+path:/&ref=searchresults&type=Code'% page
    return url



def yield_requirements_txt_from_page(page):
    github_raw_content_url = 'https://raw.githubusercontent.com'
    html = get(search_results_page_url(page)).text
    soup = BeautifulSoup(html)
    results = soup.find_all(title="requirements.txt")

    for a_tag in results:
        raw_href = a_tag.attrs['href'].replace('blob/', '')
        yield get(github_raw_content_url + raw_href).text

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


def run(max_page=99, save_location='./data/requirements_txt.csv'):
    with open(save_location, 'w') as open_file:
        for i in range(1, max_page + 1):
            for requirements_txt in yield_requirements_txt_from_page(i):
                open_file.write(parse_requirements_txt_to_one_line(requirements_txt) + "\n")
            print "Completed page %d" % i

    print "Saved to %s" % save_location


if __name__=="__main__":
    run()