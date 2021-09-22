from logging.config import dictConfig

from flask import Flask, json, request
#from flask_cors import CORS, cross_origin
import jsonpickle

from do_nltk_downloads import do_nltk_downloads
from tokenize_text import do_tokenize_dataset
from example_data import example_dataset

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
    app.logger.debug('/hitec/annotation/tokenize/ called')
    content = json.loads(request.data.decode('utf-8'))
    app.logger.debug("Loaded json request: "+json.dumps(content))

    try:
        documents = content["documents"]
    except KeyError as e:
        app.logger.error("Didn't get documents, returning example data")
        documents = example_dataset

    ret = jsonpickle.encode(do_tokenize_dataset(documents), unpicklable=False)
    # app.logger.debug("Returning: "+ret)
    print("Returning: " + ret)
    return ret


if __name__ == '__main__':
    app.run(debug=False, threaded=False, host=CONFIG['HOST'], port=CONFIG['PORT'])
