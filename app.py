from flask import Flask, render_template, request, redirect, url_for
import os
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
# import nltk
from nltk.corpus import stopwords 
import pandas as pd
import numpy as np

app = Flask(__name__)
porter = PorterStemmer()

# directory the uploaded files is saved
directory = 'D:\simplesearchengine'
# if directory doesn't exist, make a new one
if not os.path.exists(directory):
    os.makedirs(directory)

# remove punctuation in document
def removePunctuation(sentence):
    import re
    return re.sub(r'[^\w\s]', '', sentence)

# remove stopwords in document
def removeStopwords(sentence):
    stop_words = set(stopwords.words('english'))
    tokenized = word_tokenize(sentence)
    filtered_sentence = []
    for word in tokenized:
        if word not in stop_words:
            filtered_sentence.append(word)
            filtered_sentence.append(" ")
    return "".join(filtered_sentence)

# stem a document
def stemSentence(sentence):
    tokenized = word_tokenize(sentence)
    stem_sentence=[]
    for word in tokenized:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)



#  list of tuples of doc's data (nama doc, jumlahkata, kemiripan, lokasi, baris pertama dari doc)
dataList = []
query = ""
# datframe contains terms in query
df_query = pd.DataFrame()
# list of document
docList = []
@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        global query
        query = request.form["query"]
        return redirect(url_for("result"))
    return render_template("index.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename in os.listdir(directory):
            if(file.filename.split(".")[1] == "txt"):
                file.filename = file.filename.split(".")[0]+"_02.txt"
            if(file.filename.split(".")[1] == "html"):
                file.filename = file.filename.split(".")[0]+"_02.html"
        file.save(os.path.join(directory, file.filename))
        return render_template('file.html')
    return render_template('file.html')
    
@app.route("/result", methods=['GET', 'POST'])
def result():
    global query
    global df_query
    global dataList
    global docList

    df = pd.DataFrame()
    if request.method == 'POST':
        query = request.form["query"]
    # terms menyimpan daftar term
    terms = [] 
    # contain first line of doc
    firstLine = {}
    
    if dataList:
        dataList.clear()
    if docList:
        docList.clear()
    if not df_query.empty:
        for column in df_query.columns:
            df_query.drop(column, axis=1, inplace=True)

    # global terms
    # global df
    for filename in os.listdir(directory):
            # membaca tiap file di document
        file = open('D:\simplesearchengine\{}'.format(filename), encoding="utf8")
        # membaca setiap baris pada document
        my_lines_list=file.readlines()

        # if not isStemmed:
        for line in my_lines_list:
            # remove stopWords dan punctuation serta stemming tiap baris
            x = stemSentence(removeStopwords(removePunctuation(line)))
            x = x.split(" ")
            # menambahkan setiap term baru ke daftar term (terms)
            for term in x:
                if term not in terms:
                    terms.append(term)
                    
    # menghapus "" pada indeks
    # global query
    processedQuery = stemSentence(removeStopwords(removePunctuation(query)))
    processedQuery = processedQuery.split(" ")
    processedQuery = [word for word in processedQuery if word != ""]
    # menambahkan setiap term baru ke daftar term (terms)
    for term in processedQuery:
        if term not in terms:
            terms.append(term)
            
    terms = [word for word in terms if word != ""]
    term_length = len(terms)

    # menjadikan terms sebagai index
    df = pd.DataFrame(index=terms)

    df["query"] = [0 for i in range(term_length)]
    for word in processedQuery:
        df["query"][word] += 1
        
    for filename in os.listdir(directory):   
        # inisialisasi tabel term dengan 0
        df[filename.split(".")[0]] = [0 for i in range(term_length)]
        # menghitung term pada tiap document
        file = open('D:\simplesearchengine\{}'.format(filename), encoding="utf8")
        my_lines_list=file.readlines()
        
        x = []
        lineList = []
        # global firstLine
        for line in my_lines_list:
            y = stemSentence(removeStopwords(removePunctuation(line)))
            y = y.split(" ")
            x.extend(y)
            lineList.append(line)
        firstLine[filename.split(".")[0]] = lineList[0]
        # menghapus "" pada list term dari document
        x = [word for word in x if word != ""]
        # menghitung tiap term pada tiap dokumen
        for word in x:
            df[filename.split(".")[0]][word] += 1

    # append document name to docList
    for filename in os.listdir(directory):   
        docList.append(filename.split(".")[0])
    # vector of query
    vecQuery = np.array(df['query'])
    #calculate similiarity
    for doc in docList:
        vector = np.array(df[doc])
        sim = np.dot(vecQuery, vector)/(np.linalg.norm(vecQuery)*np.linalg.norm(vector))
        globals()["sim_"+doc] = sim
    # append doc's data to dataList
    
    for doc in os.listdir(directory): 
        docName = doc.split(".")[0]
        globals()[docName] = tuple((docName, df[docName].sum(), globals()["sim_"+docName], "D:/simplesearchengine/"+doc, firstLine[docName]))
        # global dataList
        dataList.append(globals()[docName])
    # sort dataList descendingly by value of "kemiripan"
    # global dataList
    dataList = sorted(dataList, key = lambda x: x[1], reverse = True)

    df_query = df.loc[processedQuery, :]
    df_query = df_query.reset_index()
    df_query = df_query.rename(columns={'index':'Term'})
    df_query['query'] = processedQuery
    return render_template("result.html", dataList=dataList, df_query=df_query, docList=docList)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
