from logging.config import dictConfig

from flask import Flask, json, request
#from flask_cors import CORS, cross_origin
import jsonpickle

from do_nltk_downloads import do_nltk_downloads
from tokenize_text import do_tokenize_text

with open('tokenize_config.json') as config_file:
    CONFIG = json.load(config_file)

app = Flask(__name__)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

dictConfig({
    'version': 1, 'root': {'level': 'DEBUG'}})

app.logger.info("Server starting now.")

do_nltk_downloads()


#@cross_origin()
@app.route('/hitec/annotation/tokenize/', methods=["POST"])
def tokenize_endpoint():
    app.logger.debug('/hitec/annotation/tokenize called')
    content = json.loads(request.data.decode('utf-8'))
    text = "".join([doc["text"] + "\n" for doc in content["dataset"]["documents"]])
    ret = jsonpickle.encode(do_tokenize_text(text))
    # app.logger.debug("Returning: "+ret)
    print("Returning: " + ret)
    return ret


if __name__ == '__main__':
    app.run()
