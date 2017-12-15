# import standard
import os

# import others
import validators

# import flask
from flask import Flask, render_template, request, Markup

#import custom
from search import search, COUNT_DESC, scrap

# initilize flask
APP = Flask(__name__)

# setup the route
@APP.route('/', methods=['GET', 'POST'])
def home():
    """ Home Page """
    print("### Home Page Loaded ###")
    return render_template('index.html', page="Home")


@APP.route('/option1', methods=['GET', 'POST'])
def option1():
    """ 1th Option """

    print("### Option 1 Loaded ###")
    if request.method == 'POST':
        term = str(request.form['term']).split(',')[0]
        source = str(request.form['source']).split(',')[0]

        if not validators.url(source):
            if validators.url("http://" + source):
                source = "http://" + source
            else:
                result = "<b><i>INVALID LINK</i></b>"
                return render_template('option1.html',  page="Anahtar kelime saydırma", term=term, source=source, result=Markup(result))
        err, count = search(term, source)
        if err:
            result = "<b><i>INVALID LINK</i></b>"
            return render_template('option1.html',  page="Anahtar kelime saydırma", term=term, source=source, result=Markup(result))
        else:
            return render_template('option1.html', page="Anahtar kelime saydırma", term=term, source=source, titles=COUNT_DESC, counts=count)
    return render_template('option1.html', page="Anahtar kelime saydırma")


@APP.route('/option2', methods=['GET', 'POST'])
def option2():
    """ 2nd Option """

    print("### Option 2 Loaded ###")

    if request.method == 'POST':
        results = []
        labels = []
        term = str(request.form['term'])
        source = str(request.form['source'])
        terms = term.split(',')
        sources = source.split(',')
        print(terms)
        print(sources)
        labels.append("#")
        for trm in terms:
            trm = trm.strip()
            labels.append(trm + " T")
            labels.append(trm + " I")
        labels.append("Total Index")
        for src in sources:
            flag = True
            src = src.strip()
            res_tmp = []
            index_sum = 0
            index =0
            if not validators.url(src):
                if validators.url("http://" + src):
                    src = "http://" + src
                else:
                    res_tmp.append(src)
                    res_tmp.append(len(labels)*"-")
                    flag = False
                    #return render_template('option1.html', term=term, source=source, result=Markup(result))
            if flag:
                res_tmp.append(src)
                for trm in terms:
                    err, count = search(trm, src)
                    if err:
                        res_tmp.append(len(labels)*"-")
                        #return render_template('option1.html', term=term, source=source, result=Markup(result))
                    else:
                        res_tmp.append(count[11])
                        res_tmp.append(count[12])
                        index_sum += count[12]
                                #return render_template('option1.html', page="Anahtar kelime saydırma", term=term, source=source, titles=COUNT_DESC, counts=count)
            print("### INDEX ###")
            # for i in range(2,len(res_tmp)-1,2):
            #     print("{} {} {}".format(i,index_sum,index))
            #     index += res_tmp[i]*(index_sum-res_tmp[i])/index_sum
            if len(terms) == 1:
                index = res_tmp[2]
                print("### condition met ###")
            else:
                for i in range(2,len(res_tmp)-1,2):
                    print("{} {} {}".format(i,index_sum,index))
                    index += res_tmp[i]*(index_sum-res_tmp[i])/index_sum
            res_tmp.append(index)
            results.append(res_tmp)
        print("### RESULTS ###")
        print(results)
        #results_final = dict(zip(labels, results))
        return render_template('option2.html', page="Sayfa (URL) Sıralama", term=term, source=source, titles=labels, results=results)

    return render_template('option2.html', page="Sayfa (URL) Sıralama")


@APP.route('/option3', methods=['GET', 'POST'])
def option3():
    """ 3rd Option """
    print("### Option 3 Loaded ###")

    if request.method == 'POST':
        results = []
        labels = []
        term = str(request.form['term'])
        source = str(request.form['source'])
        terms = term.split(',')
        sources = source.split(',')
        print(terms)
        print(sources)
        labels.append("#")
        for trm in terms:
            trm = trm.strip()
            labels.append(trm + " T")
            labels.append(trm + " I")
        labels.append("Total Index")
        for src in sources:
            flag = True
            src = src.strip()
            res_tmp = []
            index_sum = 0
            index =0
            if not validators.url(src):
                if validators.url("http://" + src):
                    src = "http://" + src
                else:
                    res_tmp.append(src)
                    res_tmp.append(len(labels)*"-")
                    flag = False
                    #return render_template('option1.html', term=term, source=source, result=Markup(result))
            if flag:
                res_tmp.append(src)
                for trm in terms:
                    err, count = search(trm, src)
                    if err:
                        res_tmp.append(len(labels)*"-")
                        #return render_template('option1.html', term=term, source=source, result=Markup(result))
                    else:
                        res_tmp.append(count[11])
                        res_tmp.append(count[12])
                        index_sum += count[12]
                                #return render_template('option1.html', page="Anahtar kelime saydırma", term=term, source=source, titles=COUNT_DESC, counts=count)
                err, src_sub = scrap(src)
                if err:
                    pass
                else:
                    print("### scrapped: ###")
                    print(src_sub)
            print("### INDEX ###")
            if len(terms) == 1:
                index = res_tmp[2]
                print("### condition met ###")
            else:
                for i in range(2,len(res_tmp)-1,2):
                    print("{} {} {}".format(i,index_sum,index))
                    index += res_tmp[i]*(index_sum-res_tmp[i])/index_sum
            res_tmp.append(index)
            results.append(res_tmp)
        print("### RESULTS ###")
        print(results)
        #results_final = dict(zip(labels, results))
        return render_template('option3.html', page="Site Sıralama", term=term, source=source, titles=labels, results=results)

    return render_template('option3.html', page="Site Sıralama")


@APP.route('/option4', methods=['GET', 'POST'])
def option4():
    """ 4th Option """

    print("### Option 4 Loaded ###")

    return render_template('option4.html', page="Semantik Analiz")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    APP.run(host='0.0.0.0', port=PORT)

# boom!
