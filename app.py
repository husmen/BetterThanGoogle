# import standard
import os
import time
import urllib

# import others
import bs4
import requests
import requests_cache

# import flask
from flask import Flask, render_template, request, Markup

# initilize flask
app = Flask(__name__)

# Global Variables
term = "static"
source = "http://localhost/sample/Static%20Website%20Definition.htm"
count_desc = ["Title", "Description", "Keywords", "h1", "h2", "h3", "h4", "h5", "h6", "content - h", "index"]
#count_desc[0],count_desc[1],count_desc[2],count_desc[3],count_desc[4],count_desc[5],count_desc[6],count_desc[7],count_desc[8],count_desc[9],count_desc[10]
#count[0],count[1],count[2],count[3],count[4],count[5],count[6],count[7],count[8],count[9],count[10]

# A single result template
table_template = '''
<table style="width:100%">
  <tr>
    <th>{}</th>
    <th>{}</th> 
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
  </tr>
'''.format(*count_desc)
result_template = table_template + '''
  <tr>
    <th>{}</th>
    <th>{}</th> 
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
  </tr>
</table>
'''

#cnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Setup cache
requests_cache.install_cache('cache', backend='sqlite', expire_after=300)

# Define functions
def crawl(url):
    now = time.ctime(int(time.time()))
    response = requests.get(url)
    print("Time: {0} / Used Cache: {1}".format(now, response.from_cache))
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup

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

def search1_1(term, source):
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    soup = crawl(source)
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
            #print(h + ":")
            source_h = soup.find_all(h)
            tmp = ""
            for item in source_h:
                tmp += item.text
            count[2+i] += tmp.lower().count(term)
            #print(source_h)
            
    print("### BODY TEXT without headlines and junk ###")
    soup = clean_soup(soup,2)
    text = soup.body.get_text()
    #print(text)

    print("### COUNT ###")
    count[9] = text.lower().count(term)
    for i in range(10):
        tmp = count_desc[i] + ": {}".format(count[i])
        print(tmp)
    print("total visible: {}".format(sum(count[3:10])))
    print("total: {}".format(sum(count)))

    return count

def result_table(count):
    result = result_template.format(*count)
    return result

# setup the route
@app.route('/', methods=['GET', 'POST'])
def home():
    print("### Home Page Loaded ###")
    if request.method == 'POST':
        term = str(request.form['term'])
        source = str(request.form['source'])
        count = search1_1(term,source)
        #print(count)
        result = result_table(count)
        print(result)
        return render_template('index.html', term=term, source=source, result = Markup(result))
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
# boom!
