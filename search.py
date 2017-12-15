#import standard
import time
import urllib

#import others
import bs4
import requests
import requests_cache
import validators

# Global Variables
term = ""
source = ""
COUNT_DESC = ["Title", "Description", "Keywords", "h1", "h2", "h3", "h4", "h5", "h6", "content", "URL", "TOTAL", "index"]

links_tree = []
links = []
links_hist = set()

# Setup cache
requests_cache.install_cache('cache', backend='sqlite', expire_after=300)

# Define functions
def crawl(url):
    now = time.ctime(int(time.time()))
    print("### before request ###")
    try:
        response = requests.get(url)
    except:
        print("### after request w/ ERROR ###")
        return True, None
    
    print("### after request ###")
    
    #if response.status_code == requests.codes.ok:
    if response.status_code == 200:
        print("### Time: {0} / Used Cache: {1} ###".format(now, response.from_cache))
        html = response.text
        soup = bs4.BeautifulSoup(html, "html.parser")
        return False, soup
    else:
        return True, None

def scrap(url,depth = 0):
    if depth == 0:
        del links_tree[:]
        del links[:]
        #links_hist = {set()}

    err, soup = crawl(source)
    if err:
        return True, None

    for link in soup.find_all('a'):
        url_tmp = link.get('href')
        if not validators.url(url_tmp):
            url_tmp2 = urllib.parse.urljoin(url, url_tmp)
            if validators.url(url_tmp2):
                url_tmp = url_tmp2
        if url in url_tmp and url_tmp not in links_hist:
            links.append(url_tmp)
            links_hist.add(url_tmp)

    # links_tree.append(links)
    # print(links_tree)
    # return(links_tree)
    return(links)

def clean_soup(soup, level=1):
    if level == 1:
        while soup.find('header'):
            tmp = soup.header.extract()
        while soup.find('script'):
            tmp = soup.script.extract()
        while soup.find('footer'):
            tmp = soup.footer.extract()
    else:
        while soup.find('h1'):
            tmp = soup.h1.extract()
        while soup.find('h2'):
            tmp = soup.h2.extract()
        while soup.find('h3'):
            tmp = soup.h3.extract()
        while soup.find('h4'):
            tmp = soup.h4.extract()
        while soup.find('h5'):
            tmp = soup.h5.extract()
        while soup.find('h6'):
            tmp = soup.h6.extract()
    return soup

def search(term, source):
    """ Search Function """
    term = term.lower()
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    err, soup = crawl(source)
    if err:
        return True, None
    #print(soup.prettify())
    
    print("### TITLE ###")
    source_title = soup.title.string
    print(source_title)
    count[0] = source_title.lower().count(term)

    print("### META ###")
    meta = soup.find_all('meta')
    for element in meta:
        attributes = element.attrs
        #print(attributes)
        if "name" in attributes and element['name'] == "description":
            source_desc = element['content']
            count[1] = source_desc.lower().count(term)
            print("DESCRIPTION: " + source_desc)
        if "name" in attributes and element['name'] == "keywords":
            source_kw = element['content']
            count[2] = source_kw.lower().count(term)
            print("KEYWORDS: " + source_kw)
            
    print("### HEADLINES ###")    
    soup = clean_soup(soup,1)
    for i in range(1,7):
        h = "h{}".format(i)
        header = soup.find_all(h)
        if header:
            print(h + ":")
            source_h = soup.find_all(h)
            tmp = ""
            for item in source_h:
                tmp += item.text
            count[2+i] += tmp.lower().count(term)
            print(source_h)
            print(tmp.lower())

    print("### BODY TEXT without headlines and junk ###")
    soup = clean_soup(soup, 2)
    text = soup.body.get_text()
    #print(text)

    print("### COUNT ###")
    count[9] = text.lower().count(term)
    count[10] = source.lower().count(term)
    count[11] = sum(count[:11])
    hd_ind = 0.6*count[3]+0.5*count[4]+0.4*count[5]+0.3*count[6]+0.2*count[7]+0.1*count[8]
    count[12] = 0.15*(sum(count[:3])+count[10])+hd_ind+0.19*count[9]

    return False, count
