from bs4 import BeautifulSoup
import multiprocessing
import urlparse 
import requests
import json
import os
import time
from random import shuffle

# Available: https://github.com/citp/OpenWPM/blob/master/automation/utilities/domain_utils.py  # noqa
import domain_utils as du
# Available: https://gist.github.com/englehardt/802d1872d6bda2084723489a82540cb3  # noqa
import alexa_utils as au
DEPTH = 1
DATA_DIR = os.path.expanduser('~/data/')
ALL_INTERNAL_LINKS = 'internal_links.json'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'  # noqa

def get_internal_links_depth(site, depth):
    """Request and parse internal links from `site`"""
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': USER_AGENT})
    if (depth == 0):
        result = list()
        result.append(site)
        return None, result
    try:
        try:
            if depth == DEPTH:
                resp = requests.get('http://' + site, headers=headers, timeout=60)
            else:
                resp = requests.get(site, headers=headers, timeout=60)
        except Exception as e:
            if depth == DEPTH:
                resp = requests.get('http://www.' + site, headers=headers, timeout=60)
            else:
                resp = requests.get(site, headers=headers, timeout=60)
        if resp.status_code != 200:
            print("Non-200 response code %i for site %s" % (
                resp.status_code, site))
            return (site, list())
        if resp.content is None:
            print("No content returned for site %s" % site)
            return (site, list())

        # Current URL after HTTP Redirects
        current_url = resp.url
        top_ps1 = du.get_ps_plus_1(current_url)

        # Find all internal a tags
        soup = BeautifulSoup(resp.content, 'lxml')
        links = set()
        for tag in soup.find_all('a'):
            href = tag.get('href')
            if href is None:
                continue
            href = urlparse.urljoin(current_url, href)

            #if (not href.startswith('http') or
            #        du.get_ps_plus_1(href) != top_ps1):
            if (not href.startswith('http')):
                print "top ps1"
                print top_ps1
                print du.get_ps_plus_1(href)
                print href
                continue
            links.add(urlparse.urldefrag(href)[0])

        # Craw Next Level
        links_next_layer = set()
        for link in links:
            links_next_layer |= set(get_internal_links_depth(link, depth-1)[1])
        links |= links_next_layer
        return site, list(links)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print("Exception while requesting %s\n%s" % (site, str(e)))
        return (site, list())

def get_internal_links(site):
    return get_internal_links_depth(site, depth=DEPTH)


def collect_homepage_links(sites, nprocesses=10):
    """Collect all homepage links for the given list of `sites`"""
    pool = multiprocessing.Pool(processes=nprocesses)
    results = pool.map(get_internal_links,
                       [x[1] for x in sites],
                       chunksize=100)
    pool.close()
    pool.join()
    print("Saving results to disk %s" % ALL_INTERNAL_LINKS)
    print len(results[0][1])
    with open(ALL_INTERNAL_LINKS, 'w') as f:
        json.dump(results, f)
    print "====>Finish time is:"
    finish = time.time()
    print finish
    print finish - start


def sample_top_1m():
    return au.sample_top_sites(
        location=DATA_DIR,
        include_rank=True,
        slices = [(10000, 0, 10000)]
        #slices=[(15000, 0, 15000),
         #       (15000, 15000, 100000),
          #      (20000, 100000, 1000000)]
    )


if __name__ == '__main__':
    print "====>Start time is:"
    start = time.time()
    print start
    sites = sample_top_1m()
    shuffle(sites)
    print sites
    collect_homepage_links(sites, nprocesses=30)
