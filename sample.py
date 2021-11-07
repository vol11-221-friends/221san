from flask import *
from janome.tokenizer import Tokenizer
from flask_cors import CORS
from github import GitHubApi
import collections
import csv
import pprint
import numpy as np

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
@app.route('/')
def index():
    # return app.send_static_file('index.html')
    return 'Hello world'

@app.route('/', methods=["POST"])
def main_process():
    # return app.send_static_file('index.html')
    return jsonify({"received_appeal": request.json["appeal"], "received_git_name": request.json["gitname"], "point": 100})

@app.route("/login_manager", methods=["POST"])  #追加
def login_manager():
    name = request.json["username"].split()
    return jsonify({"firstname":name[0], "lastname":name[1]})
    # return "" + request.json["username"] + "さん"

@app.route("/sent_analysis", methods=["POST"])
def sent_analysis():
    text = request.json["appeal"]

    t = Tokenizer()
    tokens = t.tokenize(text)
    result = []
    for token in tokens:
        # 品詞を取り出し
        partOfSpeech = token.part_of_speech.split(',')[0]

        if partOfSpeech == u'名詞':
            result.append(token.surface)

    with open('ProLanguages.csv',encoding = "utf-8-sig") as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    temp = []
    for i in range(len(l)):
        for j in range(len(result)):
            if result[j].lower() == l[i][0].lower():
                temp.append(l[i])

    return jsonify({"response":temp})

@app.route("/git_extract", methods=["POST"])
def sent_extract():
    api = GitHubApi()

    gitname = request.json["gitname"]

    repos = api.get_user_repos(gitname)
    langs = []

    for repo in repos:
        langs.append(repo['language'])

    c = collections.Counter(langs)
    langs_setted = set(langs)
    length = len(langs)

    for i in langs_setted:
        per = round((c[i] / length) * 100, 1)
        c.update({i: per})


    result = list(langs_setted)

    with open('ProLanguages.csv',encoding = "utf-8-sig") as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    temp = []
    for i in range(len(l)):
        for j in range(len(result)):
            if result[j] is not None:
                if result[j].lower() == l[i][0].lower():
                    temp.append(l[i])

    return jsonify({"a": list(c.items()), "b": list(set(langs)), "response":list(temp)})

app.run(port=8080, debug=True)