import requests
from logging.config import dictConfig

from flask import Flask, json, request, jsonify
#from flask_cors import CORS, cross_origin
import jsonpickle

from do_nltk_downloads import do_nltk_downloads
from tokenize_text import do_tokenize_dataset
from example_data import example_dataset
from build_recommendation_statistic import Code, build

with open('tokenize_config.json') as config_file:
    CONFIG = json.load(config_file)

app = Flask(__name__)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

dictConfig({
    'version': 1, 'root': {'level': 'DEBUG'}})

app.logger.info("Server starting now.")

do_nltk_downloads()

'''
owners = ["Example TORE Category 1", "Example TORE Category 2", "Example TORE Category 3"]
relationship_names = ["Example Relationship 1", "Example Relationship 2", "Example Relationship 3"]
tores = ["Example TORE Category 1", "Example TORE Category 2", "Example TORE Category 3"]

all_annotations = [{"name": "Annotation number 1", "dataset": "interview_data_normal"}, {"name": "Annotation numero dos", "dataset": "interview_data_normal"}, {"name": "Die dritte Annotation", "dataset": "interview_data_normal"}]
'''

@app.route("/hitec/annotation/tokenize/", methods=["POST"])
def make_new_annotation():
    app.logger.debug('/hitec/annotation/tokenize/ called')
    content = json.loads(request.data.decode('utf-8'))
    app.logger.debug("Loaded json request: "+json.dumps(content))

    sentenceTokenisation_activated = content.get("sentenceTokenisation_activated", False)

    try:
        documents = content["dataset"]["documents"]
    except KeyError as e:
        app.logger.error("Didn't get documents, returning example data (debugging)")
        documents = example_dataset
        name = "A new placeholder name since this method doesn't receive one"
        dataset = "interview_data_normal"
        all_annotations.append({"name": name, "dataset": dataset})

    ret = jsonpickle.encode(do_tokenize_dataset("An example dataset", documents, sentenceTokenisation_activated), unpicklable=False)
    app.logger.debug("Returning: "+ret)
    print("Returning: " + ret)
    return ret


#@cross_origin()
@app.route("/hitec/annotation/status", methods=["GET"])
def get_status():
    return jsonify({"status": "operational"})

'''
@cross_origin()
@app.route("/hitec/repository/concepts/store/annotation/", methods=["POST"])
def post_annotation():
    app.logger.info("/hitec/repository/concepts/store/annotation/")
    return "Dummy endpoint success"


@cross_origin()
@app.route("/hitec/repository/concepts/annotation/name/<annotation>", methods=["GET"])
def get_annotation(annotation):
    app.logger.info("/hitec/repository/concepts/annotation/name/<annotation>/ returning dummy annotation for name: "+annotation)

    documents = example_dataset
    dataset_name = "interview_data_normal"
    ann = do_tokenize_dataset(annotation, documents);
    ann.dataset = dataset_name
    ret = jsonpickle.encode(ann, unpicklable=False)
    return ret


@cross_origin()
@app.route("/hitec/repository/concepts/annotation/all", methods=["GET"])
def get_all_annotations():
    app.logger.info("/hitec/repository/concepts/annotation/all returning all annotations")

    ret = jsonpickle.encode(all_annotations, unpicklable=False)
    return ret


@cross_origin()
@app.route("/hitec/repository/concepts/annotation/name/<annotation>", methods=["DELETE"])
def delete_annotation(annotation):
    app.logger.info("/hitec/repository/concepts/annotation/name/<annotation> deleting annotation: "+annotation)

    global all_annotations
    all_annotations = [a for a in all_annotations if a["name"] != annotation]
    ret = jsonpickle.encode(all_annotations, unpicklable=False)
    return ret


@cross_origin()
@app.route("/hitec/repository/concepts/annotation/relationships", methods=["GET"])
def get_all_relationships():
    return jsonpickle.encode({"relationship_names": relationship_names, "owners": owners})


@cross_origin()
@app.route("/hitec/repository/concepts/store/annotation/relationships/", methods=["POST"])
def post_all_relationships():

    app.logger.debug('/hitec/repository/concepts/store/annotation/relationships/ called')
    content = json.loads(request.data.decode('utf-8'))
    app.logger.debug("Loaded json request: "+json.dumps(content))

    global relationship_names, owners
    relationship_names = content["relationship_names"]
    owners = content["owners"]
    return "", 200


@cross_origin()
@app.route("/hitec/repository/concepts/annotation/tores", methods=["GET"])
def get_all_tores():
    return jsonpickle.encode({"tores": tores})


@cross_origin()
@app.route("/hitec/repository/concepts/store/annotation/tores/", methods=["POST"])
def post_all_tores():
    app.logger.debug('/hitec/repository/concepts/store/annotation/tores/ called')
    content = json.loads(request.data.decode('utf-8'))
    app.logger.debug("Loaded json request: " + json.dumps(content))

    global tores
    tores = content["tores"]
    return "", 200

'''


@app.route("/hitec/annotation/recommendation/rebuild/", methods=["POST"])
def rebuildRecommendationDb():
    app.logger.debug('/hitec/annotation/recommendation/rebuild/ called')
    response = requests.get('https://feed-uvl.ifi.uni-heidelberg.de/hitec/repository/concepts/annotationcodes/all')
    if response.status_code != 200:
        return "ERR", 404
    annotations = response.json()

    if len(annotations) == 0:
        app.logger.error('no existing annotations detected')
    else:
        app.logger.info('Count annotations: ' + str(len(annotations)))

    codes = []
    for annotation in annotations:
        if annotation['sentenceTokenisation_activated']:
            continue
        annotationCodes = annotation['codes']
        app.logger.info(annotation['name'] + " " + str(len(annotationCodes)))
        for annotationCode in annotationCodes:
            if annotationCode['name'] != "" and annotationCode['tore'] != "":
                codes.append(Code(annotationCode['name'], annotationCode['tore']))

    if len(codes) == 0:
        app.logger.info('no existing codes detected')
    else:
        app.logger.info('Count Codes: ' + str(len(codes)))

    recommendations = build(codes)

    app.logger.info(str('Count recommendations: ' + str(len(recommendations))))

    recommendations = jsonpickle.encode(recommendations, unpicklable=False)

    insertrequest = requests.post('https://feed-uvl.ifi.uni-heidelberg.de/hitec/repository/concepts/store/recommendations/', data=recommendations)

    if insertrequest.status_code != 200:
        return "ERR", 404

    return "OK", 200


if __name__ == '__main__':
    app.run(debug=False, threaded=False, host=CONFIG['HOST'], port=CONFIG['PORT'])
