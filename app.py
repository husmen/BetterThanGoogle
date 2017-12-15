# import standard
import os

# import others
import validators

# import flask
from flask import Flask, render_template, request, Markup

#import custom
from search import search1_1, count_desc

# initilize flask
APP = Flask(__name__)

# A single result template
TABLE_TEMPLATE = '''
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
RESULT_TEMPLATE = TABLE_TEMPLATE + '''
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


def result_table(count):
    """ results table"""

    result = RESULT_TEMPLATE.format(*count)
    return result


# setup the route

@APP.route('/', methods=['GET', 'POST'])
def home():
    """ Home Page """
    print("### Home Page Loaded ###")
    return render_template('index.html', page="Home")


@APP.route('/option1', methods=['GET', 'POST'])
def option1():
    """ 5th Option """

    print("### Home Page Loaded ###")
    if request.method == 'POST':
        term = str(request.form['term'])
        source = str(request.form['source'])
        if not validators.url(source):
            if validators.url("http://" + source):
                source = "http://" + source
            else:
                result = "INVALID LINK"
                return render_template('option1.html', term=term, source=source, result=Markup(result))
        count, err = search1_1(term, source)
        result = result_table(count)
        return render_template('option1.html', page="Anahtar kelime saydırma", term=term, source=source, result=Markup(result))
    return render_template('option1.html', page="Anahtar kelime saydırma")


@APP.route('/option2', methods=['GET', 'POST'])
def option2():
    """ 2nd Option """

    print("### Home Page Loaded ###")
    return render_template('option2.html', page="Sayfa (URL) Sıralama")


@APP.route('/option3', methods=['GET', 'POST'])
def option3():
    """ 3rd Option """
    print("### Home Page Loaded ###")
    return render_template('option3.html', page="Site Sıralama")


@APP.route('/option4', methods=['GET', 'POST'])
def option4():
    """ 4th Option """

    print("### Home Page Loaded ###")
    return render_template('option4.html', page="Semantik Analiz")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    APP.run(host='0.0.0.0', port=PORT)

# boom!
