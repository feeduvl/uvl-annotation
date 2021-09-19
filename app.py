from logging.config import dictConfig

from flask import Flask, json, request

from do_nltk_downloads import do_nltk_downloads
from tokenize_text import do_tokenize_text

with open('tokenize_config.json') as config_file:
    CONFIG = json.load(config_file)

app = Flask(__name__)

dictConfig({
    'version': 1, 'root': {'level':'DEBUG'}})

app.logger.info("Server starting now.")

do_nltk_downloads()


@app.route('/hitec/annotation/tokenize', methods=["POST"])
def tokenize_endpoint():
    app.logger.debug('/hitec/annotation/tokenize called')
    content = json.loads(request.data.decode('utf-8'))
    text = content["text"]
    ret = json.dumps(do_tokenize_text(text))
    app.logger.debug("Returning: "+ret)
    return ret, 200


if __name__ == '__main__':
    app.run()
