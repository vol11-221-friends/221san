from flask import *
import MeCab
app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/')
def index():
    # return app.send_static_file('index.html')
    return 'Hello world'

@app.route("/login_manager", methods=["POST"])  #追加
def login_manager():
    name = request.json["username"].split()
    return jsonify({"firstname":name[0], "lastname":name[1]})
    # return "" + request.json["username"] + "さん"

@app.route("/sent_analysis", methods=["POST"])
def sent_analysis():
    text = request.json["apeal"]
    m = MeCab.Tagger()

    nouns = [line for line in m.parse(text).splitlines()
                if "名詞" in line.split()[-1]]

    noun = []
    for str in nouns:
        result = str.split()
        noun.add(result[0])

    return jsonify(noun)

app.run(port=8000, debug=True)