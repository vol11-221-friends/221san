from flask import *
from janome.tokenizer import Tokenizer

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

    t = Tokenizer()
    tokens = t.tokenize(text)
    result = []
    for token in tokens:
        # 品詞を取り出し
        partOfSpeech = token.part_of_speech.split(',')[0]
    
        if partOfSpeech == u'名詞':
            result.append(token.surface)

    return jsonify(result)

app.run(port=8000, debug=True)